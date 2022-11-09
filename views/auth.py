from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class RegAuthView(Resource):
    def post(self):
        try:
            req_json = request.json
            user = auth_service.register(req_json)
            return "", 201, {"location": f"/users/{user.id}"}
        except:
            return "", 501


@auth_ns.route('/login')
class RegAuthView(Resource):
    def post(self):
        data = request.json
        email = data.get('email', None)
        password = data.get('password', None)
        if None in [email, password]:
            return "", 400
        tokens = auth_service.generate_tokens(email, password)
        # request.headers["Authorization"] = f"Bearer {tokens['access_token']}"
        return tokens, 201, {"Authorization": f"Bearer {tokens['access_token']}"}

    def put(self):
        data = request.json

        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')

        tokens = auth_service.approve_refresh_token(access_token, refresh_token)
        request.headers["Authorization"] = f"Bearer {tokens['access_token']}"
        return tokens, 201
