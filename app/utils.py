import logging
import random
import string

from log4mongo.handlers import MongoHandler
from PIL import Image

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


def crop_square(filename):
    img = Image.open(filename)
    w, h = img.size
    if w == h:
        return
    elif w > h:
        x = round((w - h) / 2)
        region = img.crop((x, 0, x + h, h))
    else:
        y = round((h - w) / 2)
        region = img.crop((0, y, w, y + w))
    region.save(filename)
