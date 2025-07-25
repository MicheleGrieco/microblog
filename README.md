# Microblog

Flask web application inspired by the [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

## Overview

This mini-app demonstrates how to:

* Manage users with authentication (login/logout) and registration
* Use Flask, Flask-WTF, Flask-Login, Flask-Migrate, and SQLAlchemy
* Structure a Flask project with models, routes, and templates
* Handle a relational database for users and posts
* Display flash messages and form validation
* Display user profile pages with avatars (via Gravatar)
* Edit user profile (username and "about me" field)
* Show posts on the home and user pages (with pagination)
* Track last seen time for users
* Follow and unfollow other users
* Explore all posts from all users
* Error handling with custom 404 and 500 pages
* Docker support for containerized deployment
* Unit tests for models

---

## Prerequisites

* Python 3.12+ installed
* Basic familiarity with the terminal

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MicheleGrieco/microblog.git
cd microblog
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate       # On macOS/Linux
venv\Scripts\activate          # On Windows (cmd.exe)
venv\Scripts\Activate.ps1      # On Windows PowerShell
# Use only the command appropriate for your shell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Project Structure


```
microblog/
├── app/
│   ├── __init__.py            # Flask app, db, login manager initialization
│   ├── errors.py              # Error handlers
│   ├── forms.py               # Login, registration, edit profile, and post forms
│   ├── models.py              # User and Post models (SQLAlchemy)
│   ├── routes.py              # Routes: index, login, logout, register, user profile, edit profile, follow/unfollow, explore
│   └── templates/
│       ├── _post.html
│       ├── 404.html
│       ├── 500.html
│       ├── base.html
│       ├── edit_profile.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       └── user.html
│   
├── migrations/
├── app.db                     # SQLite database file
├── config.py                  # App configuration
├── Dockerfile                 # Docker support
├── microblog.py               # WSGI entry point
├── requirements.txt           # Python dependencies
├── tests.py                   # Unit tests for models
└── README.md                  # Project documentation
```

---

## Running the App

1. Set the `FLASK_APP` environment variable:

   ```bash
   export FLASK_APP=microblog.py       # macOS/Linux
   set FLASK_APP=microblog.py          # Windows CMD
   $env:FLASK_APP = "microblog.py"     # Windows PowerShell
   ```

2. (Optional) Initialize the database:

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

3. Start the development server:

   ```bash
   flask run
   ```

4. Visit the app in your browser:

   ```
   http://127.0.0.1:5000/
   http://127.0.0.1:5000/index
   ```

---

## Running Tests

To run the unit tests:

```bash
python -m unittest tests.py
pytest tests.py # Alternative with pytest installed
```

---

## Current Features

* User registration with unique email and username validation
* Login/logout with user session management
* Flash message display
* Create and display posts (persisted in the database)
* User profile pages at `/user/<username>` with Gravatar avatar, about me, and last seen info
* Edit profile page for the logged-in user
* Track last seen time for users
* Follow and unfollow other users
* Explore page to view all posts from all users
* Pagination for posts on home, user, and explore pages
* Custom error pages (404 and 500)
* Docker support for containerized deployment
* Unit tests for user and post models
* HTML templates with Jinja2 and Bootstrap

---

## Limitations

* No post editing or deletion functionality yet
* No deployment configuration for production

---

## Main Dependencies

* [Flask](https://flask.palletsprojects.com/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-WTF](https://flask-wtf.readthedocs.io/)
* [email-validator](https://pypi.org/project/email-validator/)

---

## Next Steps

* Add the ability to edit and delete posts
* Improve user profile management (e.g., allow avatar upload)
* Add post search functionality
* Prepare for deployment to a production server

---

## Useful Links

* [Flask documentation](https://flask.palletsprojects.com/en/stable/)
* [SQLAlchemy documentation](https://www.sqlalchemy.org/)
* [Flask-Login documentation](https://flask-login.readthedocs.io/en/latest/)
* [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [Bootstrap documentation](https://getbootstrap.com/)
* [Moment.js documentation](https://momentjs.com/)