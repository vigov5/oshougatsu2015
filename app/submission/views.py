from flask import g, Blueprint, render_template, redirect, url_for
from flask_admin.contrib.sqla import ModelView

from app import db
from app.common.tasks import run_code
from app.submission.models import Submission
from app.submission import constants as SUBMISSION


submission_module = Blueprint('submission', __name__)

@submission_module.route('/<int:submission_id>', methods=['GET'])
def show(submission_id):
    submission = Submission.query.get_or_404(submission_id)

    return render_template('submission/show.html', submission=submission)


class SubmissionView(ModelView):

    column_default_sort = ('id', True)

    can_create = False

    column_list = ('id', 'problem_id', 'user_id', 'user.email', 'language',
        'state', 'result_status', 'last_passed_test_case',
        'used_time', 'used_memory', 'received_point', 'failed_test_case_result'
    )

    column_filters = ('id', 'problem_id', 'user_id', 'user.email', 'language',
        'state', 'result_status', 'last_passed_test_case',
        'used_time', 'used_memory', 'received_point', 'failed_test_case_result'
    )

    form_excluded_columns = ('problem', 'user', 'created_at', 'updated_at')

    column_choices = {
        'language': SUBMISSION.LANGUAGES.items(),
    }

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(SubmissionView, self).__init__(Submission, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()
