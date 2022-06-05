from flask_restx import Resource, Namespace
from models import User, UserSchema
from setup_db import db
from flask import request
from required import generate_password

users_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_ns.route('/')
class UserView(Resource):
    def get(self):
        select = db.session.query(User).all()
        return users_schema.dump(select), 200

    def post(self):
        data = request.get_json()
        passwd = data['password']
        # print(passwd)
        data['password'] = generate_password(str(passwd))  # меняем значение поля password на хэш
        new_user = User(**data)
        with db.session.begin():
            db.session.add(new_user)
        return "", 204


@users_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        select = db.session.query(User.id,
                                  User.username,
                                  User.password,
                                  User.role)
        filter = select.filter(User.id == uid).one()
        return user_schema.dump(filter), 200

    def put(self, uid):
        data = request.get_json()
        user = User.query.get(uid)
        if data['username']:
            user.username = data['username']
        if data['password']:
            user.password = generate_password(data['password'])  # подаем нормальный пароль, но записываем хэшованный
        if data['role']:
            user.role = data['role']
        db.session.add(user)
        db.session.commit()
        return "", 204

    def delete(self, uid):
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return "", 204
