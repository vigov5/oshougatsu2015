import urllib

from flask import g, Blueprint, render_template, redirect, url_for, request, session
from flask_admin.contrib.sqla import ModelView

from app import db
from app.common.tasks import run_code
from app.problem.models import Problem
from app.submission.models import Submission
from app.submission.forms import CreateSubmissionForm
from app.submission import constants as SUBMISSION
from app.problem import constants as PROBLEM


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

    if problem.category == PROBLEM.CATEGORY_GAME:
        return render_template('problem/show_game.html', problem=problem)

    if g.user and g.user.is_authenticated():
        my_submissions = g.user.submissions.filter_by(problem_id=problem.id).order_by(Submission.id.desc()).all()
    else:
        my_submissions = []

    old_code = ""
    old_mode = "clike"
    old_mime = "text/x-csrc"
    if g.user and 'c%d' % g.user.id in session and 'mode%d' % g.user.id and 'mime%d' % g.user.id in session:
        old_code = session['c%d' % g.user.id]
        old_mode = session['mode%d' % g.user.id]
        old_mime = session['mime%d' % g.user.id]

    form = CreateSubmissionForm(g.user, problem)
    if form.validate_on_submit():
        submission = Submission(form.problem_id.data, form.user_id.data, form.language.data)
        old_code = str(form.code.data).encode('string_escape')
        session['c%d' % g.user.id] = old_code
        session['mode%d' % g.user.id] = SUBMISSION.CODEMIRROR_MODES[int(form.language.data)]
        session['mime%d' % g.user.id] = SUBMISSION.CODEMIRROR_MIMES[int(form.language.data)]

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

    return render_template('problem/show_code.html', problem=problem, form=form, my_submissions=my_submissions, SUBMISSION=SUBMISSION, old_code=old_code, old_mime=old_mime, old_mode=old_mode)


class ProblemView(ModelView):

    column_default_sort = ('id', True)

    # Override displayed fields
    column_list = ('id', 'contest.name', 'category', 'name_en', 'name_vi', 'rank')

    column_choices = {
        'rank': PROBLEM.RANKS.items(),
        'category': PROBLEM.CATEGORIES.items()
    }

    form_excluded_columns = ('submissions', 'created_at', 'updated_at')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ProblemView, self).__init__(Problem, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
