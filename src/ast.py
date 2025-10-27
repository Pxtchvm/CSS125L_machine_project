"""
Data structures for the SRT subtitle interpreter.
Contains all the classes and constants we need.
"""

# Token type constants - these tell us what kind of token we found
TOKEN_INDEX = "INDEX"
TOKEN_TIMESTAMP = "TIMESTAMP"
TOKEN_ARROW = "ARROW"
TOKEN_TEXT = "TEXT"
TOKEN_NEWLINE = "NEWLINE"
TOKEN_BLANK_LINE = "BLANK_LINE"
TOKEN_EOF = "EOF"


class Token:
    """A single piece of the SRT file (like a word in a sentence)"""

    def __init__(self, type, value, line_number=0):
        self.type = type  # what kind of token is this?
        self.value = value  # the actual text
        self.line_number = line_number  # which line in the file?

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"


class TimeStamp:
    """Represents a time like 00:01:30,500 (1 minute 30.5 seconds)"""

    def __init__(self, hours, minutes, seconds, milliseconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    def from_string(timestamp_str):
        """Convert a string like '00:01:30,500' into a TimeStamp object"""
        # Split by comma to get seconds and milliseconds
        time_part, ms_part = timestamp_str.split(',')

        # Split by colon to get hours, minutes, seconds
        hours_str, minutes_str, seconds_str = time_part.split(':')

        # Convert strings to numbers
        hours = int(hours_str)
        minutes = int(minutes_str)
        seconds = int(seconds_str)
        milliseconds = int(ms_part)

        # Check if the values make sense
        if minutes > 59 or seconds > 59 or milliseconds > 999:
            raise ValueError(f"Invalid time: {timestamp_str}")

        return TimeStamp(hours, minutes, seconds, milliseconds)

    def to_milliseconds(self):
        """Convert the time to total milliseconds (easier to compare)"""
        total = 0
        total += self.hours * 3600000  # hours to ms
        total += self.minutes * 60000  # minutes to ms
        total += self.seconds * 1000  # seconds to ms
        total += self.milliseconds
        return total

    def __str__(self):
        """Convert back to string format like 00:01:30,500"""
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d},{self.milliseconds:03d}"

    def is_before(self, other):
        """Check if this time comes before another time"""
        return self.to_milliseconds() < other.to_milliseconds()


class SubtitleEntry:
    """One subtitle with its index, timing, and text"""

    def __init__(self, index, start_time, end_time, text):
        self.index = index  # the number (1, 2, 3, ...)
        self.start_time = start_time  # when to show it
        self.end_time = end_time  # when to hide it
        self.text = text  # list of text lines

    def validate(self):
        """Make sure this subtitle makes sense"""
        # Index should be a positive number
        if self.index < 1:
            raise ValueError(f"Index must be positive, got {self.index}")

        # Start time should be before end time
        if not self.start_time.is_before(self.end_time):
            raise ValueError(f"Start time must be before end time for subtitle {self.index}")

        # Should have some text
        if not self.text or all(line.strip() == '' for line in self.text):
            raise ValueError(f"Subtitle {self.index} has no text")

    def get_text(self):
        """Get all the text as one string"""
        return '\n'.join(self.text)

    def __str__(self):
        """Show a summary of this subtitle"""
        text_preview = self.get_text()[:40]
        if len(self.get_text()) > 40:
            text_preview += "..."
        return f"Subtitle {self.index}: {self.start_time} to {self.end_time} - '{text_preview}'"
