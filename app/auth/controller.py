from flask import Blueprint, flash, jsonify, request, render_template, session, redirect, url_for

from .auth import Auth
from app import CONFIG
from app.member import Member
from app.utils import get_logger, get_position_name


mod_auth = Blueprint('mod_auth', __name__, static_folder='../static')

logger = get_logger(__name__)


def init_session(auth_level, member):
    session['uid'] = member.uid
    session['auth_level'] = auth_level
    session['en_name'] = member.en_name
    session['position'] = get_position_name(member.position)
    session['avatar_url'] = member.avatar_url


@mod_auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('mod_auth.signin'))


@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'config' not in session:
        session['config'] = CONFIG
    if request.method == 'GET':
        logger.info('/register')
        if session['config']['open_registration']:
            return render_template('register.html')
        else:
            return render_template('register_not_open.html')
    else:
        if not session['config']['open_registration']:
            return
        ret = Auth.register(request.form['en_name'], request.form['password'])
        if ret['success']:
            logger.info('registration success',
                        extra={'uid': ret['uid'],
                               'en_name': request.form['en_name'],
                               'username': ret['username']})
            member = Member()
            member.uid = ret['uid']
            member.en_name = request.form['en_name']
            member.create()
            init_session('member', member)
            flash('Your username is {}, please complete your profile as soon!'
                  .format(ret['username']), 'info')
            return redirect(url_for('mod_member.profile'))
        else:
            logger.info('registration failure',
                        extra={'en_name': request.form['en_name'],
                               'msg': ret['msg']})
            return render_template('register.html', error_msg=ret['msg'])


@mod_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'config' not in session:
        session['config'] = CONFIG
    if request.method == 'GET':
        logger.info('/signin')
        return render_template('signin.html')
    else:
        ret = Auth.verify_user(request.form['username'], request.form['password'])
        if ret['success']:
            user_info = Auth.get_user_info(request.form['username'])
            member = Member.get_by_uid(user_info['uid'])
            init_session(user_info['auth_level'], member)
            logger.info('signin success',
                        extra={'uid': user_info['uid'],
                               'username': request.form['username']})
            return redirect(url_for('mod_overview.index'))
        else:
            logger.error('signin failure',
                         extra={'username': request.form['username'],
                                'password': request.form['password']})
            return render_template('signin.html', error_msg=ret['msg'])


@mod_auth.route('/signout', methods=['GET'])
def signout():
    logger.info('signout',
                extra={'uid': session['uid'],
                       'en_name': session['en_name']})
    session.pop('uid', None)
    return redirect(url_for('mod_auth.signin'))


@mod_auth.route('/account', methods=['GET', 'POST'])
def account():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    if request.method == 'GET':
        logger.info('/account',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name']})
        return render_template('account.html')
    else:
        ret = Auth.change_password(session['uid'], request.form['old_password'],
                                   request.form['new_password'])
        if ret['success']:
            flash('Password successfully changed!', 'success')
            logger.info('password change success',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name']})
            return redirect(url_for('mod_overview.index'))
        else:
            logger.info('password change failure',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name']})
            return render_template('account.html', error_msg=ret['msg'])


@mod_auth.route('/setting', methods=['GET'])
def setting():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        logger.info('setting page access denied',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name']})
        return render_template('access_denied.html',
                               info='You do not have access to settings, '
                                    'please contact the administrators.')
    logger.info('/setting',
                extra={'uid': session['uid'],
                       'en_name': session['en_name']})
    usernames = Auth.list_all()
    admins = Auth.get_admins()
    return render_template('setting.html', usernames=usernames, admins=admins)


@mod_auth.route('/setting/admin', methods=['POST'])
def set_admin():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        logger.info('setting admin access denied',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name']})
        return render_template('access_denied.html',
                               info='You do not have access to settings, '
                                    'please contact the administrators.')
    logger.info('setting admin access denied',
                extra={'uid': session['uid'],
                       'en_name': session['en_name'],
                       'admins': request.form.getlist('admins[]')})
    Auth.set_admins(request.form.getlist('admins[]'))
    flash('Admins updated!', 'success')
    return jsonify({'success': True})
