# Microblog

Flask web application inspired by the [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

## Overview

This web application demonstrates:

* User authentication (login/logout), registration, and password reset via email
* User profile pages with Gravatar avatars, "about me" field, and last seen time
* Edit user profile (username and "about me" field)
* Create, display, and paginate posts (persisted in the database)
* Follow and unfollow other users
* Explore page to view all posts from all users
* Flash messages and form validation
* Error handling with custom 404 and 500 pages
* Internationalization (English, Spanish, Italian) with Flask-Babel
* Post language detection and translation (Microsoft Translator API)
* Responsive UI with Bootstrap and Moment.js for timestamps
* Docker support for containerized deployment
* Unit tests for models

---

## Prerequisites

* Python 3.12+ installed
* Basic familiarity with the terminal
* (Optional) Docker installed for containerization

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

### 4. Set environment variables (optional, for email and translation)

Create a `.env` file or set variables in shell:

```
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
MS_TRANSLATOR_KEY=your-microsoft-translator-key
```

---

## Project Structure

```
microblog/
├── app/
│   ├── __init__.py            # Flask app initialization
│   ├── cli.py                 # Custom Flask CLI commands
│   ├── email.py               # Email functionality
│   ├── models.py              # Database models
│   ├── translate.py           # Translation service
│   ├── auth/                  # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── email.py          # Password reset emails
│   │   ├── forms.py          # Login/registration forms
│   │   └── routes.py         # Auth routes
│   ├── errors/               # Error handling blueprint
│   │   ├── __init__.py
│   │   └── handlers.py       # Error handlers
│   ├── main/                 # Main application blueprint
│   │   ├── __init__.py
│   │   ├── forms.py         # Post and profile forms
│   │   └── routes.py        # Main routes
│   ├── static/
│   │   └── loading.gif      # Loading animation
│   ├── templates/
│   │   ├── _post.html        # Post template
│   │   ├── base.html         # Base template
│   │   ├── bootstrap_wtf.html
│   │   ├── edit_profile.html
│   │   ├── index.html        # Homepage
│   │   ├── user.html         # User profile
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── reset_password.html
│   │   ├── email/
│   │   │   └── reset_password.html
│   │   └── errors/
│   │       ├── 404.html
│   │       └── 500.html
│   └── translations/          # i18n translations
│       ├── es/
│       └── it/
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
   ```

---

## Running Tests

To run the unit tests:

```bash
python -m unittest tests.py
pytest tests.py # Alternative with pytest installed
```

---

## Docker Support

To build and run the app in Docker:

```bash
docker build -t microblog .
docker run -p 5000:5000 microblog
```

---

## Current Features

* User authentication (login/logout) with email/password
* User registration with email validation
* Password reset via email
* User profiles with:
  - Gravatar avatars
  - "About me" section
  - Last seen time tracking
  - Follow/unfollow functionality
* Posts system with:
  - Creation and display
  - Pagination (25 posts per page)
  - Language detection
  - Translation support via Microsoft Translator API
* Multilanguage support (English, Spanish, Italian)
* Error handling with custom 404 and 500 pages
* Modular application structure with blueprints:
  - auth: User authentication
  - main: Core functionality
  - errors: Error handling
* Flask shell context for testing
* Unit tests for User model
* SQLite database with migrations
* Bootstrap-based responsive UI

---

## Limitations

* No post editing or deletion functionality yet
* No deployment configuration for production

---

## Main Dependencies

* [Flask](https://flask.palletsprojects.com/) - Web framework
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - Database ORM
* [Flask-Migrate](https://flask-migrate.readthedocs.io/) - Database migrations
* [Flask-Login](https://flask-login.readthedocs.io/) - User session management
* [Flask-WTF](https://flask-wtf.readthedocs.io/) - Form handling
* [Flask-Mail](https://pythonhosted.org/Flask-Mail/) - Email support
* [Flask-Moment](https://flask-moment.readthedocs.io/) - Datetime handling
* [Flask-Babel](https://python-babel.github.io/flask-babel/) - Internationalization
* [PyJWT](https://pyjwt.readthedocs.io/) - JSON Web Tokens
* [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variables
* [email-validator](https://pypi.org/project/email-validator/) - Email validation
* [langdetect](https://pypi.org/project/langdetect/) - Language detection
* [requests](https://requests.readthedocs.io/) - HTTP client
* [pytest](https://docs.pytest.org/) - Testing framework
* [mypy](http://mypy-lang.org/) - Static type checking

---

## Next Steps

* Add post editing and deletion
* Add post search functionality
* Add custom avatar upload
* Add user notifications
* Add API endpoints
* Add CSRF protection
* Add rate limiting
* Configure production deployment
* Add continuous integration/deployment
* Improve test coverage

---

## Useful Links

* [Flask documentation](https://flask.palletsprojects.com/en/stable/)
* [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [SQLAlchemy documentation](https://www.sqlalchemy.org/)
* [Flask-Login documentation](https://flask-login.readthedocs.io/en/latest/)
* [Bootstrap documentation](https://getbootstrap.com/)
* [Moment.js documentation](https://momentjs.com/)
* [Flask-Babel documentation](https://python-babel.github.io/flask-babel/)
* [Click documentation](https://click.palletsprojects.com/en/stable/)
* [Microsoft Translator documentation](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/reference/v3/translate)
* [Elastic Search documentation](https://www.elastic.co/docs)