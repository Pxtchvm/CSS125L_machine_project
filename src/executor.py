"""
Executor - displays the subtitles and handles translation.
This is where the subtitles actually get shown.
"""

import time


class ExecutorError(Exception):
    """Error when something goes wrong during execution"""
    pass


class Executor:
    """Displays subtitles one by one"""

    def execute(self, entries, translate_to=None):
        """
        Display all the subtitles.

        Args:
            entries: List of SubtitleEntry objects
            translate_to: Language to translate to (e.g., 'filipino', 'korean')
                         If None, shows original English text
        """
        if not entries:
            raise ExecutorError("No subtitles to display")

        # Translate if requested
        if translate_to and translate_to.lower() != 'english':
            print(f"\nTranslating to {translate_to}...")
            entries = self.translate_subtitles(entries, translate_to)
            print("Translation complete!                    \n")  # Extra spaces clear progress line

        # Display each subtitle
        for entry in entries:
            # Show the subtitle
            start_time = self.format_time(entry.start_time)
            text = entry.get_text()
            print(f"[{start_time}] DISPLAY: \"{text}\"")

            # Pause briefly
            time.sleep(0.5)

            # Clear the subtitle
            end_time = self.format_time(entry.end_time)
            print(f"[{end_time}] CLEAR")

            # Pause before next subtitle
            time.sleep(0.5)

    def translate_subtitles(self, entries, target_language):
        """
        Translate all subtitle text to another language using Google Translate.

        Args:
            entries: List of SubtitleEntry objects
            target_language: Target language name

        Returns:
            New list of SubtitleEntry objects with translated text
        """
        # Import the translation library
        try:
            from deep_translator import GoogleTranslator
        except ImportError:
            raise ExecutorError("Translation library not installed. Run: pip install deep-translator")

        # Map language names to codes
        language_codes = {
            'filipino': 'tl',  # Tagalog
            'tagalog': 'tl',
            'korean': 'ko',
            'chinese': 'zh-CN',
            'japanese': 'ja',
            'english': 'en'
        }

        # Get the language code
        target_code = language_codes.get(target_language.lower())
        if not target_code:
            raise ExecutorError(f"Language '{target_language}' not supported")

        # Create translator
        translator = GoogleTranslator(source='en', target=target_code)

        # Translate each subtitle
        translated_entries = []
        for i, entry in enumerate(entries):
            print(f"  Translating subtitle {i + 1}/{len(entries)}...", end='\r')

            # Translate each line of text
            translated_lines = []
            for line in entry.text:
                try:
                    translated = translator.translate(line)
                    translated_lines.append(translated)
                except Exception as e:
                    # If translation fails, keep original
                    print(f"\n  Warning: Could not translate line, keeping original")
                    translated_lines.append(line)

            # Create new entry with translated text
            from src.ast import SubtitleEntry
            new_entry = SubtitleEntry(
                entry.index,
                entry.start_time,
                entry.end_time,
                translated_lines
            )
            translated_entries.append(new_entry)

        return translated_entries

    def format_time(self, timestamp):
        """
        Convert a TimeStamp to a nice display format.

        Args:
            timestamp: TimeStamp object

        Returns:
            String like "00:01:30.500"
        """
        hours = f"{timestamp.hours:02d}"
        minutes = f"{timestamp.minutes:02d}"
        seconds = f"{timestamp.seconds:02d}"
        ms = f"{timestamp.milliseconds:03d}"
        return f"{hours}:{minutes}:{seconds}.{ms}"
