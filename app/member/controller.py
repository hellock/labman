from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from .member import Member
from app.auth import Auth


mod_member = Blueprint('mod_member', __name__, static_folder='../static')


@mod_member.route('/profile', strict_slashes=False, methods=['GET', 'POST'])
def profile():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_by_uid(session['uid'])
    if request.method == 'GET':
        supervisors = Member.list('Professor')
        return render_template('profile.html', member=member,
                               supervisors=supervisors)
    elif request.method == 'POST':
        if member.update(request.form):
            flash('Profile updated!', 'success')
        else:
            flash('Failed to update your profile!', 'error')
        return redirect(url_for('mod_overview.index'))


@mod_member.route('/profile/publications', methods=['POST', 'DELETE'])
def manage_self_publication():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_by_uid(session['uid'])
    if request.method == 'POST':
        member.add_publication(request.form)
        return redirect(url_for('mod_member.profile'))
    else:
        pass


@mod_member.route('/profile/avatar', methods=['POST'])
def avatar():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_by_uid(session['uid'])
    if 'file' in request.files:
        url = member.change_avatar(request.files['file'])
        return jsonify({'avatar_url': url})


@mod_member.route('/member/search', methods=['GET'])
def search():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    members = Member.search(request.args.get('q', ''))
    if members:
        return render_template('overview_member.html', members=members)
    else:
        flash('No result found!', 'warning')
        return render_template('overview_member.html')


@mod_member.route('/member/new', methods=['GET', 'POST'])
def add_member():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        return render_template(
            'access_denied.html',
            info='You do not have access to adding members, '
                 'please contact the administrators.'
        )
    if request.method == 'GET':
        supervisors = Member.list('Professor')
        return render_template('new_member.html', member=Member(),
                               supervisors=supervisors)
    else:
        member = Member.new(request.form)
        if member:
            username = member.en_name.replace(' ', '').lower()
            username = Auth.add_new_user(member.uid, username)
            flash('Successfully added a new member, username is ' + username,
                  'success')
        else:
            flash('Failed to add a new member!', 'error')
        return redirect(url_for('mod_overview.index'))


@mod_member.route('/member/<int:uid>', methods=['GET', 'POST', 'DELETE'])
def member(uid):
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    if request.method == 'GET':
        member = Member.get_by_uid(uid)
        if member.state == 'Candidate' and session['auth_level'] != 'admin':
            return render_template(
                'access_denied.html',
                info='You do not have access to this member page, '
                     'please contact the administrators.'
            )
        supervisors = Member.list('Professor')
        return render_template('member.html', member=member,
                               supervisors=supervisors)
    elif request.method == 'POST':
        if session['auth_level'] != 'admin':
            return render_template(
                'access_denied.html',
                info='You do not have access to updating other members\' '
                     'profiles, please contact the administrators'
            )
        member = Member.get_by_uid(uid)
        if member.update(request.form):
            flash('Member info updated!', 'success')
        else:
            flash('Failed to update the member info!', 'error')
        return redirect(
            url_for('mod_overview.members', state=member.state.lower()))
    else:
        if session['auth_level'] != 'admin':
            return render_template(
                'access_denied.html',
                info='You do not have access to deleting members, '
                     'please contact the administrators.'
            )
        if Member.delete(uid):
            Auth.del_user(uid)
            flash('Successfully deleted a member!', 'success')
        else:
            flash('Failed to delete a member!', 'error')
        return ''


@mod_member.route('/member/<int:uid>/publications', methods=['POST', 'DELETE'])
def manage_publication(uid):
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        return render_template(
            'access_denied.html',
            info='You do not have access to adding publications for '
                 'other members, please contact the administrators.'
        )
    member = Member.get_by_uid(uid)
    if request.method == 'POST':
        member.add_publication(request.form)
        return redirect(url_for('mod_member.member', uid=uid))
    else:
        pass


@mod_member.route('/member/<int:uid>/comments', methods=['GET', 'POST'])
def comments(uid):
    if 'uid' not in session:
        return jsonify({'success': False, 'msg': 'Please signin first.'})
    if request.method == 'GET':
        return jsonify(Member.get_comments(uid))
    elif request.method == 'POST':
        member = Member.get_by_uid(session['uid'])
        comment = member.add_comment_to(uid, request.form['comment'])
        return jsonify(comment)
