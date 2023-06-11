"""Translators init module."""
from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    """Abstract translator class."""
    @staticmethod
    @abstractmethod
    def translate(text: str, source_language: str, dest_language: str) -> str:
        """Abstract translate method."""
        raise NotImplementedError()
