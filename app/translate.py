"""Translation utils module."""
from typing import Type

from flask import current_app

from app.translators import BaseTranslator
from app.translators.mock_translator import MockTranslator
from app.translators.ms_translator import MicrosoftTranslator


def get_application_translator() -> Type[BaseTranslator]:
    """Chose translator instance based on application settings."""
    config_translator = current_app.config.get('APP_TRANSLATOR')
    if config_translator and config_translator == 'ms_translator':
        return MicrosoftTranslator
    return MockTranslator


def translate(text: str, source_language: str, dest_language: str) -> str:
    """Call application chosen translator's translate method."""
    translator = get_application_translator()
    return translator.translate(text, source_language, dest_language)
