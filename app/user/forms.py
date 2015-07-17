from flask_wtf import Form
from wtforms import TextField, SubmitField, validators, PasswordField
from wtforms_alchemy import model_form_factory

from app.user.models import User


ModelForm = model_form_factory(Form)


class SignupForm(Form):
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

        email = User.query.filter_by(email=self.email.data).first()
        if email:
            self.email.errors.append('That email is already taken.')
            return False

        return True


class LoginForm(Form):
    email = TextField('Email',  [
        validators.Length(max=40, message='email is at most 40 characters.'),
        validators.Required('Please enter your email address.'),
        validators.Email('Please enter your email address.')
    ])
    password = PasswordField('Password', [
        validators.Required('Please enter a password.'),
        validators.Length(min=6, message='Passwords is at least 6 characters.'),
    ])
    submit = SubmitField('Login In')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data).first()
        if user:
            if not user.check_password(self.password.data):
                self.password.errors.append('Wrong password')
                return False
            else:
                return True
        else:
            self.password.errors.append('Invalid e-mail or password')
            return False


class ResendMailForm(Form):
    email = TextField('Email',  [
        validators.Length(max=40, message='email is at most 40 characters.'),
        validators.Required('Please enter your email address.'),
        validators.Email('Please enter a valid email address.')
    ])
    submit = SubmitField('Resend Activation Email')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('This email is not registered yet')
            return False
        else:
            return True


class SendForgotPasswordForm(Form):
    email = TextField('Email',  [
        validators.Length(max=40, message='email is at most 40 characters.'),
        validators.Required('Please enter your email address.'),
        validators.Email('Please enter a valid email address.')
    ])
    submit = SubmitField('Send Forgot Password Email')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('This email is not registered yet')
            return False
        else:
            return True


class ResetPasswordForm(Form):
    new_password = PasswordField('Password', [
        validators.Required('Please enter new password.'),
        validators.Length(min=6, message='Passwords is at least 6 characters.'),
        validators.EqualTo('new_confirm', message='Passwords must match')
    ])
    new_confirm = PasswordField('Repeat Password')
    submit = SubmitField('Reset password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        return True


class ChangePasswordForm(Form):
    new_password = PasswordField('Password', [
        validators.Required('Please enter new password.'),
        validators.Length(min=6, message='Passwords is at least 6 characters.'),
        validators.EqualTo('new_confirm', message='Passwords must match')
    ])
    new_confirm = PasswordField('Repeat Password')
    submit = SubmitField('Change password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        return True