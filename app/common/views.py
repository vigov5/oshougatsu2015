from flask import render_template, g, request, url_for, jsonify, redirect
from flask_login import current_user, login_required
import flask_menu as menu
from sqlalchemy import desc, asc

from app import app, lm
from app.user.models import User, UserJoin
from app.contest.models import Contest
from app.submission.models import Submission
from app.common.tasks import run_code
from app.common.utils import generate_random_string
from app.problem import constants as PROBLEM


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
@login_required
@menu.register_menu(app, '.index', 'Home', order=0)
def index():
    contest = Contest.query.order_by(Contest.id.desc()).first()
    return render_template(
        'index.html',
        contest=contest
    )


@app.route('/')
@app.route('/scoreboard')
def scoreboard():
    contest = Contest.query.order_by(Contest.id.desc()).first()
    if not contest:
        return redirect(url_for('index'))
    activities = Submission.query.order_by(desc(Submission.created_at)).all()

    joins = UserJoin.query.filter_by(contest_id=contest.id).all()
    raw = []
    for join in joins:
        raw.append((join.user, join.user.get_total_score()))

    return render_template(
        'scoreboard.html',
        activities=activities,
        raw=raw
    )

@app.route('/howto')
@menu.register_menu(app, '.howto', 'How to', order=2)
def howto():
    return render_template('howto.html')

@app.route('/admin')
def admin():
    contests = Contest.query.order_by(Contest.id.desc()).all()
    return render_template(
        'admin.html',
        contests=contests
    )


@app.route('/activities/more', methods=['POST'])
def more_activities():
    last_side = request.form.get('side', 'left')
    last_id = request.form.get('id')
    activities = Submission.query.filter(Submission.id >= last_id).order_by(desc(Submission.created_at)).limit(2).all()
    resp = []
    for activity in activities:
        last_side = 'right' if last_side == 'left' else 'left'
        element = {
            'class': 'pos-%s clearfix' % last_side,
            'id': activity.id,
            'time': activity.created_at.strftime('%b %d %H:%M'),
            'header': u"%s" % activity.user.email
        }

        element['result'] = u'/static/images/running.gif'

        if activity.problem.category == PROBLEM.CATEGORY_CODE:
            if int(activity.id) == int(last_id):
                element['type'] = 'update'
            else:
                element['type'] = 'new'

            if activity.is_finished():
                if activity.is_accepted():
                    element['footer'] = u' solved <a href="{0:s}">{1:s}</a> and scored <strong>{2:s} points</strong>'.format(url_for('problem.show', problem_id=activity.problem.id), activity.problem.name_en, str(activity.received_point))
                    element['result'] = u'/static/images/true.png'
                else:
                    element['footer'] = u' failed to solve <a href="{0:s}">{1:s}</a>'.format(url_for('problem.show', problem_id=activity.problem.id), activity.problem.name_en)
                    element['result'] = u'/static/images/false.png'
            else:
                element['footer'] = u' submitted solution for <a href="{0:s}">{1:s}</a>'.format(url_for('problem.show', problem_id=activity.problem.id), activity.problem.name_en)

        else:
            element['type'] = 'update'
            element['result'] = u'/static/images/true.png'
            if int(activity.id) != int(last_id):
                element['type'] = 'new'
                element['footer'] = u' solved <a href="{0:s}">{1:s}</a> and scored <strong>{2:s} points</strong>'.format(url_for('problem.show', problem_id=activity.problem.id), activity.problem.name_en, str(activity.received_point))

        resp.append(element)

    contest = Contest.query.order_by(Contest.id.desc()).first()
    joins = UserJoin.query.filter_by(contest_id=contest.id).all()
    for join in joins:
        resp.append({
            'type': 'point',
            'user_id': join.user.id,
            'point': join.user.get_total_score()
        })

    return jsonify(result=resp)