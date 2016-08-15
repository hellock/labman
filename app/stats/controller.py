from flask import Blueprint, jsonify, redirect, request, render_template, session, url_for

from . import Stats


mod_stats = Blueprint('mod_stats', __name__, static_folder='../static', url_prefix='/stats')


@mod_stats.route('/member', methods=['GET', 'POST'])
def member():
    if 'uid' not in session:
        return redirect(url_for('mod_auth.signin'))
    if request.method == 'GET':
        return render_template('stats_member.html')
    else:
        if request.form['stats_key'] == 'supervisor':
            data = Stats.by_supervisor()
        elif request.form['stats_key'] == 'admission_year':
            data = Stats.by_admission_year()
        return jsonify(data)
