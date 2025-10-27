"""Parser - takes tokens and builds subtitle entries."""

from src.ast import TimeStamp, SubtitleEntry
from src.ast import TOKEN_INDEX, TOKEN_TIMESTAMP, TOKEN_ARROW, TOKEN_TEXT
from src.ast import TOKEN_NEWLINE, TOKEN_BLANK_LINE, TOKEN_EOF


class ParserError(Exception):
    pass


class Parser:
    """Reads tokens and creates subtitle entries."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current = tokens[0] if tokens else None

    def parse(self):
        entries = []
        expected_index = 1

        while self.current and self.current.type != TOKEN_EOF:
            if self.current.type == TOKEN_BLANK_LINE:
                self.move_next()
                continue

            entry = self.parse_subtitle(expected_index)
            entries.append(entry)
            expected_index += 1

        if len(entries) == 0:
            raise ParserError("No subtitles found in file")

        return entries

    def parse_subtitle(self, expected_index):
        if not self.current or self.current.type != TOKEN_INDEX:
            raise ParserError(f"Expected subtitle number {expected_index}")

        index = int(self.current.value)

        if index != expected_index:
            raise ParserError(f"Expected subtitle {expected_index}, got {index}")

        self.move_next()
        self.expect(TOKEN_NEWLINE)

        start_time, end_time = self.parse_timestamps()
        self.expect(TOKEN_NEWLINE)

        text_lines = self.parse_text()
        self.expect(TOKEN_BLANK_LINE)

        entry = SubtitleEntry(index, start_time, end_time, text_lines)

        try:
            entry.validate()
        except ValueError as e:
            raise ParserError(f"Subtitle {index} is invalid: {e}")

        return entry

    def parse_timestamps(self):
        if not self.current or self.current.type != TOKEN_TIMESTAMP:
            raise ParserError("Expected start time")

        start_str = self.current.value
        try:
            start_time = TimeStamp.from_string(start_str)
        except ValueError as e:
            raise ParserError(f"Bad start time: {e}")

        self.move_next()
        self.expect(TOKEN_ARROW)

        if not self.current or self.current.type != TOKEN_TIMESTAMP:
            raise ParserError("Expected end time")

        end_str = self.current.value
        try:
            end_time = TimeStamp.from_string(end_str)
        except ValueError as e:
            raise ParserError(f"Bad end time: {e}")

        self.move_next()

        if not start_time.is_before(end_time):
            raise ParserError(f"Start time {start_time} must be before end time {end_time}")

        return start_time, end_time

    def parse_text(self):
        text_lines = []

        if not self.current or self.current.type != TOKEN_TEXT:
            raise ParserError("Subtitle needs text")

        while self.current and self.current.type == TOKEN_TEXT:
            text_lines.append(self.current.value)
            self.move_next()

            if self.current and self.current.type == TOKEN_NEWLINE:
                self.move_next()
            else:
                break

        return text_lines

    def expect(self, token_type):
        if not self.current or self.current.type != token_type:
            current_type = self.current.type if self.current else 'end of file'
            raise ParserError(f"Expected {token_type}, got {current_type}")
        self.move_next()

    def move_next(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current = self.tokens[self.position]
        else:
            self.current = None
