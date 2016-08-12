import hashlib
import random
import string

from app.db import get_db


class Auth(object):

    @classmethod
    def encrypt_password(cls, raw_password, salt_len=8):
        hash1 = hashlib.md5(raw_password.encode()).hexdigest()
        salt = ''.join(random.choice(string.ascii_lowercase + string.digits)
                       for i in range(salt_len))
        return salt + hashlib.md5((salt + hash1).encode()).hexdigest()

    @classmethod
    def check_password(cls, password, db_password, salt_len=8):
        salt = db_password[:salt_len]
        if salt + hashlib.md5((salt + password).encode()).hexdigest() == db_password:
            return True
        else:
            return False

    @classmethod
    def verify_user(cls, username, password):
        db = get_db()
        user = db.auth.find_one({'username': username})
        if not user:
            return {'success': False, 'msg': 'The username does not exist!'}
        elif not cls.check_password(password, user['password']):
            return {'success': False, 'msg': 'Wrong password!'}
        else:
            return {'success': True}

    @classmethod
    def get_user_info(cls, username):
        db = get_db()
        user = db.auth.find_one({'username': username})
        return user

    @classmethod
    def add_new_user(cls, uid, username):
        db = get_db()
        db.auth.insert_one({
            'uid': uid,
            'username': username,
            'password': cls.encrypt_password(username),
            'auth_level': 'member'
        })
