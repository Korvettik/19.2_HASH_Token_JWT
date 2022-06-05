from flask import request, abort
import jwt

import datetime
import calendar
from models import User
from flask_restx import Resource, Namespace
from setup_db import db
from required import secret, algo, generate_password

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        # просто парсим данные, полученные на вход, с проверкой что они есть
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            abort(400)

        # делаем запрос в бд и получаем строку-кортеж (если она есть и соответствует выше), (имя, хэш-пароль, роль)
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        # если все ок, делаем новый хэш из полученного пароля (с проверкой) - проверка пароля
        user_password = generate_password(password)  # делаем хэш из полученного пароля
        if user.password != user_password:  # сравниваем хэш-пароль пользователя из бд с хэш-паролем введенным
            return {"error": "Неверные учётные данные"}, 401

        # если все ок, формируем данные пользователя (спецсловарь) из базы данных (далее пригодится)
        # в реальности это просто будет информация для работы с бд, она будет храниться в шифрованном виде
        # пароль сюда в чистом виде лучше не сувать
        data = {
            "username": user.username,
            "role": user.role
        }

        # генерим access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)

        # генерим refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)

        # формируем результат
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens, 201

    def put(self):
        # проверка наличия рефреш токена в теле запроса
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        # пробуем расшифровать рефреш токен
        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(401)

        # из запроса получаем имя пользователя
        username = data.get("username")
        print(username)

        # получаем модель-строку из базы-данных по имени пользователя
        user = db.session.query(User).filter(User.username == username).first()

        # формируем данные пользователя (спецсловарь) из базы данных (далее пригодится)
        data = {
            "username": user.username,
            "role": user.role
        }

        # генерим access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)

        # генерим refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)

        # формируем результат
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201
