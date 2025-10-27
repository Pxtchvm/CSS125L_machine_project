"""
Parser - takes tokens and builds subtitle entries.
Checks if everything is in the right order and makes sense.
"""

from src.ast import TimeStamp, SubtitleEntry
from src.ast import TOKEN_INDEX, TOKEN_TIMESTAMP, TOKEN_ARROW, TOKEN_TEXT
from src.ast import TOKEN_NEWLINE, TOKEN_BLANK_LINE, TOKEN_EOF


class ParserError(Exception):
    """Error when the file structure is wrong"""
    pass


class Parser:
    """
    Reads through tokens and creates subtitle entries.

    Expected structure for each subtitle:
    - Index number (like 1, 2, 3)
    - Timestamp line (00:00:01,000 --> 00:00:03,000)
    - One or more lines of text
    - A blank line
    """

    def __init__(self, tokens):
        self.tokens = tokens  # list of all tokens
        self.position = 0  # where we are in the list
        self.current = tokens[0] if tokens else None  # current token

    def parse(self):
        """Go through all tokens and build subtitle entries"""
        entries = []
        expected_index = 1  # subtitles should be numbered 1, 2, 3, ...

        # Keep going until we hit the end
        while self.current and self.current.type != TOKEN_EOF:
            # Skip blank lines at the start
            if self.current.type == TOKEN_BLANK_LINE:
                self.move_next()
                continue

            # Parse one subtitle
            entry = self.parse_subtitle(expected_index)
            entries.append(entry)
            expected_index += 1

        # Make sure we found at least one subtitle
        if len(entries) == 0:
            raise ParserError("No subtitles found in file")

        return entries

    def parse_subtitle(self, expected_index):
        """Parse one complete subtitle entry"""

        # Step 1: Get the index number
        if not self.current or self.current.type != TOKEN_INDEX:
            raise ParserError(f"Expected subtitle number {expected_index}")

        index = int(self.current.value)

        # Check if it's the right number (sequential)
        if index != expected_index:
            raise ParserError(f"Expected subtitle {expected_index}, got {index}")

        self.move_next()

        # Step 2: Expect a newline after the index
        self.expect(TOKEN_NEWLINE)

        # Step 3: Get the timestamps
        start_time, end_time = self.parse_timestamps()

        # Step 4: Expect a newline after timestamps
        self.expect(TOKEN_NEWLINE)

        # Step 5: Get the text lines
        text_lines = self.parse_text()

        # Step 6: Expect a blank line at the end
        self.expect(TOKEN_BLANK_LINE)

        # Create the subtitle entry
        entry = SubtitleEntry(index, start_time, end_time, text_lines)

        # Make sure it's valid
        try:
            entry.validate()
        except ValueError as e:
            raise ParserError(f"Subtitle {index} is invalid: {e}")

        return entry

    def parse_timestamps(self):
        """Parse the timestamp line: start --> end"""

        # Get start timestamp
        if not self.current or self.current.type != TOKEN_TIMESTAMP:
            raise ParserError("Expected start time")

        start_str = self.current.value
        try:
            start_time = TimeStamp.from_string(start_str)
        except ValueError as e:
            raise ParserError(f"Bad start time: {e}")

        self.move_next()

        # Expect the arrow
        self.expect(TOKEN_ARROW)

        # Get end timestamp
        if not self.current or self.current.type != TOKEN_TIMESTAMP:
            raise ParserError("Expected end time")

        end_str = self.current.value
        try:
            end_time = TimeStamp.from_string(end_str)
        except ValueError as e:
            raise ParserError(f"Bad end time: {e}")

        self.move_next()

        # Make sure start is before end
        if not start_time.is_before(end_time):
            raise ParserError(f"Start time {start_time} must be before end time {end_time}")

        return start_time, end_time

    def parse_text(self):
        """Parse the subtitle text lines"""
        text_lines = []

        # Should have at least one line of text
        if not self.current or self.current.type != TOKEN_TEXT:
            raise ParserError("Subtitle needs text")

        # Collect all text lines
        while self.current and self.current.type == TOKEN_TEXT:
            text_lines.append(self.current.value)
            self.move_next()

            # Move past newline if there is one
            if self.current and self.current.type == TOKEN_NEWLINE:
                self.move_next()
            else:
                break

        return text_lines

    def expect(self, token_type):
        """Make sure current token is the type we expect"""
        if not self.current or self.current.type != token_type:
            current_type = self.current.type if self.current else 'end of file'
            raise ParserError(f"Expected {token_type}, got {current_type}")
        self.move_next()

    def move_next(self):
        """Move to the next token"""
        self.position += 1
        if self.position < len(self.tokens):
            self.current = self.tokens[self.position]
        else:
            self.current = None
