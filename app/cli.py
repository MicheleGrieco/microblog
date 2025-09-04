"""
Module name: cli.py
Author: Michele Grieco
Description:
    Translation and localization commands for the Flask application.
    These commands use the Flask CLI integration to provide a set of commands
    for managing translations using the Babel toolchain.

    Replacing app with current_app does not work in this case because these commands
    are registered at startup, not during the handling of a request, which is the only time
    when current_app can be used. To remove the reference to app in this module,
    I created another blueprint.

    Flask puts commands that are attached to blueprints under a group with the blueprint's name by default.
    That would have caused these commands to be available as flask cli translate <command>.
    To aboid the extra cli group, the cli_group=None argument is given to the blueprint,
    then I register this cli blueprint in the application factory function in app/__init__.py.

Usage:
    - translate init <lang>: Initialize a new language.
    - translate update: Update all languages.
    - translate compile: Compile all languages.
"""

import os
from flask import Blueprint
import click

bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.group()
def translate() -> None:
    """Translation and localization commands."""
    pass


@translate.command()
@click.argument('lang')
def init(lang) -> None:
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate.command()
def update() -> None:
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate.command()
def compile() -> None:
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')
