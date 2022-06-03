from flask import Flask, request, abort
from flask_restx import Api
import jwt

from setup_db import db
from views.movies import movies_ns
from views.directors import directors_ns
from views.genres import genre_ns
from views.users import users_ns
from views.auth import auth_ns

from models import User

from config import Config

secret = 's3cR$eT'
algo = 'HS256'


config = Config


def create_app():
    config = Config
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)
    # create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()

        u1 = User(username="vasya", password="my_little_pony", role="user")
        u2 = User(username="oleg", password="qwerty", role="user")
        u3 = User(username="oleg", password="P@ssw0rd", role="admin")

        with db.session.begin():
            db.session.add_all([u1, u2, u3])




app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
