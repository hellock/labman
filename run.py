#!/usr/bin/env python3

from app import app, CONFIG
from app.auth import mod_auth
from app.member import mod_member
from app.notification import mod_notification
from app.overview import mod_overview
from app.stats import mod_stats


def main():
    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_member)
    app.register_blueprint(mod_notification)
    app.register_blueprint(mod_overview)
    app.register_blueprint(mod_stats)
    if CONFIG['run_mode'] == 'debug':
        app.run(debug=True, host='0.0.0.0')
    elif CONFIG['run_mode'] == 'deploy':
        app.run(host='0.0.0.0')
    else:
        raise ValueError('run_mode must be either "debug" or "deploy"')


if __name__ == '__main__':
    main()
