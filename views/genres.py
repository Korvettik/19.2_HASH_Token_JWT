from flask_restx import Resource, Namespace
from models import Movie, Director, Genre, MovieSchema, DirectorSchema, GenreSchema
from setup_db import db
from flask import request
from required import auth_required, admin_required

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        select = db.session.query(Genre.name).all()
        return genres_schema.dump(select), 200

    @admin_required
    def post(self):
        data = request.get_json()
        new_genre = Genre(**data)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 204

@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        select = db.session.query(Genre.id,
                                  Genre.name)
        where = select.filter(Genre.id == gid).one()
        return genre_schema.dump(where), 200

    @admin_required
    def put(self, gid):
        data = request.get_json()
        genre = Genre.query.get(gid)
        if data['name']:
            genre.name = data['name']
        db.session.add(genre)
        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, gid):
        genre = Director.query.get(gid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204