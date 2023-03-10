from flask_restx import Resource, Namespace
from project.dao.model.movie import MovieSchema

from project.container import movie_service

#from decorators import admin_required, auth_required

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    #@auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    #@admin_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    #@auth_required
    def get(self, bid):
        b = movie_service.get_one(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    #@admin_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    #@admin_required
    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204

#############################
from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)

# список всех фильмов
movies = [
    {"id": 1, "title": "Movie 1", "status": "old"},
    {"id": 2, "title": "Movie 2", "status": "new"},
    {"id": 3, "title": "Movie 3", "status": "old"},
    # ... дополнительные записи ...
]

# функция для фильтрации фильмов по статусу
def filter_movies_by_status(movies, status):
    if status == "new":
        return sorted(movies, key=lambda x: x["id"], reverse=True)
    else:
        return movies

@app.route('/movies/')
def get_movies():
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = 12

    # фильтрация фильмов по статусу (если параметр status указан)
    filtered_movies = movies if not status else filter_movies_by_status(movies, status)

    # пагинация
    start = (page - 1) * per_page
    end = start + per_page
    paginated_movies = filtered_movies[start:end]

    # подсчет количества страниц
    total_pages = len(filtered_movies) // per_page + (len(filtered_movies) % per_page > 0)

    # формирование ответа
    response = {
        "movies": paginated_movies,
        "total_pages": total_pages,
        "current_page": page
    }
    return jsonify(response)
##################

