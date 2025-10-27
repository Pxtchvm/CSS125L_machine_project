"""
Lexer - breaks up the SRT file text into tokens.
Think of it like breaking a sentence into words.
"""

import re
from src.ast import Token, TOKEN_INDEX, TOKEN_TIMESTAMP, TOKEN_ARROW
from src.ast import TOKEN_TEXT, TOKEN_NEWLINE, TOKEN_BLANK_LINE, TOKEN_EOF


class LexerError(Exception):
    """Error when we find something wrong in the file"""
    pass


class Lexer:
    """Reads the SRT file and breaks it into tokens"""

    def __init__(self):
        # Patterns to recognize different parts of the file
        self.timestamp_pattern = re.compile(r'^\d{2}:\d{2}:\d{2},\d{3}$')
        self.index_pattern = re.compile(r'^\d+$')
        self.tokens = []
        self.line_number = 0

    def tokenize(self, text):
        """Break the file text into a list of tokens"""
        self.tokens = []
        self.line_number = 0

        # Split the file into lines
        lines = text.split('\n')

        # Process each line
        for i in range(len(lines)):
            self.line_number = i + 1
            line = lines[i]
            self.process_line(line)

        # Add an end-of-file token at the end
        self.tokens.append(Token(TOKEN_EOF, "", self.line_number))

        return self.tokens

    def process_line(self, line):
        """Figure out what kind of line this is and create tokens"""

        # Is it a blank line?
        if self.is_blank(line):
            self.tokens.append(Token(TOKEN_BLANK_LINE, line, self.line_number))
            return

        # Is it an index number?
        stripped = line.strip()
        if self.index_pattern.match(stripped):
            self.tokens.append(Token(TOKEN_INDEX, stripped, self.line_number))
            self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))
            return

        # Does it have timestamps with an arrow?
        if '-->' in line:
            self.process_timestamp_line(line)
            return

        # Otherwise it's text content
        if stripped != '':
            self.tokens.append(Token(TOKEN_TEXT, line, self.line_number))
            self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))

    def process_timestamp_line(self, line):
        """Handle a line like: 00:00:01,000 --> 00:00:03,000"""
        parts = line.split()

        # Should have exactly 3 parts: start, arrow, end
        if len(parts) != 3:
            raise LexerError(f"Line {self.line_number}: Bad timestamp line")

        start_time = parts[0]
        arrow = parts[1]
        end_time = parts[2]

        # Check if they look right
        if not self.timestamp_pattern.match(start_time):
            raise LexerError(f"Line {self.line_number}: Bad start time '{start_time}'")

        if arrow != '-->':
            raise LexerError(f"Line {self.line_number}: Expected '-->', got '{arrow}'")

        if not self.timestamp_pattern.match(end_time):
            raise LexerError(f"Line {self.line_number}: Bad end time '{end_time}'")

        # Create the tokens
        self.tokens.append(Token(TOKEN_TIMESTAMP, start_time, self.line_number))
        self.tokens.append(Token(TOKEN_ARROW, arrow, self.line_number))
        self.tokens.append(Token(TOKEN_TIMESTAMP, end_time, self.line_number))
        self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))

    def is_blank(self, line):
        """Check if a line is empty or just whitespace"""
        return line.strip() == ''
