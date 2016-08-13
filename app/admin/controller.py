from flask import Blueprint, flash, request, render_template, redirect, session, url_for

from .admin import Admin
from app.profile import Member


mod_admin = Blueprint('mod_admin', __name__, static_folder='../static')


@mod_admin.route('/overview', methods=['GET'])
def overview():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif 'en_name' not in session or 'position' not in 'session':
        current_user = Admin.get_member_by_uid(session['uid'])
        session['en_name'] = current_user.en_name
        session['position'] = current_user.position
        session['avatar_url'] = current_user.avatar_url
    return overview_members()


@mod_admin.route('/overview/members', methods=['GET'])
def overview_members():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    members = Admin.list_members()
    return render_template('overview_member.html', members=members)


@mod_admin.route('/overview/publications', methods=['GET'])
def overview_publications():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    publications = Admin.list_publications()
    return render_template('overview_publications.html',
                           publications=publications)


@mod_admin.route('/member/new', methods=['GET', 'POST'])
def add_member():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        return render_template(
            'access_denied.html',
            info='You do not have the authority to add a member, '
                 'please contact the administrator.'
        )
    if request.method == 'GET':
        supervisors = Admin.list_supervisors()
        return render_template('new_member.html', member=Member(),
                               supervisors=supervisors)
    else:
        if Admin.add_member(request.form):
            flash('Successfully added a new member!')
        else:
            flash('Failed to add a new member!')
        return redirect(url_for('mod_admin.overview'))


@mod_admin.route('/member/<int:uid>', methods=['GET', 'POST', 'DELETE'])
def view_member(uid):
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    if request.method == 'GET':
        member = Admin.get_member_by_uid(uid)
        supervisors = Admin.list_supervisors()
        return render_template('member.html', member=member,
                               supervisors=supervisors)
    elif request.method == 'POST':
        if Admin.update_member(uid, request.form):
            flash('Member info updated!')
        else:
            flash('Failed to update the member info!')
        return redirect(url_for('mod_admin.overview'))
    else:
        if Admin.delete_member(uid):
            flash('Successfully deleted a member!')
        else:
            flash('Failed to delete a member!')
        return ''


@mod_admin.route('/member/<int:uid>/publications', methods=['POST', 'DELETE'])
def add_publication(uid):
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        return render_template(
            'access_denied.html',
            info='You do not have the authority to add publications for '
                 'a member, please contact the administrator.'
        )
    member = Member.get_member_by_uid(uid)
    if request.method == 'POST':
        member.add_publication(request.form['new_pub'])
        return redirect(url_for('mod_admin.view_member', uid=uid))
    else:
        pass
