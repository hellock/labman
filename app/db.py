from datetime import datetime

from flask import g
from pymongo import ASCENDING, MongoClient, TEXT

from app import CONFIG
from app.utils import rand_str


def init_db():
    db = connect_db()
    # create counter collection and add uid counter
    db.counters.insert_one({'_id': 'uid', 'next_uid': 1000})
    # add an admin account
    from app.auth import Auth
    from app.profile import Member
    admin_username = 'admin'
    admin_password = rand_str(8)
    encrypted = Auth.encrypt_password(admin_password)
    db.auth.insert_one({
        'uid': 0, 'username': admin_username,
        'password': encrypted, 'auth_level': 'admin'})
    # add an empty admin memebr
    empty_info = Member().to_info()
    empty_info['uid'] = 0
    empty_info['created_time'] = datetime.utcnow()
    empty_info['updated_time'] = datetime.utcnow()
    empty_info['publications'] = []
    db.members.insert_one(empty_info)
    # create indexes
    db.auth.create_index([('uid', ASCENDING)], unique=True)
    db.members.create_index([('uid', ASCENDING)], unique=True)
    db.members.create_index([('en_name', TEXT)])
    return (admin_username, admin_password)


def connect_db():
    client = MongoClient(CONFIG['db']['ip'], CONFIG['db']['port'])
    return client[CONFIG['db']['name']]


def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db
