from sqlalchemy import Column, String, Integer, Float, ForeignKey

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class Director(models.Base):
    __tablename__ = 'director'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class User(models.Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String)
    surname = Column(String)


class Movie(models.Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=False)
    director_id = Column(Integer, ForeignKey("director.id"), nullable=False)
