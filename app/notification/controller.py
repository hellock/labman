from flask import Blueprint, redirect, render_template, session, url_for


mod_notification = Blueprint('mod_notification', __name__, static_folder='../static',
                             url_prefix='/notification')


@mod_notification.route('/all', methods=['GET'])
def all():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    return render_template('notification.html')
