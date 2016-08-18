import os

from flask import Flask, redirect, render_template, session, url_for
from flask_mail import Mail

try:
    from app.config import CONFIG
except ImportError:
    from app.config_default import CONFIG


app = Flask(__name__)

app.config['MAIL_SERVER'] = CONFIG['mail']['server']
app.config['MAIL_PORT'] = CONFIG['mail']['port']
app.config['MAIL_USE_SSL'] = CONFIG['mail']['use_ssl']
app.config['MAIL_DEFAULT_SENDER'] = CONFIG['mail']['address']
app.config['MAIL_USERNAME'] = CONFIG['mail']['address']
app.config['MAIL_PASSWORD'] = CONFIG['mail']['password']

app.secret_key = os.urandom(24)

mailer = Mail(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.route('/help', methods=['GET'])
def help():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    return render_template('user_guide.html')
