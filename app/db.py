from flask import g
from pymongo import ASCENDING, MongoClient


def init_db():
    db = connect_db()
    db.counters.insert_one({'_id': 'uid', 'next_uid': 1000})
    db.auth.create_index([('uid', ASCENDING)], unique=True)
    db.members.create_index([('uid', ASCENDING)], unique=True)


def connect_db():
    client = MongoClient('localhost', 27017)
    return client['mmlab']


def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db
