from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask.ext.bcrypt import Bcrypt
import flask_menu as menu

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

mail = Mail(app)

menu.Menu(app=app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

bcrypt = Bcrypt(app)

from app.common import views
from app.user.views import user_module, UserView
from app.contest.views import contest_module, ContestView
from app.problem.views import ProblemView

app.register_blueprint(user_module, url_prefix='/user')
app.register_blueprint(contest_module, url_prefix='/contest')

admin = Admin(app, url='/admin')
admin.add_view(UserView(db.session, name='Users'))
admin.add_view(ContestView(db.session, name='Contests'))
admin.add_view(ProblemView(db.session, name='Problems'))
