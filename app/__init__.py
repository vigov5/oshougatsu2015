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
from app.user.views import user_module

admin = Admin(app, url='/admin')
app.register_blueprint(user_module, url_prefix='/user')
