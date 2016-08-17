import logging
import random
import string

from log4mongo.handlers import MongoHandler

from app import CONFIG
from app.db import get_db


def rand_str(len, case='any'):
    if case == 'any':
        str_set = string.ascii_letters + string.digits
    elif case == 'lower':
        str_set = string.ascii_lowercase + string.digits
    elif case == 'upper':
        str_set = string.ascii_uppercase + string.digits
    else:
        raise ValueError('case must be "lower", "upper" or "any"')
    return ''.join(random.choice(str_set) for i in range(len))


def get_next_uid():
    db = get_db()
    res = db.counters.find_one_and_update(
        {'_id': 'uid'}, {'$inc': {'next_uid': 1}})
    return res['next_uid']


def get_logger(name):
    logging.basicConfig(level=CONFIG['log']['level'])
    logger = logging.getLogger(name)
    logger.addHandler(MongoHandler(host=CONFIG['db']['ip'],
                                   capped=CONFIG['log']['capped']))
    return logger
