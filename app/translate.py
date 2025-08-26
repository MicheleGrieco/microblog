import requests
from flask_babel import _
from app import app

def translate(text, source_language, dest_language):
    """
    Translates text from the source language to the destination language
    using the Microsoft Translator service.
    :param text: the text to translate
    :param source_language: the language code of the source text
    :param dest_language: the language code for the translation
    :return: the translated text or an error message if the service is not
    configured or fails.
    """
    if 'MS_TRANSLATOR_KEY' not in app.config or \
        not app.config['MS_TRANSLATOR_KEY']:
            return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'westus',
    }
    
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com'
        '/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[{'Text': text}]
    )
    
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return r.json()[0]['translations'][0]['text']