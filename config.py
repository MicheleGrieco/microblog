"""
Module Name: config.py
Author: Michele Grieco
Created: 2025-06-12
Description:
    This module contains the configuration settings for the Flask application.
    It defines the application's secret key, database URI, mail server settings, and admin email addresses.
    The configuration can be customized using environment variables or defaults.    

Usage:
    This module is imported by the main application and is used to configure the Flask app.
    It sets up the necessary configurations for database access, email notifications, and security.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__)) # The main directory of the application

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['michelegrieco92@gmail.com']
    POSTS_PER_PAGE = 25