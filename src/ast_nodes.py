"""
AST (Abstract Syntax Tree) node definitions for SRT subtitle files.

This module defines the data structures that represent parsed subtitle entries.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TimeStamp:
    """
    Represents a timestamp in SRT format (HH:MM:SS,mmm).

    Attributes:
        hours: Hours (0-99)
        minutes: Minutes (0-59)
        seconds: Seconds (0-59)
        milliseconds: Milliseconds (0-999)
    """
    hours: int
    minutes: int
    seconds: int
    milliseconds: int

    @classmethod
    def from_string(cls, timestamp_str: str) -> 'TimeStamp':
        """
        Parse a timestamp string into a TimeStamp object.

        Args:
            timestamp_str: Timestamp in format HH:MM:SS,mmm

        Returns:
            TimeStamp object

        Raises:
            ValueError: If timestamp format is invalid or values out of range
        """
        try:
            # Split by comma to separate seconds and milliseconds
            time_part, ms_part = timestamp_str.split(',')

            # Split time part by colon
            hours_str, minutes_str, seconds_str = time_part.split(':')

            hours = int(hours_str)
            minutes = int(minutes_str)
            seconds = int(seconds_str)
            milliseconds = int(ms_part)

            # Validate ranges
            if not (0 <= hours <= 99):
                raise ValueError(f"Hours must be between 0 and 99, got {hours}")
            if not (0 <= minutes <= 59):
                raise ValueError(f"Minutes must be between 0 and 59, got {minutes}")
            if not (0 <= seconds <= 59):
                raise ValueError(f"Seconds must be between 0 and 59, got {seconds}")
            if not (0 <= milliseconds <= 999):
                raise ValueError(f"Milliseconds must be between 0 and 999, got {milliseconds}")

            return cls(hours, minutes, seconds, milliseconds)

        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid timestamp format '{timestamp_str}': {e}")

    def to_milliseconds(self) -> int:
        """
        Convert timestamp to total milliseconds.

        Returns:
            Total milliseconds
        """
        return (
            self.hours * 3600000 +
            self.minutes * 60000 +
            self.seconds * 1000 +
            self.milliseconds
        )

    def __lt__(self, other: 'TimeStamp') -> bool:
        """Compare timestamps for ordering."""
        return self.to_milliseconds() < other.to_milliseconds()

    def __le__(self, other: 'TimeStamp') -> bool:
        """Compare timestamps for ordering."""
        return self.to_milliseconds() <= other.to_milliseconds()

    def __gt__(self, other: 'TimeStamp') -> bool:
        """Compare timestamps for ordering."""
        return self.to_milliseconds() > other.to_milliseconds()

    def __ge__(self, other: 'TimeStamp') -> bool:
        """Compare timestamps for ordering."""
        return self.to_milliseconds() >= other.to_milliseconds()

    def __str__(self) -> str:
        """String representation in SRT format."""
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d},{self.milliseconds:03d}"


@dataclass
class SubtitleEntry:
    """
    Represents a single subtitle entry in an SRT file.

    Attributes:
        index: Sequential subtitle number (1, 2, 3...)
        start_time: When subtitle should appear
        end_time: When subtitle should disappear
        text: List of text lines for this subtitle
        formatting: Optional formatting tags present in the text
    """
    index: int
    start_time: TimeStamp
    end_time: TimeStamp
    text: List[str]
    formatting: Optional[List[str]] = None

    def validate(self) -> None:
        """
        Validate the subtitle entry.

        Raises:
            ValueError: If validation fails
        """
        # Check index is positive
        if self.index < 1:
            raise ValueError(f"Index must be positive, got {self.index}")

        # Check start time is before end time
        if self.start_time >= self.end_time:
            raise ValueError(
                f"Start time ({self.start_time}) must be before end time ({self.end_time})"
            )

        # Check text is not empty
        if not self.text or all(not line.strip() for line in self.text):
            raise ValueError(f"Subtitle {self.index} has no text content")

    def get_text(self) -> str:
        """
        Get the full text content as a single string.

        Returns:
            All text lines joined with newlines
        """
        return '\n'.join(self.text)

    def __str__(self) -> str:
        """String representation showing key information."""
        text_preview = self.get_text()[:50]
        if len(self.get_text()) > 50:
            text_preview += "..."
        return f"SubtitleEntry({self.index}: {self.start_time} → {self.end_time}, '{text_preview}')"
