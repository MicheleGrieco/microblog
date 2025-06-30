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
* Show example posts on the home and user pages (currently hardcoded)

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
│   ├── forms.py               # Login, registration, and edit profile forms (Flask-WTF)
│   ├── models.py              # User and Post models (SQLAlchemy)
│   ├── routes.py              # Routes: index, login, logout, register, user profile, edit profile
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

## Current Features

* User registration with unique email and username validation
* Login/logout with user session management
* Flash message display
* Example posts shown on the home page (currently hardcoded)
* User profile pages at `/user/<username>` with Gravatar avatar and last seen info
* Edit profile page for the logged-in user
* HTML templates with Jinja2

---

## Limitations

* Posts are not yet stored in the database; only hardcoded examples are shown
* No post creation or editing functionality yet
* No pagination or search features
* No deployment configuration for production

--

## Main Dependencies

* [Flask](https://flask.palletsprojects.com/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-WTF](https://flask-wtf.readthedocs.io/)
* [email-validator](https://pypi.org/project/email-validator/)

---

## Next Steps

* Add the ability to create new posts in the database
* Display real posts from the database on the home and user pages
* Improve user profile management (e.g., allow avatar upload)
* Add post pagination
* Prepare for deployment to a production server

---

## Useful Links

* [Flask documentation](https://flask.palletsprojects.com/en/stable/)
* [SQLAlchemy documentation](https://www.sqlalchemy.org/)
* [Flask-Login documentation](https://flask-login.readthedocs.io/en/latest/)
* [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)