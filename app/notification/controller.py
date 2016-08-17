from flask import Blueprint, redirect, render_template, session, url_for

from app.utils import get_logger


mod_notification = Blueprint('mod_notification', __name__, static_folder='../static',
                             url_prefix='/notification')

logger = get_logger(__name__)


@mod_notification.route('/all', methods=['GET'])
def all():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    logger.info('/notification/all',
                extra={'uid': session['uid'],
                       'en_name': session['en_name']})
    return render_template('notification.html')
