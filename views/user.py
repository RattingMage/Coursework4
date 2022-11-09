import jwt
from flask import request, abort
from flask_restx import Resource, Namespace

from constants import JWT_SECRET, JWT_ALGORITHMS
from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('user')


@user_ns.route("/")
class UserDataView(Resource):
    def get(self):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        user_d = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHMS])
        user = user_service.get_one(user_d.get("id"))

        return UserSchema().dump(user), 200

    def patch(self):
        user_d = request.json
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHMS])
        user_d["id"] = user.get("id", None)
        user_service.update_profile(user_d)
        return "", 200


@user_ns.route("/password")
class UserPasswordView(Resource):
    def put(self):
        data = request.json
        password_1 = data.get("password_1")
        password_2 = data.get("password_2")

        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHMS])

        user_service.update_password(password_1, password_2, user)

        return "", 200
