import calendar
import datetime

import jwt
from flask import abort

from constants import JWT_SECRET, JWT_ALGORITHMS
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, user_d):
        return self.user_service.create(user_d)

    def generate_tokens(self, email, password, is_refreshed=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            raise abort(404)

        if not is_refreshed:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            "id": user.id,
            "email": user.email,
            "password": user.password.decode('UTF-8')
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHMS)

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHMS)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, access_token, refresh_token):
        data1 = jwt.decode(jwt=access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHMS])
        data2 = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHMS])

        email1 = data1.get('email')
        email2 = data2.get('email')

        if email1 == email2:
            return self.generate_tokens(email2, None, is_refreshed=True)
