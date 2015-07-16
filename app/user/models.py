import datetime

from app import app, db, bcrypt
from app.common.utils import generate_token
from app.user import constants as USER
from app.submission.models import Submission
from app.user_score.models import UserScore


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
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    locale = db.Column(db.SmallInteger, default=USER.LOCALE_VN)

    submissions = db.relationship(Submission, backref='user', lazy='dynamic')
    scores = db.relationship(UserScore, backref='user', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email.lower()
        self.set_password(password)
        self.reset_password_token = generate_token()
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
        return '<User %r>' % self.email

    def is_admin(self):
        return self.email in app.config['ADMINS']

    def update_login_info(self, remote_ip):
        if not self.sign_in_count:
            self.sign_in_count = 0
        self.sign_in_count += 1
        self.current_sign_in_at = datetime.datetime.now()
        self.current_sign_in_ip = remote_ip

    def log_last_login(self, remote_ip):
        self.last_sign_in_at = datetime.datetime.now()
        self.last_sign_in_ip = remote_ip

    def log_sent_password_token(self):
        self.reset_password_sent_at = datetime.datetime.now()

    def refresh_password_token(self):
        self.reset_password_token = generate_token()

    def is_valid_token(self):
        return self.reset_password_sent_at + datetime.timedelta(minutes=USER.TOKEN_EXPIRE_MINUTES) > datetime.datetime.now()

    def is_locale_vn(self):
        return self.locale == USER.LOCALE_VN

    def is_locale_en(self):
        return self.locale == USER.LOCALE_EN

    def  get_locale_text(self):
        return USER.LOCALES[self.locale]


class UserForgotPassword(db.Model):

    __tablename__ = 'user_forgot_passwords'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    token = db.Column(db.String(40))
    expire_at = db.Column(db.DateTime, default=datetime.datetime.now() + datetime.timedelta(minutes=30))

    user = db.relationship('User', backref=db.backref('forgot_password', lazy='dynamic', cascade='all'))

    def __init__(self, user):
        self.user = user
        self.token = generate_token()

    def refresh(self):
        self.token = generate_token()
        self.expire_at = datetime.datetime.now() + datetime.timedelta(minutes=30)

    def is_expired(self):
        return datetime.datetime.now() >= self.expire_at
