"""
Text and SRT export functionality for subtitle files.

This module provides functionality to export subtitle content as plain text
or as complete translated SRT files.
"""

from pathlib import Path
from typing import List
from src.ast_nodes import SubtitleEntry


class ExportError(Exception):
    """Exception raised when export operation fails."""
    pass


def export_to_text(
    entries: List[SubtitleEntry],
    output_path: str,
    format_type: str = "plain"
) -> None:
    """
    Export subtitle text content to a plain text file.

    Args:
        entries: List of SubtitleEntry objects
        output_path: Path where text file should be written
        format_type: Export format ("plain", "numbered", or "separated")
            - plain: Just the text content, one subtitle per line
            - numbered: Include entry index before each subtitle [1], [2], etc.
            - separated: Include blank lines between subtitles for readability

    Raises:
        ExportError: If export fails or format is invalid
    """
    if not entries:
        raise ExportError("Cannot export: entries list is empty")

    valid_formats = ["plain", "numbered", "separated"]
    if format_type not in valid_formats:
        raise ExportError(
            f"Invalid format type '{format_type}'. "
            f"Must be one of: {', '.join(valid_formats)}"
        )

    try:
        # Generate output content based on format
        lines = []

        for entry in entries:
            text_content = entry.get_text()

            if format_type == "plain":
                # Just the text, no metadata
                lines.append(text_content)

            elif format_type == "numbered":
                # Include entry index number
                lines.append(f"[{entry.index}] {text_content}")

            elif format_type == "separated":
                # Include blank line between entries
                lines.append(text_content)
                lines.append("")  # Blank line separator

        # Join all lines
        output_content = "\n".join(lines)

        # Remove trailing blank line for separated format
        if format_type == "separated" and output_content.endswith("\n\n"):
            output_content = output_content[:-1]

        # Write to file
        output_file = Path(output_path)

        # Create parent directories if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)

    except IOError as e:
        raise ExportError(f"Failed to write text file: {e}")
    except Exception as e:
        raise ExportError(f"Text export failed: {e}")


def export_to_srt(
    entries: List[SubtitleEntry],
    output_path: str
) -> None:
    """
    Export subtitles as a complete valid SRT file.

    This preserves all timing information and creates a properly formatted
    SRT file that can be used in video players.

    Args:
        entries: List of SubtitleEntry objects (can be translated)
        output_path: Path where .srt file should be written

    Raises:
        ExportError: If export fails
    """
    if not entries:
        raise ExportError("Cannot export: entries list is empty")

    try:
        # Build SRT content
        srt_blocks = []

        for entry in entries:
            # Build each subtitle block in SRT format:
            # Index
            # Start --> End
            # Text (can be multiple lines)
            # Blank line

            block_lines = [
                str(entry.index),
                f"{entry.start_time} --> {entry.end_time}",
            ]

            # Add text lines
            block_lines.extend(entry.text)

            # Join this block
            srt_blocks.append("\n".join(block_lines))

        # Join all blocks with blank lines
        output_content = "\n\n".join(srt_blocks)

        # SRT files should end with a blank line
        output_content += "\n"

        # Write to file
        output_file = Path(output_path)

        # Create parent directories if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)

    except IOError as e:
        raise ExportError(f"Failed to write SRT file: {e}")
    except Exception as e:
        raise ExportError(f"SRT export failed: {e}")
