import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user, login_required, logout_user
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

# View functions
@app.route('/') # Decorator, used to register functions as callbacks for certain events
@app.route('/index') # Same as the above
@login_required
def index():
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
    # Check if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve the user from the database
        # If the user or password do not exist, redirect again to login form
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # Check for "next" URL args, than redirect to them
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '': # check if URL is relative or not
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    # Works as scalar() when there are results,
    # sends a 404 to the client otherwise
    user = db.first_or_404(sa.select(User).where(User.username == username))
    # Placeholder list of posts
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)