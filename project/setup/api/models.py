from flask_restx import fields, Model

from project.setup.api import api
# Модели для сериализации:
# жанров
genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

# режиссеров
director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Дени Вильнев'),
})

# фильмов
movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Дюна'),
    'description': fields.String(required=True, max_length=200, example='Тимоти Шаламе грустно смотрит вдаль'),
    'trailer': fields.String(required=True, max_length=200, example='Видео на ютубе'),
    'year': fields.Integer(required=True, example=2021),
    'rating': fields.Float(required=True, example=10.0),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director)
})

# пользователей
user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='ivan.ivanov@gmail.com'),
    'name': fields.String(max_length=100, example='Иван'),
    'surname': fields.String(max_length=100, example='Иванов'),
    'genre': fields.Nested(genre)
})