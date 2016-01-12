from flask_wtf import Form
from wtforms import validators, SubmitField, SelectField, HiddenField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import TextArea

from app import code_upload_set
from app.user.models import User
from app.submission.models import Submission
from app.submission import constants as SUBMISSION


class CreateSubmissionForm(Form):
    user_id = HiddenField('user_id')
    problem_id = HiddenField('problem_id')
    submit = SubmitField('Submit')
    language = SelectField('Language', choices=[(str(k), v) for k, v in SUBMISSION.LANGUAGES.items()])
    code = TextAreaField('Code', widget=TextArea())


    def __init__(self, current_user, current_problem, *args, **kwargs):
        if current_user.is_authenticated():
            self.current_user_id = current_user.id
        else:
            self.current_user_id = None
        self.current_problem_id = current_problem.id
        Form.__init__(self, *args, **kwargs)


    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.get(self.user_id.data)
        if not user or user.id != self.current_user_id:
            self.user_id.errors.append('Invalid user')
            return False
        else:
            return True

        problem = Problem.query.get(self.problem_id.data)
        if not problem or problem.id != self.current_problem_id:
            self.problem_id.errors.append('Invalid problem')
            return False
        else:
            return True