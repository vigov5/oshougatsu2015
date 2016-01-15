import random
import datetime

from flask import g, Blueprint, render_template, redirect, url_for, flash
from flask.ext.admin.contrib.sqla import ModelView

from app import db
from app.contest.models import Contest
from app.problem.models import Problem
from app.submission.models import Submission
from app.problem import constants as PROBLEM

contest_module = Blueprint('contest', __name__)


@contest_module.route('/<int:contest_id>')
def show(contest_id):
    contest = Contest.query.get_or_404(contest_id)
    return render_template('contest/show.html', contest=contest)


@contest_module.route('/<int:contest_id>/scores')
def scores(contest_id):
    raw = {}
    for problem in contest.problems:
        for submission in problem.submissions:
            if submission.is_accepted():
                if not raw.has_key(submission.user.email):
                    raw[submission.user.email] = {}
                raw[submission.user.email][problem.id] = submission.received_point
    summary = [(email, points, sum(points.values())) for email, points in raw.items()]
    summary = sorted(summary, key=lambda x: x[2], reverse=True)

    return render_template('contest/scores.html', contest=contest, summary=summary)


@contest_module.route('/generate')
def generate():
    last_contest = Contest.query.order_by(Contest.id.desc()).first()
    new_id = 1
    if last_contest:
        new_id = last_contest.id + 1
    contest = Contest('New Year Contest %d' % new_id, 'Contest for HUST Oshougatsu 2015')

    Submission.query.delete()
    db.session.add(contest);
    db.session.commit();
    a = random.choice(Problem.query.filter_by(rank=PROBLEM.RANK_EASY, category=PROBLEM.CATEGORY_CODE).all())
    b = random.choice(Problem.query.filter_by(rank=PROBLEM.RANK_HARD, category=PROBLEM.CATEGORY_CODE).all())
    c = random.choice(Problem.query.filter_by(rank=PROBLEM.RANK_EASY, category=PROBLEM.CATEGORY_GAME).all())
    d = random.choice(Problem.query.filter_by(rank=PROBLEM.RANK_HARD, category=PROBLEM.CATEGORY_GAME).all())
    a.contest = contest
    b.contest = contest
    c.contest = contest
    d.contest = contest
    db.session.add(a)
    db.session.add(b)
    db.session.add(c)
    db.session.add(d)
    db.session.commit()
    flash('Generate contest successfully', category='success')

    return redirect(url_for('admin'))


@contest_module.route('/<int:contest_id>/start')
def start_now(contest_id):
    contest = Contest.query.get_or_404(contest_id)
    contest.change_start_time(datetime.datetime.now())
    db.session.add(contest)
    db.session.commit()
    flash('Contest started', category='success')

    return redirect(url_for('admin'))

@contest_module.route('/<int:contest_id>/end')
def end_now(contest_id):
    contest = Contest.query.get_or_404(contest_id)
    contest.change_end_time(datetime.datetime.now())
    db.session.add(contest)
    db.session.commit()
    flash('Contest ended', category='success')

    return redirect(url_for('admin'))

class ContestView(ModelView):

    column_default_sort = ('id', True)

    # Override displayed fields
    column_list = ('name', 'description', 'start_at', 'end_at', 'result_announced_at')
    column_filters = ('name', 'description', 'start_at', 'end_at', 'result_announced_at')

    form_excluded_columns = ('problems', 'scores', 'created_at', 'updated_at')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ContestView, self).__init__(Contest, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
