from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from .member import Member
from app.auth import Auth
from app.utils import get_logger


mod_member = Blueprint('mod_member', __name__, static_folder='../static')

logger = get_logger(__name__)


@mod_member.route('/profile', strict_slashes=False, methods=['GET', 'POST'])
def profile():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_by_uid(session['uid'])
    if request.method == 'GET':
        logger.info('/profile',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name']})
        supervisors = Member.list('Professor')
        return render_template('profile.html', member=member,
                               supervisors=supervisors)
    elif request.method == 'POST':
        if member.update(request.form):
            flash('Profile updated!', 'success')
            logger.info('profile update success',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name'],
                               'form': request.form})
        else:
            flash('Failed to update your profile!', 'error')
            logger.error('profile update failure',
                         extra={'uid': session['uid'],
                                'en_name': session['en_name'],
                                'form': request.form})
        return redirect(url_for('mod_overview.index'))


@mod_member.route('/profile/publications', methods=['POST', 'DELETE'])
def manage_self_publication():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_by_uid(session['uid'])
    if request.method == 'POST':
        logger.info('add publication',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name'],
                           'form': request.form})
        member.add_publication(request.form)
        return redirect(url_for('mod_member.profile'))
    else:
        logger.info('delete publication',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name'],
                           'form': request.form})
        pass
        # TODO: implement delete operation


@mod_member.route('/profile/avatar', methods=['POST'])
def avatar():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    member = Member.get_by_uid(session['uid'])
    if 'file' in request.files:
        url = member.change_avatar(request.files['file'])
        session['avatar_url'] = url
        logger.info('change avatar',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name'],
                           'avatar_url': url})
        return jsonify({'avatar_url': url})


@mod_member.route('/member/search', methods=['GET'])
def search():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    members = Member.search(request.args.get('q', ''))
    if members:
        result_list = []
        for position in members:
            for member in members[position]:
                result_list.append({'uid': member.uid, 'en_name': member.en_name})
        logger.info(
            'search members',
            extra={'uid': session['uid'],
                   'en_name': session['en_name'],
                   'q': request.args.get('q', ''),
                   'result': result_list}
        )
        return render_template('overview_member.html', members=members)
    else:
        flash('No result found!', 'warning')
        logger.info('search members',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name'],
                           'q': request.args.get('q', ''),
                           'result': ''})
        return render_template('overview_member.html')


@mod_member.route('/member/new', methods=['GET', 'POST'])
def add_member():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        logger.info('add member access denied',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name']})
        return render_template(
            'access_denied.html',
            info='You do not have access to adding members, '
                 'please contact the administrators.'
        )
    if request.method == 'GET':
        logger.info('/member/new',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name']})
        supervisors = Member.list('Professor')
        return render_template('new_member.html', member=Member(),
                               supervisors=supervisors)
    else:
        member = Member.new(request.form)
        if member:
            if member.position == 'Professor':
                auth_level = 'admin'
            else:
                auth_level = 'memebr'
            username = member.en_name.replace(' ', '').lower()
            username = Auth.add_new_user(member.uid, username,
                                         auth_level=auth_level)
            flash('Successfully added a new member, username is ' + username,
                  'success')
            logger.info('add member success',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name'],
                               'form': request.form,
                               'username': username,
                               'auth_level': auth_level})
        else:
            flash('Failed to add a new member!', 'error')
            logger.error('add member failure',
                         extra={'uid': session['uid'],
                                'en_name': session['en_name'],
                                'form': request.form})
        return redirect(url_for('mod_overview.index'))


@mod_member.route('/member/<int:uid>', methods=['GET', 'POST', 'DELETE'])
def member(uid):
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    if request.method == 'GET':
        member = Member.get_by_uid(uid)
        if member.state == 'Candidate' and session['auth_level'] != 'admin':
            logger.info('view candidate access denied',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name'],
                               'member_uid': uid})
            return render_template(
                'access_denied.html',
                info='You do not have access to this member page, '
                     'please contact the administrators.'
            )
        logger.info('/member/' + str(uid),
                    extra={'uid': session['uid'],
                           'en_name': session['en_name'],
                           'member_uid': uid,
                           'member_name': member.en_name})
        supervisors = Member.list('Professor')
        return render_template('member.html', member=member,
                               supervisors=supervisors)
    elif request.method == 'POST':
        if session['auth_level'] != 'admin':
            logger.info('update member access denied',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name'],
                               'member_uid': uid,
                               'form': request.form})
            return render_template(
                'access_denied.html',
                info='You do not have access to updating other members\' '
                     'profiles, please contact the administrators'
            )
        member = Member.get_by_uid(uid)
        if member.update(request.form):
            flash('Member info updated!', 'success')
            logger.info('update member success',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name'],
                               'member_uid': uid,
                               'form': request.form})
        else:
            flash('Failed to update the member info!', 'error')
            logger.error('update member failure',
                         extra={'uid': session['uid'],
                                'en_name': session['en_name'],
                                'member_uid': uid,
                                'form': request.form})
        return redirect(
            url_for('mod_overview.members', state=member.state.lower()))
    else:
        if session['auth_level'] != 'admin':
            logger.info('delete member access denied',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name'],
                               'member_uid': uid})
            return render_template(
                'access_denied.html',
                info='You do not have access to deleting members, '
                     'please contact the administrators.'
            )
        if Member.delete(uid):
            logger.info('delete member success',
                        extra={'uid': session['uid'],
                               'en_name': session['en_name'],
                               'member_uid': uid})
            Auth.del_user(uid)
            flash('Successfully deleted a member!', 'success')
        else:
            flash('Failed to delete a member!', 'error')
            logger.error('delete member failure',
                         extra={'uid': session['uid'],
                                'en_name': session['en_name'],
                                'member_uid': uid})
        return jsonify({'success': True})


@mod_member.route('/member/<int:uid>/publications', methods=['POST', 'DELETE'])
def manage_publication(uid):
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    elif session['auth_level'] != 'admin':
        logger.error('add member publication access denied',
                     extra={'uid': session['uid'],
                            'en_name': session['en_name'],
                            'member_uid': uid})
        return render_template(
            'access_denied.html',
            info='You do not have access to adding publications for '
                 'other members, please contact the administrators.'
        )
    member = Member.get_by_uid(uid)
    if request.method == 'POST':
        logger.info('add member publication',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name'],
                           'member_uid': uid,
                           'form': request.form})
        member.add_publication(request.form)
        return redirect(url_for('mod_member.member', uid=uid))
    else:
        logger.info('delete member publication',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name'],
                           'member_uid': uid,
                           'form': request.form})
        pass


@mod_member.route('/member/<int:uid>/comments', methods=['GET', 'POST'])
def comments(uid):
    if 'uid' not in session:
        return jsonify({'success': False, 'msg': 'Please signin first.'})
    if request.method == 'GET':
        logger.debug('get comment api',
                     extra={'uid': session['uid'],
                            'en_name': session['en_name'],
                            'member_uid': uid})
        return jsonify(Member.get_comments(uid))
    elif request.method == 'POST':
        logger.info('add comment',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name'],
                           'member_uid': uid,
                           'form': request.form})
        member = Member.get_by_uid(session['uid'])
        comment = member.add_comment_to(uid, request.form['comment'])
        return jsonify(comment)
