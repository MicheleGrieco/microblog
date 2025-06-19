# Microblog

Flask web app built following <a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world" target="_blank">The Flask Mega Tutorial</a>.

## 🚀 Overview

This mini-app demonstrates how to:

* Set up a Python virtual environment
* Install and import the Flask framework
* Structure a minimal Flask project with a package
* Create a basic route and view function
* Run the development server

By the end, it’ll be a working Flask app that responds at `http://localhost:5000/` or `/index`.

---

## Prerequisites

* Python 3.x installed on your machine
* Basic familiarity with the command line

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

### 3. Install Flask

```bash
pip install flask
```

---

## Project Structure

```
microblog/
├── venv/           # Virtual environment
├── app/            
│   ├── __init__.py # Flask app instance
│   └── routes.py   # Route definitions
└── microblog.py    # WSGI entry point
```

* **app/**init**.py**: Initializes the `Flask` app instance and imports routes.
* **app/routes.py**: Defines the `index()` view with two routes (`/` and `/index`) returning **"Hello, World!"**.
* **microblog.py**: Imports the app and serves as the entry point for Flask CLI.

---

## Running the App

1. Set the `FLASK_APP` environment variable:

   ```bash
   export FLASK_APP=microblog.py       # macOS/Linux
   set FLASK_APP=microblog.py          # Windows CMD
   ```

2. Start the development server:

   ```bash
   flask run
   ```

3. Visit your app in a browser:

   ```
   http://127.0.0.1:5000/
   http://127.0.0.1:5000/index
   ```

---

## Notes & Best Practices

* Use [`venv`](https://docs.python.org/3/library/venv.html) to isolate dependencies.
* Use `requirements.txt` to install all the dependencies at once.
* Keep environment variables in an optional `.flaskenv` (requires `python-dotenv`) to avoid repeatedly exporting them.
* The import of `routes` inside `app/__init__.py` avoids circular dependencies common in Flask apps.

---

## What’s Next?

Continue with Miguel Grinberg’s Mega‑Tutorial to add templates, forms, database support, user authentication, deployment, and more.

Check out the [official tutorial post](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) and the \[full Microblog project on GitHub].