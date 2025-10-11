"""
Statistics calculation for SRT subtitle files.

This module provides functionality to analyze subtitle files and generate
comprehensive statistics about timing, text length, and distribution.
"""

from dataclasses import dataclass
from typing import List, Tuple
from src.ast_nodes import SubtitleEntry


@dataclass
class SubtitleStats:
    """
    Container for subtitle file statistics.

    Attributes:
        total_entries: Total number of subtitle entries
        total_duration_ms: Total duration from first start to last end (milliseconds)
        avg_duration_ms: Average subtitle display duration (milliseconds)
        avg_char_length: Average text length in characters
        avg_word_length: Average text length in words
        longest_by_duration: Tuple of (entry_index, duration_ms, text_preview)
        shortest_by_duration: Tuple of (entry_index, duration_ms, text_preview)
        longest_by_text: Tuple of (entry_index, char_count, text_preview)
        shortest_by_text: Tuple of (entry_index, char_count, text_preview)
    """
    total_entries: int
    total_duration_ms: int
    avg_duration_ms: float
    avg_char_length: float
    avg_word_length: float
    longest_by_duration: Tuple[int, int, str]
    shortest_by_duration: Tuple[int, int, str]
    longest_by_text: Tuple[int, int, str]
    shortest_by_text: Tuple[int, int, str]

    def format_duration(self, ms: int) -> str:
        """
        Format milliseconds as HH:MM:SS.mmm.

        Args:
            ms: Milliseconds to format

        Returns:
            Formatted duration string
        """
        hours = ms // 3600000
        ms %= 3600000
        minutes = ms // 60000
        ms %= 60000
        seconds = ms // 1000
        milliseconds = ms % 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    def to_string(self) -> str:
        """
        Generate a formatted string representation of the statistics.

        Returns:
            Multi-line formatted statistics report
        """
        lines = [
            "Subtitle Statistics:",
            "=" * 60,
            f"Total entries: {self.total_entries}",
            f"Total duration: {self.format_duration(self.total_duration_ms)}",
            f"Average subtitle duration: {self.avg_duration_ms / 1000:.2f}s",
            f"Average text length: {self.avg_char_length:.1f} characters, {self.avg_word_length:.1f} words",
            "",
            "Longest subtitle by duration:",
            f"  Entry #{self.longest_by_duration[0]}: {self.longest_by_duration[1] / 1000:.2f}s",
            f"  Text: \"{self.longest_by_duration[2]}\"",
            "",
            "Shortest subtitle by duration:",
            f"  Entry #{self.shortest_by_duration[0]}: {self.shortest_by_duration[1] / 1000:.2f}s",
            f"  Text: \"{self.shortest_by_duration[2]}\"",
            "",
            "Longest subtitle by text length:",
            f"  Entry #{self.longest_by_text[0]}: {self.longest_by_text[1]} characters",
            f"  Text: \"{self.longest_by_text[2]}\"",
            "",
            "Shortest subtitle by text length:",
            f"  Entry #{self.shortest_by_text[0]}: {self.shortest_by_text[1]} characters",
            f"  Text: \"{self.shortest_by_text[2]}\"",
        ]
        return "\n".join(lines)


class StatisticsError(Exception):
    """Exception raised when statistics calculation fails."""
    pass


def calculate_statistics(entries: List[SubtitleEntry]) -> SubtitleStats:
    """
    Calculate comprehensive statistics for a list of subtitle entries.

    Args:
        entries: List of validated SubtitleEntry objects

    Returns:
        SubtitleStats object containing calculated statistics

    Raises:
        StatisticsError: If entries list is empty or invalid
    """
    if not entries:
        raise StatisticsError("Cannot calculate statistics: entries list is empty")

    # Total entries
    total_entries = len(entries)

    # Total duration (first start to last end)
    first_start_ms = entries[0].start_time.to_milliseconds()
    last_end_ms = entries[-1].end_time.to_milliseconds()
    total_duration_ms = last_end_ms - first_start_ms

    # Calculate per-entry statistics
    durations = []
    char_lengths = []
    word_lengths = []

    for entry in entries:
        # Duration
        duration_ms = entry.end_time.to_milliseconds() - entry.start_time.to_milliseconds()
        durations.append((entry.index, duration_ms, entry.get_text()))

        # Text length
        full_text = entry.get_text()
        char_count = len(full_text)
        word_count = len(full_text.split())
        char_lengths.append((entry.index, char_count, full_text))
        word_lengths.append(word_count)

    # Average duration
    avg_duration_ms = sum(d[1] for d in durations) / total_entries

    # Average text lengths
    avg_char_length = sum(c[1] for c in char_lengths) / total_entries
    avg_word_length = sum(word_lengths) / total_entries

    # Find longest and shortest by duration
    longest_by_duration = max(durations, key=lambda x: x[1])
    shortest_by_duration = min(durations, key=lambda x: x[1])

    # Find longest and shortest by text length
    longest_by_text = max(char_lengths, key=lambda x: x[1])
    shortest_by_text = min(char_lengths, key=lambda x: x[1])

    # Truncate text previews to 80 characters
    def truncate_text(text: str, max_len: int = 80) -> str:
        if len(text) > max_len:
            return text[:max_len] + "..."
        return text

    # Create tuples with truncated text
    longest_duration_tuple = (
        longest_by_duration[0],
        longest_by_duration[1],
        truncate_text(longest_by_duration[2])
    )
    shortest_duration_tuple = (
        shortest_by_duration[0],
        shortest_by_duration[1],
        truncate_text(shortest_by_duration[2])
    )
    longest_text_tuple = (
        longest_by_text[0],
        longest_by_text[1],
        truncate_text(longest_by_text[2])
    )
    shortest_text_tuple = (
        shortest_by_text[0],
        shortest_by_text[1],
        truncate_text(shortest_by_text[2])
    )

    return SubtitleStats(
        total_entries=total_entries,
        total_duration_ms=total_duration_ms,
        avg_duration_ms=avg_duration_ms,
        avg_char_length=avg_char_length,
        avg_word_length=avg_word_length,
        longest_by_duration=longest_duration_tuple,
        shortest_by_duration=shortest_duration_tuple,
        longest_by_text=longest_text_tuple,
        shortest_by_text=shortest_text_tuple,
    )
