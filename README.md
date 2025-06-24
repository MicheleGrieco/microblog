# Microblog

Flask web application inspired by the [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

## Overview

This mini-app demonstrates how to:

* Manage users with authentication (login/logout) and registration
* Use Flask, Flask-WTF, Flask-Login, Flask-Migrate, and SQLAlchemy
* Structure a Flask project with models, routes, and templates
* Handle a relational database for users and posts
* Display flash messages and form validation

---

## Prerequisites

* Python 3.x installed
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
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
microblog/
├── venv/                   # Virtual environment
├── app/
│   ├── __init__.py         # Flask app, db, login manager initialization
│   ├── models.py           # User and Post models (SQLAlchemy)
│   ├── routes.py           # Routes: index, login, logout, register
│   ├── forms.py            # Login and registration forms (Flask-WTF)
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       └── register.html
├── migrations/             # Database migrations (Flask-Migrate)
├── microblog.py            # WSGI entry point
└── README.md
```

---

## Running the App

1. Set the `FLASK_APP` environment variable:

   ```bash
   export FLASK_APP=microblog.py       # macOS/Linux
   set FLASK_APP=microblog.py          # Windows CMD
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
* Example posts shown on the home page
* HTML templates with Jinja2

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

* Add the ability to create new posts
* Improve user profile management
* Post pagination
* Deployment to a production server

---

## Useful Links

* [Flask documentation](https://flask.palletsprojects.com/en/stable/)
* [SQLAlchemy documentation](https://www.sqlalchemy.org/)
* [Flask-Login documentation](https://flask-login.readthedocs.io/en/latest/)
* [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)