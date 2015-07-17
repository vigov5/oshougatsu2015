from flask import render_template, g
from flask_login import current_user
import flask_menu as menu

from app import app, lm
from app.user.models import User
from app.contest.models import Contest
from app.submission.models import Submission
from app.common.tasks import run_code
from app.common.utils import generate_random_string


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
@menu.register_menu(app, '.index', 'Home', order=0)
def index():
    contests = Contest.query.order_by(Contest.id.desc()).all()
    return render_template(
        'index.html',
        contests=contests
    )


@app.route('/')
@app.route('/scoreboard')
@menu.register_menu(app, '.scoreboard', 'Score Board', order=1)
def scoreboard():
    users = User.query.all()
    raw = {}
    for user in users:
        for submission in user.submissions:
            if submission.is_accepted():
                if not raw.has_key(submission.user.email):
                    raw[submission.user.email] = 0
                raw[submission.user.email] += submission.received_point

    summary = [(email, total_score) for email, total_score in raw.items()]
    summary = sorted(summary, key=lambda x: x[1], reverse=True)
    max_score = summary[0][1]

    return render_template(
        'scoreboard.html',
        max_score=max_score,
        summary=summary
    )

@app.route('/howto')
@menu.register_menu(app, '.howto', 'How to', order=2)
def howto():
    return render_template('howto.html')