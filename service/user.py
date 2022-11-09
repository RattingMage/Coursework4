import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def update_profile(self, user_d):
        return self.dao.update_profile(user_d)

    # Do later
    def update_password(self, password_1, password_2, user):
        if self.compare_passwords(user.get("password").encode('utf-8'), password_1) and password_1 != password_2:
            password_2_digest = self.generate_password(password_2)
            user["password"] = password_2_digest
            self.dao.update_password(user)

    def create(self, user_d):
        user_d['password'] = self.generate_password(user_d.get('password'))
        return self.dao.create(user_d)

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password):
        hash_digset = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digset)

    def compare_passwords(self, password_hash, other_password) -> bool:
        hash_digest = self.generate_password(other_password)

        return hmac.compare_digest(password_hash, hash_digest)
