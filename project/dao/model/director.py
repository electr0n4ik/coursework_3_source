from marshmallow import Schema, fields

from project.setup.db import db


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
