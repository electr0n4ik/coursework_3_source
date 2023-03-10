import hmac

from project.dao.user import UserDAO
import base64
import hashlib
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        users = self.dao.get_all()
        return users

    def get_by_username(self, uid):
        return self.dao.get_by_username(uid)

    def get_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def create(self, user_d):
        user_d["password"] = self.get_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def compare_passwords(self, hash_pass, input_pass):
        decoded_digest = base64.b64decode(hash_pass)

        hash_digest = base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            input_pass.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))
        return hmac.compare_digest(decoded_digest, hash_digest)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)
