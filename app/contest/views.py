from flask import g, Blueprint, render_template
from flask.ext.admin.contrib.sqla import ModelView

from app.contest.models import Contest

contest_module = Blueprint('contest', __name__)


@contest_module.route('/<int:contest_id>')
def show(contest_id):
    contest = Contest.query.get_or_404(contest_id)
    return render_template('contest/show.html', contest=contest)

@contest_module.route('/<int:contest_id>/scores')
def scores(contest_id):
    contest = Contest.query.get_or_404(contest_id)
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