#!/usr/bin/env python3

from app import db


if __name__ == '__main__':
    print('Initializing the database...')
    admin_username, admin_pass = db.init_db()
    print('Initialization done')
    print('Initial admin username: {}, password: {}'.format(
          admin_username, admin_pass))
