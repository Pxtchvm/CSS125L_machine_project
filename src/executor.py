"""
Executor for SRT subtitle files.

This module executes subtitle display in time-synchronized manner with
support for multiple execution modes.
"""

import time
from typing import List
from src.ast_nodes import SubtitleEntry, TimeStamp


class ExecutorError(Exception):
    """Exception raised for execution errors."""
    pass


class Executor:
    """
    Executor for subtitle display.

    Supports three execution modes:
    - real_time: Display at actual timestamps
    - accelerated: Display with speed multiplier
    - sequential: Display one after another with brief pause
    """

    def __init__(self):
        self.start_time = None

    def execute(self, entries: List[SubtitleEntry], mode: str = "sequential", speed_factor: float = 1.0) -> None:
        """
        Execute subtitle display.

        Args:
            entries: List of validated SubtitleEntry objects
            mode: Execution mode ("real_time", "accelerated", or "sequential")
            speed_factor: Speed multiplier for accelerated mode (e.g., 2.0 = 2x speed)

        Raises:
            ExecutorError: If execution fails or mode is invalid
        """
        if not entries:
            raise ExecutorError("No subtitle entries to execute")

        if mode not in ["real_time", "accelerated", "sequential"]:
            raise ExecutorError(f"Invalid execution mode '{mode}'. Must be 'real_time', 'accelerated', or 'sequential'")

        if speed_factor <= 0:
            raise ExecutorError(f"Speed factor must be positive, got {speed_factor}")

        # Execute based on mode
        if mode == "sequential":
            self._execute_sequential(entries)
        elif mode == "real_time":
            self._execute_real_time(entries)
        elif mode == "accelerated":
            self._execute_accelerated(entries, speed_factor)

    def _execute_sequential(self, entries: List[SubtitleEntry]) -> None:
        """
        Execute subtitles sequentially with brief pause between each.

        Args:
            entries: List of SubtitleEntry objects
        """
        PAUSE_DURATION = 0.5  # seconds between subtitles

        for entry in entries:
            # Display subtitle
            display_time = self._format_timestamp(entry.start_time)
            text = entry.get_text()
            print(f"[{display_time}] DISPLAY: \"{text}\"")

            # Brief pause
            time.sleep(PAUSE_DURATION)

            # Clear subtitle
            clear_time = self._format_timestamp(entry.end_time)
            print(f"[{clear_time}] CLEAR")

            # Brief pause before next subtitle
            time.sleep(PAUSE_DURATION)

    def _execute_real_time(self, entries: List[SubtitleEntry]) -> None:
        """
        Execute subtitles at actual timestamps.

        Args:
            entries: List of SubtitleEntry objects
        """
        self.start_time = time.time()
        first_subtitle_time = entries[0].start_time.to_milliseconds()

        for entry in entries:
            # Calculate when this subtitle should appear
            subtitle_start_ms = entry.start_time.to_milliseconds()
            subtitle_end_ms = entry.end_time.to_milliseconds()
            duration_ms = subtitle_end_ms - subtitle_start_ms

            # Wait until it's time to display this subtitle
            wait_until_start = (subtitle_start_ms - first_subtitle_time) / 1000.0
            self._wait_until(wait_until_start)

            # Display subtitle
            display_time = self._format_timestamp(entry.start_time)
            text = entry.get_text()
            print(f"[{display_time}] DISPLAY: \"{text}\"")

            # Wait for subtitle duration
            time.sleep(duration_ms / 1000.0)

            # Clear subtitle
            clear_time = self._format_timestamp(entry.end_time)
            print(f"[{clear_time}] CLEAR")

    def _execute_accelerated(self, entries: List[SubtitleEntry], speed_factor: float) -> None:
        """
        Execute subtitles with accelerated timing.

        Args:
            entries: List of SubtitleEntry objects
            speed_factor: Speed multiplier (e.g., 2.0 = 2x speed)
        """
        self.start_time = time.time()
        first_subtitle_time = entries[0].start_time.to_milliseconds()

        for entry in entries:
            # Calculate when this subtitle should appear (accelerated)
            subtitle_start_ms = entry.start_time.to_milliseconds()
            subtitle_end_ms = entry.end_time.to_milliseconds()
            duration_ms = subtitle_end_ms - subtitle_start_ms

            # Wait until it's time to display this subtitle (accelerated)
            wait_until_start = (subtitle_start_ms - first_subtitle_time) / 1000.0 / speed_factor
            self._wait_until(wait_until_start)

            # Display subtitle
            display_time = self._format_timestamp(entry.start_time)
            text = entry.get_text()
            print(f"[{display_time}] DISPLAY: \"{text}\"")

            # Wait for subtitle duration (accelerated)
            time.sleep((duration_ms / 1000.0) / speed_factor)

            # Clear subtitle
            clear_time = self._format_timestamp(entry.end_time)
            print(f"[{clear_time}] CLEAR")

    def _wait_until(self, target_elapsed: float) -> None:
        """
        Wait until the target elapsed time from start.

        Args:
            target_elapsed: Target elapsed seconds from execution start
        """
        current_elapsed = time.time() - self.start_time
        wait_time = target_elapsed - current_elapsed

        if wait_time > 0:
            time.sleep(wait_time)

    def _format_timestamp(self, timestamp: TimeStamp) -> str:
        """
        Format a TimeStamp for display output.

        Args:
            timestamp: TimeStamp object

        Returns:
            Formatted string in HH:MM:SS.mmm format
        """
        return f"{timestamp.hours:02d}:{timestamp.minutes:02d}:{timestamp.seconds:02d}.{timestamp.milliseconds:03d}"
