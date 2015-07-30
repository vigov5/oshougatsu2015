from flask import g, Blueprint, render_template, redirect, url_for
from flask_admin.contrib.sqla import ModelView

from app import db
from app.common.tasks import run_code
from app.problem.models import Problem
from app.submission.models import Submission
from app.submission.forms import CreateSubmissionForm
from app.submission import constants as SUBMISSION


problem_module = Blueprint('problem', __name__)


@problem_module.route('/<int:problem_id>', methods=['GET', 'POST'])
def show(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    if not problem.contest.is_started():
        if g.user.is_authenticated():
            if not g.user.is_admin():
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))

    if g.user and g.user.is_authenticated():
        my_submissions = g.user.submissions.filter_by(problem_id=problem.id).order_by(Submission.id.desc()).all()
    else:
        my_submissions = []

    form = CreateSubmissionForm(g.user, problem)
    if form.validate_on_submit():
        submission = Submission(form.problem_id.data, form.user_id.data, form.language.data)
        submission.state = SUBMISSION.STATE_QUEUED
        db.session.add(submission)
        db.session.commit()
        if submission.save_source_code(form.code.data):
            run_code.delay(problem.id, submission.id, submission.get_source_name_with_prefix(), submission.get_target_name(), submission.get_language_mapping())
            db.session.add(submission)
            db.session.commit()
        else:
            form.code.errors.append("Can't save source code file")
        return redirect(url_for('problem.show', problem_id=problem.id))

    return render_template('problem/show.html', problem=problem, form=form, my_submissions=my_submissions)


class ProblemView(ModelView):

    column_default_sort = ('id', True)

    # Override displayed fields
    column_list = ('id', 'contest.name', 'name_en', 'name_vi', 'rank')

    form_excluded_columns = ('submissions', 'created_at', 'updated_at')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ProblemView, self).__init__(Problem, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
