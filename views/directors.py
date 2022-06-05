from flask_restx import Resource, Namespace
from models import Director, DirectorSchema
from setup_db import db
from flask import request
from required import auth_required, admin_required

directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorView(Resource):
    def get(self):
        select = db.session.query(Director.name).all()
        return directors_schema.dump(select), 200

    @admin_required
    def post(self):
        data = request.get_json()
        new_director = Director(**data)
        with db.session.begin():
            db.session.add(new_director)
        return "", 204


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        select = db.session.query(Director.id,
                                  Director.name)
        where = select.filter(Director.id == did).one()
        return director_schema.dump(where), 200

    @admin_required
    def put(self, did):
        data = request.get_json()
        director = Director.query.get(did)
        if data['name']:
            director.name = data['name']
        db.session.add(director)
        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, did):
        director = Director.query.get(did)
        db.session.delete(director)
        db.session.commit()
        return "", 204
