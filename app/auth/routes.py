# type: ignore

"""
Module name: routes.py
Author: Michele Grieco
Description:
    This module contains the routes for user authentication, including login, logout, registration, and password reset.
Usage:
    - /login: Route for user login.
    - /logout: Route for user logout.
    - /register: Route for new user registration.
    - /reset_password_request: Route to request a password reset.
    - /reset_password/<token>: Route to reset the password using a token.
"""

from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    If the user is already authenticated, redirect to the main index.
    If the login form is submitted and valid, authenticate the user and
    redirect to the next page or main index.
    :return: Rendered login template or redirect response.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    """
    Log the user out and redirect to the main index.
    :return: Redirect response to the main index.
    """
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    If the user is already authenticated, redirect to the main index.
    If the registration form is submitted and valid, create a new user,
    set their password, and commit to the database. Then redirect to the login page.
    :return: Rendered registration template or redirect response.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    Handle password reset requests.
    If the user is already authenticated, redirect to the main index.
    If the reset password request form is submitted and valid, send a password
    reset email to the user if the email exists in the database. Then redirect to the login page.
    :return: Rendered reset password request template or redirect response.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Handle password reset using a token.
    If the user is already authenticated, redirect to the main index.
    If the token is valid, allow the user to reset their password using the
    reset password form. After successful password reset, redirect to the login page.
    :param token: The password reset token.
    :return: Rendered reset password template or redirect response.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
