import os

from flask import Flask, render_template

from app.config import CONFIG
from app.auth import mod_auth
from app.member import mod_member
from app.overview import mod_overview


app = Flask(__name__)

app.secret_key = os.urandom(24)

app.register_blueprint(mod_auth)
app.register_blueprint(mod_member)
app.register_blueprint(mod_overview)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
