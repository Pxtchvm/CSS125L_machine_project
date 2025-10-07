"""
Translator for SRT subtitle files.

This module translates subtitle text from English to target languages
using the deep-translator library.
"""

from typing import List
from deep_translator import GoogleTranslator
from src.ast_nodes import SubtitleEntry


class TranslationError(Exception):
    """Exception raised for translation errors."""
    pass


class Translator:
    """
    Translator for subtitle entries.

    Translates subtitle text from English to supported target languages.
    """

    # Language mapping: user-friendly name → language code
    LANGUAGE_MAP = {
        'english': 'en',
        'filipino': 'tl',  # Tagalog
        'korean': 'ko',
        'chinese': 'zh-CN',  # Simplified Chinese
        'japanese': 'ja',
    }

    def __init__(self, target_lang: str = 'filipino'):
        """
        Initialize translator with target language.

        Args:
            target_lang: Target language name (default: 'filipino')

        Raises:
            TranslationError: If target language is not supported
        """
        self.target_lang = target_lang.lower()

        if self.target_lang not in self.LANGUAGE_MAP:
            supported = ', '.join(self.LANGUAGE_MAP.keys())
            raise TranslationError(
                f"Unsupported language '{target_lang}'. "
                f"Supported languages: {supported}"
            )

        self.target_code = self.LANGUAGE_MAP[self.target_lang]

    def translate_entries(self, entries: List[SubtitleEntry]) -> List[SubtitleEntry]:
        """
        Translate subtitle entries to target language.

        Args:
            entries: List of SubtitleEntry objects with English text

        Returns:
            List of SubtitleEntry objects with translated text

        Note:
            If translation fails for any entry, it falls back to English
            and prints a warning message.
        """
        # If target is English, return original entries (no translation needed)
        if self.target_lang == 'english':
            return entries

        translated_entries = []

        for entry in entries:
            try:
                # Translate each text line
                translated_lines = []
                for line in entry.text:
                    translated_line = self._translate_text(line)
                    translated_lines.append(translated_line)

                # Create new entry with translated text
                translated_entry = SubtitleEntry(
                    index=entry.index,
                    start_time=entry.start_time,
                    end_time=entry.end_time,
                    text=translated_lines,
                    formatting=entry.formatting
                )
                translated_entries.append(translated_entry)

            except Exception as e:
                # Fall back to English on error
                print(f"Warning: Translation failed for subtitle {entry.index}: {e}")
                print(f"  Falling back to English for this subtitle.")
                translated_entries.append(entry)  # Keep original

        return translated_entries

    def _translate_text(self, text: str) -> str:
        """
        Translate a single text string.

        Args:
            text: English text to translate

        Returns:
            Translated text

        Raises:
            Exception: If translation fails (network error, API error, etc.)
        """
        # Strip whitespace for translation
        stripped = text.strip()

        if not stripped:
            return text  # Return empty/whitespace as-is

        try:
            translator = GoogleTranslator(source='en', target=self.target_code)
            translated = translator.translate(stripped)
            return translated

        except Exception as e:
            # Re-raise to be caught by translate_entries
            raise Exception(f"Network or API error: {e}")

    @classmethod
    def get_supported_languages(cls) -> List[str]:
        """
        Get list of supported language names.

        Returns:
            List of supported language names
        """
        return list(cls.LANGUAGE_MAP.keys())
