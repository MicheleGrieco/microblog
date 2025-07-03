"""
Module Name: routes.py
Author: Michele Grieco
Created: 2025-06-12
Description:
    This module contains the view functions for the Flask application.
    It handles user authentication, registration, profile editing, and the main index page.

Usage:
    This module is imported by the main application and is used to define the routes and their corresponding view functions.
    The view functions render HTML templates and handle user interactions.
"""

import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user, login_required, logout_user
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from app.models import User


# View functions
@app.route('/') # Decorator, used to register functions as callbacks for certain events
@app.route('/index') # Same as the above
@login_required
def index():
    """
    The main page of the application, which is only accessible to logged-in users.
    It displays a list of posts, which are currently hardcoded.
    :return: Rendered HTML template for the index page.
    :rtype: str
    :raises: None
    """
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST']) # Yet another decorator, which overwrites default GET allowance
def login():
    """
    The login page of the application, which allows users to log in with their credentials.
    If the user is already logged in, they are redirected to the index page.
    If the login form is submitted and valid, the user is authenticated and logged in.
    If the credentials are invalid, an error message is displayed.
    :return: Rendered HTML template for the login page or a redirect to the index page.
    :rtype: str
    :raises: None
    """
    # Check if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve the user from the database
        # If the user or password does not exist, redirect again to login form
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # Check for "next" URL args, then redirect to them
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '': # check if URL is relative or not
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """
    The logout route of the application, which logs out the current user and redirects them to the index page.
    :return: Redirect to the index page.
    :rtype: werkzeug.wrappers.Response
    :raises: None
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    The registration page of the application, which allows new users to create an account.
    If the user is already logged in, they are redirected to the index page.
    If the registration form is submitted and valid, a new user is created and added to the database.
    :return: Rendered HTML template for the registration page or a redirect to the login page
    :rtype: str
    :raises: None
    """
    # Make sure user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create the user with username, email and password
        # Add it to the database
        user = User()
        user.username=str(form.username.data)
        user.email=str(form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
        
        
@app.route('/user/<username>') # Dynamic decorator
@login_required
def user(username):
    """
    The user profile page, which displays the user's information and their posts.
    If the user does not exist, a 404 error is raised.
    :param username: The username of the user whose profile is being viewed.
    :type username: str
    :return: Rendered HTML template for the user profile page.
    :rtype: str
    :raises: 404 error if the user does not exist.
    """
    # Works as scalar() when there are results,
    # sends a 404 to the client otherwise
    user = db.first_or_404(sa.select(User).where(User.username == username))
    # Placeholder list of posts
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    """
    Update the last seen time of the current user before each request.
    :return: None
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit() # no db.session.add() needed, since the user is already in the session
        
        
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    The edit profile page, which allows users to update their profile information.
    If the form is submitted and valid, the user's information is updated in the database.
    If the request method is GET, the form is pre-filled with the current user's data.
    :return: Rendered HTML template for the edit profile page.
    :rtype: str
    :raises: None
    """
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit:
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET': # GET request, pre-fill the form with current user data
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username)
        )
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    

