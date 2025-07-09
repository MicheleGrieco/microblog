"""
Module Name: forms.py
Author: Michele Grieco
Created: 2025-06-12
Description:
    This module defines the forms used in the Flask application.
    It includes forms for user login, registration, profile editing and other interactions.
    The forms use Flask-WTF for form handling and validation.

Usage:
    This module is imported by the main application and is used to define the forms for user interactions.
    The forms are rendered in HTML templates and handle user input validation.
"""

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length
from app import db
from app.models import User

class LoginForm(FlaskForm):
    """
    Form for user login.
    This form includes fields for username, password, and a remember me option.
    It uses Flask-WTF for form handling and validation.
    Attributes:
        username (StringField): The username field for user login.
        password (PasswordField): The password field for user login.
        remember_me (BooleanField): Checkbox to remember the user on the device.
        submit (SubmitField): Submit button to log in the user.
    Validators:
        DataRequired: Ensures that the username and password fields are not empty.
    Usage:
        This form is used in the login view to authenticate users.
        It is rendered in the login template and handles user input validation.
    :param FlaskForm: Base class for Flask-WTF forms.
    :type FlaskForm: class
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    This form includes fields for username, email, password, and password confirmation.
    It uses Flask-WTF for form handling and validation.
    Attributes:
        username (StringField): The username field for user registration.
        email (StringField): The email field for user registration.
        password (PasswordField): The password field for user registration.
        password2 (PasswordField): Confirmation field for the password.
        submit (SubmitField): Submit button to register the user.
    Validators:
        DataRequired: Ensures that the username, email, and password fields are not empty.
        Email: Validates that the email field contains a valid email address.
        EqualTo: Ensures that the password confirmation matches the password.
    Usage:
        This form is used in the registration view to create new users.
        It is rendered in the registration template and handles user input validation.
    :param FlaskForm: Base class for Flask-WTF forms.
    :type FlaskForm: class
    :raises ValidationError: If the username or email already exists in the database.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    # Custom validators (validate_<attribute> pattern)
    def validate_username(self, username):
        """
        Validate that the username is unique in the database.
        Raises ValidationError if the username already exists.
        :param username: The username field to validate.
        :raises ValidationError: If the username already exists.
        """
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        """
        Validate that the email is unique in the database.
        Raises ValidationError if the email already exists.
        :param email: The email field to validate.
        :raises ValidationError: If the email already exists.
        """
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        

class EditProfileForm(FlaskForm):
    """
    Form for editing user profile.
    This form includes fields for username and about me section.
    It uses Flask-WTF for form handling and validation.
    Attributes:
        username (StringField): The username field for editing the profile.
        about_me (TextAreaField): A text area for the user to write about themselves.
        submit (SubmitField): Submit button to save the profile changes.
    Validators:
        DataRequired: Ensures that the username field is not empty.
        Length: Validates the length of the about me section (maximum 140 characters).
    Usage:
        This form is used in the profile editing view to allow users to update their profile information.
        It is rendered in the profile template and handles user input validation.
    :param FlaskForm: Base class for Flask-WTF forms.
    :type FlaskForm: class
    """
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    
    def __init__(self, original_username, *args, **kwargs):
        """
        Initialize the form with the original username to validate against.
        :param original_username: The original username to compare against.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :raises: ValidationError if the new username is already taken.
        """
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        
    def validate_username(self, username):
        """
        Validate that the username is unique in the database, excluding the original username.
        Raises ValidationError if the username already exists.
        :param username: The username field to validate.
        :raises ValidationError: If the username already exists.
        """
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
            

class PostForm(FlaskForm):
    """
    Form for creating or editing a post.
    This form includes a text area for the post content and a submit button.
    It uses Flask-WTF for form handling and validation.
    Attributes:
        post (TextAreaField): The text area field for the post content.
        submit (SubmitField): Submit button to create or edit the post.
    Validators:
        DataRequired: Ensures that the post field is not empty.
        Length: Validates the length of the post content (minimum 1 character, maximum 140 characters).
    Usage:
        This form is used in the post creation and editing views to handle user input.
        It is rendered in the post template and handles validation for the post content.
    :param FlaskForm: Base class for Flask-WTF forms.
    :type FlaskForm: class
    """
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
    

class ResetPasswordRequestForm(FlaskForm):
    """
    Form for requesting a password reset.
    This form includes a field for the user's email address.
    It uses Flask-WTF for form handling and validation.
    Attributes:
        email (StringField): The email field for requesting a password reset.
        submit (SubmitField): Submit button to request the password reset.
    Validators:
        DataRequired: Ensures that the email field is not empty.
        Email: Validates that the email field contains a valid email address.
    Usage:
        This form is used in the password reset request view to collect the user's email.
        It is rendered in the password reset request template and handles user input validation.
    :param FlaskForm: Base class for Flask-WTF forms.
    :type FlaskForm: class
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
            

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
            
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')