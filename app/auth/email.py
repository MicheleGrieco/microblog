from flask import render_template, current_app
from flask_babel import _
from app.email import send_email


def send_password_reset_email(user) -> None:
    """
    Send a password reset email to the specified user.
    This function generates a password reset token and sends an email with
    instructions to reset the password.
    :param user: The user object to whom the email will be sent.
    :return: None
    """
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
