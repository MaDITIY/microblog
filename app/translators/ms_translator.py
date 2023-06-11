"""Microsoft translator implementation module."""
import requests
import uuid

from flask import current_app
from flask_babel import _

from app.translators import BaseTranslator


class MicrosoftTranslator(BaseTranslator):
    """Microsoft translator class."""
    @staticmethod
    def translate(text: str, source_language: str, dest_language: str) -> str:
        """Translate text using MS Translator API"""
        if (
                'MS_TRANSLATOR_KEY' not in current_app.config or
                not current_app.config['MS_TRANSLATOR_KEY']
        ):
            return _('Error: the translator service is not properly configured.')
        auth = {
            'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
            'Ocp-Apim-Subscription-Region': current_app.config['MS_TRANSLATOR_LOCATION'],
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        params = {
            'api-version': '3.0',
            'from': source_language,
            'to': [dest_language, ]
        }
        body = [{
            'text': text
        }]
        response = requests.post(
            'https://api.cognitive.microsofttranslator.com/translate',
            headers=auth,
            params=params,
            json=body,
        )
        if response.status_code != 200:
            return _('Error: the translation service failed.')
        response_json = response.json()
        return response_json[0]['translations'][0]['text']
