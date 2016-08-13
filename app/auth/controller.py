from flask import Blueprint, flash, request, render_template, session, redirect, url_for

from .auth import Auth
from app import CONFIG


mod_auth = Blueprint('mod_auth', __name__, static_folder='../static')


@mod_auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('mod_auth.signin'))


@mod_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'config' not in session:
        session['config'] = CONFIG
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        ret = Auth.verify_user(request.form['username'], request.form['password'])
        if not ret['success']:
            return render_template('signin.html', error_msg=ret['msg'])
        else:
            user_info = Auth.get_user_info(request.form['username'])
            session['uid'] = user_info['uid']
            session['auth_level'] = user_info['auth_level']
            return redirect(url_for('mod_admin.overview'))


@mod_auth.route('/signout', methods=['GET'])
def signout():
    session.clear()
    return render_template('signin.html')


@mod_auth.route('/account', methods=['GET', 'POST'])
def account():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    if request.method == 'GET':
        return render_template('account.html')
    else:
        ret = Auth.change_password(session['uid'], request.form['old_password'],
                                   request.form['new_password'])
        if ret['success']:
            flash('Password successfully changed!')
            return redirect(url_for('mod_admin.overview'))
        else:
            return render_template('account.html', error_msg=ret['msg'])
