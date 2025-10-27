"""Lexer - breaks SRT file text into tokens."""

import re
from src.ast import Token, TOKEN_INDEX, TOKEN_TIMESTAMP, TOKEN_ARROW
from src.ast import TOKEN_TEXT, TOKEN_NEWLINE, TOKEN_BLANK_LINE, TOKEN_EOF


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self):
        self.timestamp_pattern = re.compile(r'^\d{2}:\d{2}:\d{2},\d{3}$')
        self.index_pattern = re.compile(r'^\d+$')
        self.tokens = []
        self.line_number = 0

    def tokenize(self, text):
        self.tokens = []
        self.line_number = 0
        lines = text.split('\n')

        for i in range(len(lines)):
            self.line_number = i + 1
            line = lines[i]
            self.process_line(line)

        self.tokens.append(Token(TOKEN_EOF, "", self.line_number))
        return self.tokens

    def process_line(self, line):
        if self.is_blank(line):
            self.tokens.append(Token(TOKEN_BLANK_LINE, line, self.line_number))
            return

        stripped = line.strip()
        if self.index_pattern.match(stripped):
            self.tokens.append(Token(TOKEN_INDEX, stripped, self.line_number))
            self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))
            return

        if '-->' in line:
            self.process_timestamp_line(line)
            return

        if stripped != '':
            self.tokens.append(Token(TOKEN_TEXT, line, self.line_number))
            self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))

    def process_timestamp_line(self, line):
        parts = line.split()

        if len(parts) != 3:
            raise LexerError(f"Line {self.line_number}: Bad timestamp line")

        start_time = parts[0]
        arrow = parts[1]
        end_time = parts[2]

        if not self.timestamp_pattern.match(start_time):
            raise LexerError(f"Line {self.line_number}: Bad start time '{start_time}'")

        if arrow != '-->':
            raise LexerError(f"Line {self.line_number}: Expected '-->', got '{arrow}'")

        if not self.timestamp_pattern.match(end_time):
            raise LexerError(f"Line {self.line_number}: Bad end time '{end_time}'")

        self.tokens.append(Token(TOKEN_TIMESTAMP, start_time, self.line_number))
        self.tokens.append(Token(TOKEN_ARROW, arrow, self.line_number))
        self.tokens.append(Token(TOKEN_TIMESTAMP, end_time, self.line_number))
        self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))

    def is_blank(self, line):
        return line.strip() == ''
