#!/usr/bin/env python3

from app import app, CONFIG


if __name__ == '__main__':
    if CONFIG['run_mode'] == 'debug':
        app.run(debug=True, host='0.0.0.0')
    elif CONFIG['run_mode'] == 'deploy':
        app.run(host='0.0.0.0')
    else:
        raise ValueError('run_mode must be either "debug" or "deploy"')
