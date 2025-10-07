"""
Translator for SRT subtitle files.

This module translates subtitle text from English to target languages
using the deep-translator library with caching and batch translation support.
"""

import json
import hashlib
from typing import List, Optional
from pathlib import Path
from tqdm import tqdm
from deep_translator import GoogleTranslator
from src.ast_nodes import SubtitleEntry, TimeStamp


class TranslationError(Exception):
    """Exception raised for translation errors."""
    pass


class Translator:
    """
    Translator for subtitle entries.

    Translates subtitle text from English to supported target languages
    with caching and batch translation for improved performance.
    """

    # Language mapping: user-friendly name → language code
    LANGUAGE_MAP = {
        'english': 'en',
        'filipino': 'tl',  # Tagalog
        'korean': 'ko',
        'chinese': 'zh-CN',  # Simplified Chinese
        'japanese': 'ja',
    }

    # Batch size for translation (API limits)
    BATCH_SIZE = 50

    def __init__(self, target_lang: str = 'filipino', use_cache: bool = True):
        """
        Initialize translator with target language.

        Args:
            target_lang: Target language name (default: 'filipino')
            use_cache: Whether to use file-based caching (default: True)

        Raises:
            TranslationError: If target language is not supported
        """
        self.target_lang = target_lang.lower()
        self.use_cache = use_cache

        if self.target_lang not in self.LANGUAGE_MAP:
            supported = ', '.join(self.LANGUAGE_MAP.keys())
            raise TranslationError(
                f"Unsupported language '{target_lang}'. "
                f"Supported languages: {supported}"
            )

        self.target_code = self.LANGUAGE_MAP[self.target_lang]

        # Setup cache directory
        if self.use_cache:
            self.cache_dir = Path('.cache/translations')
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def translate_entries(
        self,
        entries: List[SubtitleEntry],
        file_content: Optional[str] = None
    ) -> List[SubtitleEntry]:
        """
        Translate subtitle entries to target language.

        Args:
            entries: List of SubtitleEntry objects with English text
            file_content: Original file content for cache key generation

        Returns:
            List of SubtitleEntry objects with translated text

        Note:
            If translation fails for any entry, it falls back to English
            and prints a warning message.
        """
        # If target is English, return original entries (no translation needed)
        if self.target_lang == 'english':
            return entries

        # Try to load from cache
        if self.use_cache and file_content:
            cached = self._load_from_cache(file_content)
            if cached:
                print("  Loaded from cache (instant)")
                return cached

        # Translate with batch processing and progress bar
        translated_entries = self._translate_with_batching(entries)

        # Save to cache
        if self.use_cache and file_content:
            self._save_to_cache(file_content, translated_entries)

        return translated_entries

    def _translate_with_batching(self, entries: List[SubtitleEntry]) -> List[SubtitleEntry]:
        """
        Translate entries using batch translation with progress bar.

        Args:
            entries: List of SubtitleEntry objects

        Returns:
            List of translated SubtitleEntry objects
        """
        translated_entries = []

        # Create GoogleTranslator instance once
        translator = GoogleTranslator(source='en', target=self.target_code)

        # Process entries with progress bar
        with tqdm(total=len(entries), desc="  Translating", unit="subtitle") as pbar:
            # Process in batches
            for i in range(0, len(entries), self.BATCH_SIZE):
                batch = entries[i:i + self.BATCH_SIZE]

                try:
                    # Collect all text lines from batch
                    batch_texts = []
                    batch_text_map = []  # Track which entry each text belongs to

                    for entry in batch:
                        entry_texts = []
                        for line in entry.text:
                            if line.strip():
                                batch_texts.append(line.strip())
                                entry_texts.append(len(batch_texts) - 1)
                            else:
                                entry_texts.append(None)  # Empty line
                        batch_text_map.append(entry_texts)

                    # Translate batch
                    if batch_texts:
                        translated_batch = translator.translate_batch(batch_texts)

                        # Reconstruct entries with translated text
                        for entry, text_indices in zip(batch, batch_text_map):
                            translated_lines = []
                            for idx in text_indices:
                                if idx is None:
                                    translated_lines.append("")
                                else:
                                    translated_lines.append(translated_batch[idx])

                            translated_entry = SubtitleEntry(
                                index=entry.index,
                                start_time=entry.start_time,
                                end_time=entry.end_time,
                                text=translated_lines,
                                formatting=entry.formatting
                            )
                            translated_entries.append(translated_entry)
                    else:
                        # All empty lines, keep original
                        translated_entries.extend(batch)

                    pbar.update(len(batch))

                except Exception as e:
                    # Fall back to English for this batch
                    print(f"\n  Warning: Batch translation failed: {e}")
                    print(f"  Falling back to English for subtitles {batch[0].index}-{batch[-1].index}")
                    translated_entries.extend(batch)
                    pbar.update(len(batch))

        return translated_entries

    def _load_from_cache(self, file_content: str) -> Optional[List[SubtitleEntry]]:
        """
        Load translation from cache if available.

        Args:
            file_content: Original file content

        Returns:
            List of cached SubtitleEntry objects, or None if not cached
        """
        cache_file = self._get_cache_file(file_content)

        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Reconstruct SubtitleEntry objects
                entries = []
                for entry_data in data['entries']:
                    entry = SubtitleEntry(
                        index=entry_data['index'],
                        start_time=TimeStamp(
                            entry_data['start_time']['hours'],
                            entry_data['start_time']['minutes'],
                            entry_data['start_time']['seconds'],
                            entry_data['start_time']['milliseconds']
                        ),
                        end_time=TimeStamp(
                            entry_data['end_time']['hours'],
                            entry_data['end_time']['minutes'],
                            entry_data['end_time']['seconds'],
                            entry_data['end_time']['milliseconds']
                        ),
                        text=entry_data['text'],
                        formatting=entry_data.get('formatting')
                    )
                    entries.append(entry)

                return entries

            except Exception as e:
                print(f"  Warning: Failed to load cache: {e}")
                return None

        return None

    def _save_to_cache(self, file_content: str, entries: List[SubtitleEntry]) -> None:
        """
        Save translation to cache.

        Args:
            file_content: Original file content
            entries: Translated SubtitleEntry objects
        """
        cache_file = self._get_cache_file(file_content)

        try:
            # Convert entries to serializable format
            data = {
                'language': self.target_lang,
                'entries': []
            }

            for entry in entries:
                entry_data = {
                    'index': entry.index,
                    'start_time': {
                        'hours': entry.start_time.hours,
                        'minutes': entry.start_time.minutes,
                        'seconds': entry.start_time.seconds,
                        'milliseconds': entry.start_time.milliseconds
                    },
                    'end_time': {
                        'hours': entry.end_time.hours,
                        'minutes': entry.end_time.minutes,
                        'seconds': entry.end_time.seconds,
                        'milliseconds': entry.end_time.milliseconds
                    },
                    'text': entry.text,
                    'formatting': entry.formatting
                }
                data['entries'].append(entry_data)

            # Save to file
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"  Warning: Failed to save cache: {e}")

    def _get_cache_file(self, file_content: str) -> Path:
        """
        Get cache file path for given content.

        Args:
            file_content: Original file content

        Returns:
            Path to cache file
        """
        # Create hash of content
        content_hash = hashlib.md5(file_content.encode('utf-8')).hexdigest()

        # Cache filename: hash_language.json
        cache_filename = f"{content_hash}_{self.target_lang}.json"

        return self.cache_dir / cache_filename

    @classmethod
    def get_supported_languages(cls) -> List[str]:
        """
        Get list of supported language names.

        Returns:
            List of supported language names
        """
        return list(cls.LANGUAGE_MAP.keys())
