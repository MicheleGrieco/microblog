"""
Module Name: email.py
Author: Michele Grieco
Created: 2025-07-07
Description:
    This module provides functionality to send emails using Flask-Mail.q 
    It includes functions to send emails asynchronously, send a password reset email,
    and render email templates. The email sending is done in a separate thread to avoid blocking
    the main application thread, allowing for a smoother user experience.

Usage:
    - send_email(subject, sender, recipients, text_body, html_body)
    - send_password_reset_email(user)
"""

from flask_mail import Message
from flask import render_template
from app import mail, app
from threading import Thread

def send_async_email(app, msg):
    """
    Function to send email asynchronously using Flask's application context.
    This allows the email to be sent without blocking the main thread.
    :param app: Flask application instance
    :param msg: Message object containing email details
    :return: None
    """
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    """
    Function to send an email with both text and HTML body.
    This function creates a Message object and sends it asynchronously.
    :param subject: Subject of the email
    :param sender: Email address of the sender
    :param recipients: List of recipient email addresses
    :param text_body: Plain text body of the email
    :param html_body: HTML body of the email
    :return: None
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
    
def send_password_reset_email(user):
    """
    Function to send a password reset email to the user.
    This function generates a reset token for the user and sends an email
    with a link to reset the password.
    :param user: User object for whom the password reset email is to be sent
    :return: None
    """
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))