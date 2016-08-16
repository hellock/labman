from flask import Blueprint, flash, jsonify, request, render_template, session, redirect, url_for

from .auth import Auth
from app import CONFIG
from app.member import Member


mod_auth = Blueprint('mod_auth', __name__, static_folder='../static')


@mod_auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('mod_auth.signin'))


@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'config' not in session:
        session['config'] = CONFIG
    if request.method == 'GET':
        return render_template('register.html')
    else:
        ret = Auth.register(request.form['en_name'], request.form['password'])
        if ret['success']:
            member = Member()
            member.uid = ret['uid']
            member.en_name = request.form['en_name']
            member.create()
            session['uid'] = ret['uid']
            session['auth_level'] = 'member'
            flash('Your username is {}, please complete your profile as soon!'
                  .format(ret['username']), 'info')
            return redirect(url_for('mod_overview.index'))
        else:
            return render_template('register.html', error_msg=ret['msg'])


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
            return redirect(url_for('mod_overview.index'))


@mod_auth.route('/signout', methods=['GET'])
def signout():
    session.pop('uid', None)
    return redirect(url_for('mod_auth.signin'))


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
            flash('Password successfully changed!', 'success')
            return redirect(url_for('mod_overview.index'))
        else:
            return render_template('account.html', error_msg=ret['msg'])


@mod_auth.route('/setting', methods=['GET'])
def setting():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        return render_template('access_denied.html',
                               info='You do not have access to settings, '
                                    'please contact the administrators.')
    usernames = Auth.list_all()
    admins = Auth.get_admins()
    return render_template('setting.html', usernames=usernames, admins=admins)


@mod_auth.route('/setting/admin', methods=['POST'])
def set_admin():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        return render_template('access_denied.html',
                               info='You do not have access to settings, '
                                    'please contact the administrators.')
    Auth.set_admins(request.form.getlist('admins[]'))
    flash('Admins updated!', 'success')
    return jsonify({'success': True})
