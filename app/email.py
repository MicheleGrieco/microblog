"""
Module name: email.py
Author: Michele Grieco
Description:
    Email sending functions.
    In the send_email() function, the application instance is passed as an argument
    to a background thread that will then deliver the email without blocking the main application.
    Using current_app directly in the send_async_email() function that runs as a background thread
    would not have worked, because current_app is a context-aware variable that is tied to the thread
    that is handling the client request.
    In a different thread, current_app would not have a value assigned.
    Passing current_app directly as an argument to the thread object would not have worked either,
    because current_app is really a proxy object that is dynamically mapped to the application instance.
    So passing the proxy object would be the same as using current_app directly in the thread.
    What I needed to do is access the real application instance that is stored inside the proxy object,
    and pass that as the app argument.
    The current_app._get_current_object() expression extracts the actual application instance
    from inside the proxy object, so that is what I passed to the thread as an argument.
Usage:
    - send_email(subject, sender, recipients, text_body, html_body): Send an email asynchronously.
    - send_async_email(app, msg): Helper function to send email in a background thread.
"""

from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg) -> None:
    """
    Send an email in a background thread.
    :param app: The Flask application instance.
    :param msg: The email message to send.
    :return: None
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body) -> None:
    """
    Send an email asynchronously.
    :param subject: The subject of the email.
    :param sender: The sender's email address.
    :param recipients: A list of recipient email addresses.
    :param text_body: The plain text body of the email.
    :param html_body: The HTML body of the email.
    :return: None
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start() # pyright: ignore[reportAttributeAccessIssue]
