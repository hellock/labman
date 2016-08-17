from flask import Blueprint, jsonify, redirect, request, render_template, session, url_for

from . import Stats
from app.utils import get_logger


mod_stats = Blueprint('mod_stats', __name__, static_folder='../static',
                      url_prefix='/stats')

logger = get_logger(__name__)


@mod_stats.route('/member', methods=['GET', 'POST'])
def member():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    if request.method == 'GET':
        logger.info('/stats/member',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name']})
        return render_template('stats_member.html')
    else:
        if request.form['stats_key'] == 'supervisor':
            data = Stats.by_supervisor()
        elif request.form['stats_key'] == 'admission_year':
            data = Stats.by_admission_year()
        logger.debug('member stats api',
                     extra={'uid': session['uid'],
                            'en_name': session['en_name'],
                            'form': request.form,
                            'ret': data})
        return jsonify(data)


@mod_stats.route('/publication', methods=['GET', 'POST'])
def publication():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    if request.method == 'GET':
        logger.info('/stats/publication',
                    extra={'uid': session['uid'],
                           'en_name': session['en_name']})
        return render_template('stats_publication.html')
    else:
        if request.form['stats_key'] == 'year':
            data = Stats.pubs_by_year()
        logger.debug('publication stats api',
                     extra={'uid': session['uid'],
                            'en_name': session['en_name'],
                            'form': request.form,
                            'ret': data})
        return jsonify(data)
