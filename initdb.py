#!/usr/bin/env python3

from app import db


if __name__ == '__main__':
    print('Initializing the database...')
    db.init_db()
    print('Initialization done')
