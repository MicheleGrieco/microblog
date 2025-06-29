from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # Database instance
migrate = Migrate(app, db) # Database migration engine
login = LoginManager(app)
login.login_view = 'login' # type: ignore

from app import routes, models, errors