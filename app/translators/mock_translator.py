"""Mock translator implementation module."""
from app.translators import BaseTranslator


class MockTranslator(BaseTranslator):
    """Mock translator class."""
    @staticmethod
    def translate(text: str, source_language: str, dest_language: str) -> str:
        """Always return given text w/o any translation."""
        del source_language
        del dest_language
        return text
