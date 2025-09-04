"""
Module name: translate.py
Author: Michele Grieco
Description:
    This module provides a function to translate text using the Microsoft Translator API.
    It checks for the presence of an API key in the application configuration and
    handles errors gracefully by returning appropriate messages.
Usage:
    - translate: Function to translate text from a source language to a destination language.
"""

import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language) -> str:
    """
    Translate text from source_language to dest_language using Microsoft Translator API.
    :param text: The text to translate.
    :param source_language: The language code of the source text.
    :param dest_language: The language code to translate the text into.
    :return: The translated text or an error message if the service is not configured or fails.
    """
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'westus'
    }
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com'
        '/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[
                {'Text': text}])
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return r.json()[0]['translations'][0]['text']
