import hashlib

from flask import Blueprint, render_template, flash, redirect, url_for, request, g, abort
from flask_login import login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.user.forms import LoginForm, SignupForm, SendForgotPasswordForm, ResetPasswordForm
from app.user.models import User
from app.user import constants as USER
from app.common.utils import generate_token, send_email


user_module = Blueprint('user', __name__)


@user_module.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)
        user.update_login_info(request.environ['REMOTE_ADDR'])
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('user/signup.html', form=form)


@user_module.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        user = User.query.filter_by(email=form.email.data).first()
        user.update_login_info(request.environ['REMOTE_ADDR'])
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Logged in successfully.')

        return redirect(request.args.get('next') or url_for('index'))
    return render_template('user/login.html', form=form)


@user_module.route('/logout')
@login_required
def logout():
    g.user.log_last_login(request.environ['REMOTE_ADDR'])
    db.session.add(g.user)
    db.session.commit()
    logout_user()

    return redirect(url_for('index'))


@user_module.route('/password/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = SendForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        token = user.reset_password_token.encode('base64').strip().replace('=', '_')
        send_email(
            'Framgia Code Contest - Reset Password',
            app.config['MAIL_SENDERS']['admin'],
            [user.email],
            'reset_password',
            dict(token=token)
        )

        user.log_sent_password_token()
        db.session.add(user)
        db.session.commit()

        return render_template('user/reset_password_sent.html', user=user)

    return render_template('user/forgot_password.html', form=form)


@user_module.route('/password/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        token = token.replace('_', '=').decode('base64')
    except Exception, e:
        abort(404)

    user = User.query.filter_by(reset_password_token=token).first()
    if not user:
        abort(404)
    elif not user.is_valid_token():
        user.refresh_password_token()
        db.session.add(user)
        db.session.commit()
        flash('Your token is expired ! Please request a new one.')

        return redirect(url_for('user.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        user.refresh_password_token()
        db.session.add(user)
        db.session.commit()
        flash('Password changed successfully.')

        return redirect(url_for('user.login'))

    return render_template('user/reset_password.html', form=form)


class UserView(ModelView):
    # Disable model creation
    can_create = False

    # Override displayed fields
    column_list = ('id', 'email', 'current_sign_in_at', 'current_sign_in_ip', 'last_sign_in_at', 'last_sign_in_ip', 'locale')
    column_filters = ('id', 'email', 'current_sign_in_at', 'current_sign_in_ip', 'last_sign_in_at', 'last_sign_in_ip', 'locale')

    form_excluded_columns = ('encrypted_password', 'submissions', 'scores')

    column_choices = {
        'locale': USER.LOCALES.items()
    }

    form_choices = {
        'locale': [(str(k), v) for k,v in USER.LOCALES.items()]
    }

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)

    def is_accessible(self):
        return g.user.is_authenticated() and g.user.is_admin()