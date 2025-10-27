"""Executor - displays subtitles and handles translation."""

import time


class ExecutorError(Exception):
    pass


class Executor:
    def execute(self, entries, translate_to=None):
        if not entries:
            raise ExecutorError("No subtitles to display")

        if translate_to and translate_to.lower() != 'english':
            print(f"\nTranslating to {translate_to}...")
            entries = self.translate_subtitles(entries, translate_to)
            print("Translation complete!                    \n")

        for entry in entries:
            start_time = self.format_time(entry.start_time)
            text = entry.get_text()
            print(f"[{start_time}] DISPLAY: \"{text}\"")

            time.sleep(0.5)

            end_time = self.format_time(entry.end_time)
            print(f"[{end_time}] CLEAR")

            time.sleep(0.5)

    def translate_subtitles(self, entries, target_language):
        try:
            from deep_translator import GoogleTranslator
        except ImportError:
            raise ExecutorError("Translation library not installed. Run: pip install deep-translator")

        language_codes = {
            'filipino': 'tl',
            'tagalog': 'tl',
            'korean': 'ko',
            'chinese': 'zh-CN',
            'japanese': 'ja',
            'english': 'en'
        }

        target_code = language_codes.get(target_language.lower())
        if not target_code:
            raise ExecutorError(f"Language '{target_language}' not supported")

        translator = GoogleTranslator(source='en', target=target_code)

        translated_entries = []
        for i, entry in enumerate(entries):
            print(f"  Translating subtitle {i + 1}/{len(entries)}...", end='\r')

            translated_lines = []
            for line in entry.text:
                try:
                    translated = translator.translate(line)
                    translated_lines.append(translated)
                except Exception as e:
                    print(f"\n  Warning: Could not translate line, keeping original")
                    translated_lines.append(line)

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
        hours = f"{timestamp.hours:02d}"
        minutes = f"{timestamp.minutes:02d}"
        seconds = f"{timestamp.seconds:02d}"
        ms = f"{timestamp.milliseconds:03d}"
        return f"{hours}:{minutes}:{seconds}.{ms}"
