"""
Lexer for SRT (SubRip Text) subtitle files.

This module tokenizes raw .srt file content into a stream of tokens
that can be processed by the parser.
"""

import re
from dataclasses import dataclass
from typing import List, Optional


# Token type constants
TOKEN_INDEX = "INDEX"
TOKEN_TIMESTAMP = "TIMESTAMP"
TOKEN_ARROW = "ARROW"
TOKEN_TEXT = "TEXT"
TOKEN_FORMATTING_TAG = "FORMATTING_TAG"
TOKEN_NEWLINE = "NEWLINE"
TOKEN_BLANK_LINE = "BLANK_LINE"
TOKEN_EOF = "EOF"


@dataclass
class Token:
    """Represents a single lexical token."""
    type: str
    value: str
    line_number: int = 0

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


class LexerError(Exception):
    """Exception raised for lexical analysis errors."""
    pass


class Lexer:
    """
    Lexer for .srt subtitle files.

    Converts raw text into a stream of tokens for parsing.
    """

    # Regex patterns for token matching
    TIMESTAMP_PATTERN = re.compile(r'^\d{2}:\d{2}:\d{2},\d{3}$')
    ARROW_PATTERN = re.compile(r'^-->$')
    INDEX_PATTERN = re.compile(r'^\d+$')
    FORMATTING_TAG_PATTERN = re.compile(r'</?[a-z]+[^>]*>')

    def __init__(self):
        self.tokens: List[Token] = []
        self.line_number = 0

    def tokenize(self, text: str) -> List[Token]:
        """
        Tokenize the input text into a list of tokens.

        Args:
            text: Raw .srt file content

        Returns:
            List of Token objects

        Raises:
            LexerError: If malformed tokens are encountered
        """
        self.tokens = []
        self.line_number = 0

        lines = text.split('\n')

        for i, line in enumerate(lines):
            self.line_number = i + 1
            self._process_line(line)

        # Add EOF token at the end
        self.tokens.append(Token(TOKEN_EOF, "", self.line_number))

        return self.tokens

    def _process_line(self, line: str) -> None:
        """Process a single line and generate tokens."""

        # Check for blank line (empty or whitespace only)
        if self._is_blank_line(line):
            self.tokens.append(Token(TOKEN_BLANK_LINE, line, self.line_number))
            return

        # Check for index (standalone number on a line)
        if self._match_index(line):
            self.tokens.append(Token(TOKEN_INDEX, line.strip(), self.line_number))
            self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))
            return

        # Check for timestamp line (contains -->)
        if '-->' in line:
            self._process_timestamp_line(line)
            return

        # Otherwise, it's text content
        self._process_text_line(line)

    def _process_timestamp_line(self, line: str) -> None:
        """Process a line containing timestamps and arrow."""
        parts = line.split()

        if len(parts) != 3:
            raise LexerError(
                f"Line {self.line_number}: Invalid timestamp line format. "
                f"Expected 'HH:MM:SS,mmm --> HH:MM:SS,mmm'"
            )

        start_time, arrow, end_time = parts

        # Validate start timestamp
        if not self.TIMESTAMP_PATTERN.match(start_time):
            raise LexerError(
                f"Line {self.line_number}: Invalid start timestamp format '{start_time}'. "
                f"Expected HH:MM:SS,mmm"
            )

        # Validate arrow
        if not self.ARROW_PATTERN.match(arrow):
            raise LexerError(
                f"Line {self.line_number}: Invalid arrow '{arrow}'. Expected '-->'."
            )

        # Validate end timestamp
        if not self.TIMESTAMP_PATTERN.match(end_time):
            raise LexerError(
                f"Line {self.line_number}: Invalid end timestamp format '{end_time}'. "
                f"Expected HH:MM:SS,mmm"
            )

        # Add tokens
        self.tokens.append(Token(TOKEN_TIMESTAMP, start_time, self.line_number))
        self.tokens.append(Token(TOKEN_ARROW, arrow, self.line_number))
        self.tokens.append(Token(TOKEN_TIMESTAMP, end_time, self.line_number))
        self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))

    def _process_text_line(self, line: str) -> None:
        """Process a text content line, detecting formatting tags."""
        # For now, treat the entire line as text
        # In a more advanced implementation, we could tokenize formatting tags separately
        stripped = line.strip()

        if stripped:
            # Check if line contains formatting tags
            if self.FORMATTING_TAG_PATTERN.search(line):
                self.tokens.append(Token(TOKEN_TEXT, line, self.line_number))
            else:
                self.tokens.append(Token(TOKEN_TEXT, line, self.line_number))

            self.tokens.append(Token(TOKEN_NEWLINE, '\n', self.line_number))

    def _is_blank_line(self, line: str) -> bool:
        """Check if a line is blank (empty or whitespace only)."""
        return len(line.strip()) == 0

    def _match_index(self, line: str) -> bool:
        """Check if a line matches the index pattern (standalone number)."""
        return bool(self.INDEX_PATTERN.match(line.strip()))

    def _match_timestamp(self, text: str) -> bool:
        """Check if text matches timestamp pattern."""
        return bool(self.TIMESTAMP_PATTERN.match(text.strip()))
