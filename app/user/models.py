import datetime

from app import app, db, bcrypt
from app.common.utils import generate_token
from app.user import constants as USER


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, default='')
    encrypted_password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(255), unique=True, default='')
    reset_password_sent_at = db.Column(db.DateTime)
    remember_created_at = db.Column(db.DateTime)
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(db.DateTime)
    last_sign_in_at = db.Column(db.DateTime)
    current_sign_in_ip = db.Column(db.String(255), default='')
    last_sign_in_ip = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime)
    locale = db.Column(db.SmallInteger, default=USER.LOCALE_VN)

    def __init__(self, email, password):
        self.email = email.lower()
        self.set_password(password)
        self.updated_at = datetime.datetime.now()

    def set_password(self, password):
        self.encrypted_password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_admin(self):
        return True