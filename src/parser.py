"""
Parser for SRT subtitle files.

This module takes a token stream from the Lexer and builds an Abstract Syntax Tree
(AST) consisting of validated SubtitleEntry objects.
"""

from typing import List
from src.lexer import Token, TOKEN_INDEX, TOKEN_TIMESTAMP, TOKEN_ARROW, TOKEN_TEXT, TOKEN_NEWLINE, TOKEN_BLANK_LINE, TOKEN_EOF
from src.ast_nodes import TimeStamp, SubtitleEntry


class ParserError(Exception):
    """Exception raised for parsing errors."""
    pass


class Parser:
    """
    Parser for SRT subtitle files.

    Implements the grammar:
        subtitle_file := subtitle_block+
        subtitle_block := INDEX NEWLINE timestamp_line NEWLINE text_lines BLANK_LINE
        timestamp_line := TIMESTAMP ARROW TIMESTAMP
        text_lines := TEXT (NEWLINE TEXT)*
    """

    def __init__(self, tokens: List[Token]):
        """
        Initialize parser with a token stream.

        Args:
            tokens: List of tokens from the Lexer
        """
        self.tokens = tokens
        self.current_pos = 0
        self.current_token = self.tokens[0] if self.tokens else None

    def parse(self) -> List[SubtitleEntry]:
        """
        Parse the token stream into a list of SubtitleEntry objects.

        Returns:
            List of validated SubtitleEntry objects

        Raises:
            ParserError: If parsing or validation fails
        """
        entries = []
        expected_index = 1

        while self.current_token and self.current_token.type != TOKEN_EOF:
            # Skip any leading blank lines
            if self.current_token.type == TOKEN_BLANK_LINE:
                self._advance()
                continue

            entry = self._parse_subtitle_block(expected_index)
            entries.append(entry)
            expected_index += 1

        if not entries:
            raise ParserError("No subtitle entries found in file")

        return entries

    def _parse_subtitle_block(self, expected_index: int) -> SubtitleEntry:
        """
        Parse a single subtitle block.

        Args:
            expected_index: The expected sequential index number

        Returns:
            SubtitleEntry object

        Raises:
            ParserError: If block structure is invalid
        """
        # Parse INDEX
        index = self._parse_index(expected_index)

        # Expect NEWLINE after index
        self._expect(TOKEN_NEWLINE)

        # Parse timestamp line
        start_time, end_time = self._parse_timestamp_line()

        # Expect NEWLINE after timestamp line
        self._expect(TOKEN_NEWLINE)

        # Parse text lines
        text_lines = self._parse_text_lines()

        # Expect BLANK_LINE after text
        self._expect(TOKEN_BLANK_LINE)

        # Create and validate entry
        entry = SubtitleEntry(
            index=index,
            start_time=start_time,
            end_time=end_time,
            text=text_lines
        )

        try:
            entry.validate()
        except ValueError as e:
            raise ParserError(f"Validation error for subtitle {index}: {e}")

        return entry

    def _parse_index(self, expected_index: int) -> int:
        """
        Parse and validate subtitle index.

        Args:
            expected_index: Expected sequential index number

        Returns:
            Parsed index value

        Raises:
            ParserError: If index is missing or not sequential
        """
        if not self.current_token or self.current_token.type != TOKEN_INDEX:
            raise ParserError(
                f"Expected subtitle index {expected_index}, "
                f"but got {self.current_token.type if self.current_token else 'EOF'}"
            )

        index = int(self.current_token.value)

        # Validate sequential ordering
        if index != expected_index:
            raise ParserError(
                f"Expected subtitle index {expected_index}, but got {index}. "
                f"Indices must be sequential (1, 2, 3...)"
            )

        self._advance()
        return index

    def _parse_timestamp_line(self) -> tuple[TimeStamp, TimeStamp]:
        """
        Parse timestamp line (TIMESTAMP ARROW TIMESTAMP).

        Returns:
            Tuple of (start_time, end_time)

        Raises:
            ParserError: If timestamp line is malformed
        """
        # Parse start timestamp
        if not self.current_token or self.current_token.type != TOKEN_TIMESTAMP:
            raise ParserError(
                f"Expected start timestamp, got {self.current_token.type if self.current_token else 'EOF'}"
            )

        try:
            start_time = TimeStamp.from_string(self.current_token.value)
        except ValueError as e:
            raise ParserError(f"Invalid start timestamp: {e}")

        self._advance()

        # Expect arrow
        self._expect(TOKEN_ARROW)

        # Parse end timestamp
        if not self.current_token or self.current_token.type != TOKEN_TIMESTAMP:
            raise ParserError(
                f"Expected end timestamp, got {self.current_token.type if self.current_token else 'EOF'}"
            )

        try:
            end_time = TimeStamp.from_string(self.current_token.value)
        except ValueError as e:
            raise ParserError(f"Invalid end timestamp: {e}")

        self._advance()

        # Validate time ordering
        if start_time >= end_time:
            raise ParserError(
                f"Start time ({start_time}) must be before end time ({end_time})"
            )

        return start_time, end_time

    def _parse_text_lines(self) -> List[str]:
        """
        Parse text lines (TEXT (NEWLINE TEXT)*).

        Returns:
            List of text lines

        Raises:
            ParserError: If no text content is found
        """
        text_lines = []

        # Expect at least one TEXT token
        if not self.current_token or self.current_token.type != TOKEN_TEXT:
            raise ParserError("Expected text content for subtitle")

        while self.current_token and self.current_token.type == TOKEN_TEXT:
            text_lines.append(self.current_token.value)
            self._advance()

            # If there's a NEWLINE and then more TEXT, continue
            if self.current_token and self.current_token.type == TOKEN_NEWLINE:
                self._advance()
            else:
                break

        if not text_lines:
            raise ParserError("Subtitle has no text content")

        return text_lines

    def _expect(self, expected_type: str) -> None:
        """
        Expect a specific token type and advance.

        Args:
            expected_type: Expected token type

        Raises:
            ParserError: If current token doesn't match expected type
        """
        if not self.current_token or self.current_token.type != expected_type:
            raise ParserError(
                f"Expected {expected_type}, "
                f"got {self.current_token.type if self.current_token else 'EOF'}"
            )
        self._advance()

    def _advance(self) -> None:
        """Move to the next token."""
        self.current_pos += 1
        if self.current_pos < len(self.tokens):
            self.current_token = self.tokens[self.current_pos]
        else:
            self.current_token = None
