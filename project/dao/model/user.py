from marshmallow import Schema, fields

from project.setup.db import db

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, nullable=False, unique=True)
	password = db.Column(db.String, nullable=False)
	name = db.Column(db.String)
	surname = db.Column(db.String)
	favorite_genre = db.Column(db.String)


class UserSchema(Schema):
	id = fields.Int()
	username = fields.Str()
	password = fields.Str()
	role = fields.Str()
	