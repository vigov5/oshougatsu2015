from flask_wtf import Form
from wtforms import TextField, SubmitField, validators, PasswordField
from models import User

class SignupForm(Form):
    username = TextField('Username',  [
        validators.Required('Please enter your username.'),
        validators.Length(max=30, message='Username is at most 30 characters.'),
    ])
    email = TextField('Email',  [
        validators.Length(max=40, message='email is at most 40 characters.'),
        validators.Required('Please enter your email address.'),
        validators.Email('Please enter your email address.')
    ])
    password = PasswordField('Password', [
        validators.Required('Please enter a password.'),
        validators.Length(min=6, message='Passwords is at least 6 characters.'),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Create account')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('That username is already taken.')
            return False

        email = User.query.filter_by(email=self.email.data).first()
        if email:
            self.email.errors.append('That email is already taken.')
            return False

        return True


class LoginForm(Form):
    username = TextField('Username',  [
        validators.Required('Please enter your username.'),
        validators.Length(max=30, message='Username is at most 30 characters.'),
    ])
    password = PasswordField('Password', [
        validators.Required('Please enter a password.'),
        validators.Length(min=6, message='Passwords is at least 6 characters.'),
    ])
    submit = SubmitField('Sign In')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username = self.username.data).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.password.errors.append('Invalid e-mail or password')
            return False
