from flask import abort, Blueprint, render_template, redirect, session, url_for

from app.member import Member


mod_overview = Blueprint('mod_overview', __name__, static_folder='../static',
                         url_prefix='/overview')


@mod_overview.route('/', methods=['GET'])
@mod_overview.route('/members', strict_slashes=False, methods=['GET'])
def index():
    return members('present')


@mod_overview.route('/members/<string:state>', methods=['GET'])
def members(state='present'):
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif state not in ['present', 'alumni', 'candidate']:
        abort(404)
    elif 'en_name' not in session or 'position' not in 'session':
        current_user = Member.get_by_uid(session['uid'])
        session['en_name'] = current_user.en_name
        session['position'] = current_user.position
        session['avatar_url'] = current_user.avatar_url
    members = Member.list_all(state[0].upper() + state[1:])
    supervisor_urls = {}
    supervisor_list = Member.list('Professor')
    for supervisor in supervisor_list:
        supervisor_urls[supervisor.en_name] = '/member/' + str(supervisor.uid)
    return render_template('overview_member.html',
                           members=members, supervisor_urls=supervisor_urls)


@mod_overview.route('/publications', methods=['GET'])
def publications():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    publications = Member.list_publications()
    return render_template('overview_publications.html',
                           publications=publications)


@mod_overview.route('/stats', methods=['GET'])
def stats():
    return redirect(url_for('mod_stats.member'))
