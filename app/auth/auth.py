import hashlib

from app.db import get_db
from app.utils import get_next_uid, rand_str


class Auth(object):

    @classmethod
    def encrypt_password(cls, password, src='plain_text', salt_len=8):
        if src == 'plain_text':
            hash1 = hashlib.md5(password.encode()).hexdigest()
        elif src == 'md5':
            hash1 = password
        else:
            raise ValueError('`src` must be either "plain_text" or "md5"')
        salt = rand_str(salt_len)
        return salt + hashlib.md5((salt + hash1).encode()).hexdigest()

    @classmethod
    def check_password(cls, password, db_password, salt_len=8):
        salt = db_password[:salt_len]
        if salt + hashlib.md5((salt + password).encode()).hexdigest() == db_password:
            return True
        else:
            return False

    @classmethod
    def change_password(cls, uid, old_password, new_password, salt_len=8):
        db = get_db()
        user = db.auth.find_one({'uid': uid})
        if not cls.check_password(old_password, user['password']):
            return {'success': False, 'msg': 'Old password is not corrent!'}
        else:
            encrypted = cls.encrypt_password(new_password, 'md5')
            db.auth.update_one({'uid': uid}, {'$set': {'password': encrypted}})
            return {'success': True, 'msg': ''}

    @classmethod
    def verify_user(cls, username, password):
        db = get_db()
        user = db.auth.find_one({'username': username})
        if not user:
            return {'success': False, 'msg': 'The username does not exist!'}
        elif not cls.check_password(password, user['password']):
            return {'success': False, 'msg': 'Wrong password!'}
        else:
            return {'success': True, 'msg': ''}

    @classmethod
    def get_user_info(cls, username):
        db = get_db()
        user = db.auth.find_one({'username': username})
        return user

    @classmethod
    def add_new_user(cls, uid, username, password=None, src='plain_text'):
        if not password:
            password = username
        db = get_db()
        if db.auth.find_one({'username': username}):
            for idx in range(1, 100):
                new_username = '{}{:>02d}'.format(username, idx)
                if not db.auth.find_one({'username': new_username}):
                    username = new_username
                    break
        db.auth.insert_one({
            'uid': uid,
            'username': username,
            'password': cls.encrypt_password(password, src),
            'auth_level': 'member'
        })
        return username

    @classmethod
    def del_user(cls, uid):
        db = get_db()
        db.auth.delete_one({'uid': uid})

    @classmethod
    def register(cls, en_name, password):
        uid = get_next_uid()
        username = en_name.replace(' ', '').lower()
        username = cls.add_new_user(uid, username, password, 'md5')
        return {'success': True, 'uid': uid, 'username': username}
