from flask import render_template, g
from flask_login import current_user
import flask_menu as menu

from app import app, lm
from app.user.models import User
from app.contest.models import Contest


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
