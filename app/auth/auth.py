import hashlib
from datetime import datetime

from app.db import get_db
from app.profile import Member
from app.utils import rand_str


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
        db.auth.insert_one({
            'uid': uid,
            'username': username,
            'password': cls.encrypt_password(password, src),
            'auth_level': 'member'
        })

    @classmethod
    def get_next_uid(cls):
        db = get_db()
        res = db.counters.find_one_and_update(
            {'_id': 'uid'}, {'$inc': {'next_uid': 1}})
        return res['next_uid']

    @classmethod
    def register(cls, en_name, password):
        uid = cls.get_next_uid()
        username = en_name.replace(' ', '').lower()
        cls.add_new_user(uid, username, password, 'md5')
        member_info = Member().to_info()
        member_info['uid'] = uid
        member_info['en_name'] = en_name
        member_info['created_time'] = datetime.utcnow()
        member_info['updated_time'] = datetime.utcnow()
        member_info['publications'] = []
        db = get_db()
        db.members.insert_one(member_info)
        return {'success': True, 'uid': uid}
