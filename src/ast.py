"""Data structures for the SRT subtitle interpreter."""

TOKEN_INDEX = "INDEX"
TOKEN_TIMESTAMP = "TIMESTAMP"
TOKEN_ARROW = "ARROW"
TOKEN_TEXT = "TEXT"
TOKEN_NEWLINE = "NEWLINE"
TOKEN_BLANK_LINE = "BLANK_LINE"
TOKEN_EOF = "EOF"


class Token:
    def __init__(self, type, value, line_number=0):
        self.type = type
        self.value = value
        self.line_number = line_number

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"


class TimeStamp:
    def __init__(self, hours, minutes, seconds, milliseconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    def from_string(timestamp_str):
        time_part, ms_part = timestamp_str.split(',')
        hours_str, minutes_str, seconds_str = time_part.split(':')

        hours = int(hours_str)
        minutes = int(minutes_str)
        seconds = int(seconds_str)
        milliseconds = int(ms_part)

        if minutes > 59 or seconds > 59 or milliseconds > 999:
            raise ValueError(f"Invalid time: {timestamp_str}")

        return TimeStamp(hours, minutes, seconds, milliseconds)

    def to_milliseconds(self):
        total = 0
        total += self.hours * 3600000
        total += self.minutes * 60000
        total += self.seconds * 1000
        total += self.milliseconds
        return total

    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d},{self.milliseconds:03d}"

    def is_before(self, other):
        return self.to_milliseconds() < other.to_milliseconds()


class SubtitleEntry:
    def __init__(self, index, start_time, end_time, text):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def validate(self):
        if self.index < 1:
            raise ValueError(f"Index must be positive, got {self.index}")

        if not self.start_time.is_before(self.end_time):
            raise ValueError(f"Start time must be before end time for subtitle {self.index}")

        if not self.text or all(line.strip() == '' for line in self.text):
            raise ValueError(f"Subtitle {self.index} has no text")

    def get_text(self):
        return '\n'.join(self.text)

    def __str__(self):
        text_preview = self.get_text()[:40]
        if len(self.get_text()) > 40:
            text_preview += "..."
        return f"Subtitle {self.index}: {self.start_time} to {self.end_time} - '{text_preview}'"
