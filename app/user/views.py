import hashlib

from flask import Blueprint, render_template, flash, redirect, url_for, request, g, abort
from flask_login import login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView

from app import app, db
from app.user.forms import LoginForm, SignupForm, SendForgotPasswordForm
from app.user.models import User
from app.common.utils import generate_token


user_module = Blueprint('user', __name__)


@user_module.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)

        db.session.add(new_user)
        db.session.commit()

        return render_template('confirm_mail_sent.html', user=new_user)

    return render_template('user/signup.html', form=form)


@user_module.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Logged in successfully.')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('user/login.html', form=form)


@user_module.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@user_module.route('/profile', methods=['GET', 'POST'])
@user_module.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id=None):
    if g.user is not None and g.user.is_authenticated():
        if user_id is None:
            return render_template('user/profile.html', user=g.user)
        else:
            user = User.query.get(user_id)
            if user:
                return render_template('user/profile.html', user=user)
            else:
                return redirect(url_for('index'))
    else:
        if user_id is None:
            return redirect(url_for('index'))
        else:
            user = User.query.get(user_id)
            return render_template('user/profile.html', user=user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    model = User.query.get(g.user.id)
    form = UserForm(obj=model)

    if form.validate_on_submit():
        form.populate_obj(model)
        db.session.add(model)
        db.session.commit()
        flash('Profile updated', category='success')
        return redirect(url_for('profile'))

    return render_template('user/edit_profile.html', user=g.user, form=form)


@user_module.route('/password/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = SendForgotPasswordForm()
    '''
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user_forgot_password = UserForgotPassword.query.filter_by(user_id=user.id).first()
        if not user_forgot_password:
            user_forgot_password = UserForgotPassword(user)
        else:
            user_forgot_password.refresh()
        db.session.add(user_forgot_password)
        db.session.commit()

        token = user_forgot_password.token.encode('base64').strip().replace('=', '_')
        send_email(
            'Heasygame - Reset Password',
            app.config['MAIL_SENDERS']['admin'],
            [user.email],
            'reset_password',
            dict(token=token)
        )
        return render_template('user/reset_password_sent.html', user=user)
    '''
    return render_template('user/forgot_password.html', form=form)


@user_module.route('/password/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        token = token.replace('_', '=').decode('base64')
    except Exception, e:
        abort(404)
    '''
    user_forgot_password = UserForgotPassword.query.filter_by(token=token).get_or_404()

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_forgot_password.user.set_password(form.new_password.data)
        user_forgot_password.refresh()
        db.session.add(user_forgot_password)
        db.session.commit()
        flash('Password changed successfully.')
        return redirect(url_for('user.login'))
    '''
    #return render_template('user/reset_password.html', form=form)
