from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask.ext.bcrypt import Bcrypt
import flask_menu as menu
from celery import Celery
from flaskext.uploads import UploadSet, configure_uploads, patch_request_class

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

mail = Mail(app)

menu.Menu(app=app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

celery = make_celery(app)

bcrypt = Bcrypt(app)

code_upload_set = UploadSet('code', extensions=app.config['UPLOADED_FILES_ALLOW'])
configure_uploads(app, code_upload_set)
patch_request_class(app, 2 * 1024 * 1024) # 2MB

app.jinja_env.add_extension('jinja2.ext.do')

from app.common import views
from app.user.views import user_module, UserView
from app.contest.views import contest_module, ContestView
from app.problem.views import problem_module, ProblemView
from app.hint.views import HintView
from app.submission.views import submission_module, SubmissionView
from app.api.v1.views import api_v1_module

app.register_blueprint(user_module, url_prefix='/user')
app.register_blueprint(contest_module, url_prefix='/contest')
app.register_blueprint(problem_module, url_prefix='/problem')
app.register_blueprint(submission_module, url_prefix='/submission')
app.register_blueprint(api_v1_module, url_prefix='/api/v1')

admin = Admin(app, url='/admin')
admin.add_view(UserView(db.session, name='Users'))
admin.add_view(ContestView(db.session, name='Contests'))
admin.add_view(ProblemView(db.session, name='Problems'))
admin.add_view(HintView(db.session, name='Hints'))
admin.add_view(SubmissionView(db.session, name='Submissions'))
