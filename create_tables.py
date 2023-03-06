from project.config import config
from project.server import create_app
from project.setup.db import db

from project.dao.model import *

if __name__ == '__main__':
    with create_app(config).app_context():
        db.add
        db.create_all()
