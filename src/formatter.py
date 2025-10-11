"""
HTML to ANSI formatting converter for subtitle display.

This module converts HTML-like formatting tags in subtitles to ANSI escape codes
for terminal display with colors and text styles.
"""

import re
from typing import List


# ANSI escape codes
class ANSICode:
    """ANSI escape code constants."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'


class FormatterError(Exception):
    """Exception raised when formatting conversion fails."""
    pass


def hex_to_ansi_color(hex_color: str) -> str:
    """
    Convert hex color code to ANSI 24-bit color escape code.

    Args:
        hex_color: Hex color in format #RRGGBB or RRGGBB

    Returns:
        ANSI escape code for the color

    Raises:
        FormatterError: If hex color format is invalid
    """
    # Remove # if present
    hex_color = hex_color.lstrip('#')

    # Validate hex color format
    if not re.match(r'^[0-9A-Fa-f]{6}$', hex_color):
        raise FormatterError(f"Invalid hex color format: #{hex_color}")

    # Parse RGB values
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError as e:
        raise FormatterError(f"Failed to parse hex color #{hex_color}: {e}")

    # Return ANSI 24-bit color code (RGB)
    return f'\033[38;2;{r};{g};{b}m'


def html_to_ansi(text: str) -> str:
    """
    Convert HTML-like formatting tags to ANSI escape codes.

    Supported tags:
    - <i>text</i> → italic
    - <b>text</b> → bold
    - <u>text</u> → underline
    - <font color="#RRGGBB">text</font> → colored text

    Nested tags are supported (e.g., <i><b>text</b></i>).

    Args:
        text: Text with HTML-like formatting tags

    Returns:
        Text with ANSI escape codes replacing HTML tags

    Raises:
        FormatterError: If tag parsing fails
    """
    result = text

    # Process <i> tags (italic)
    result = re.sub(
        r'<i>(.*?)</i>',
        f'{ANSICode.ITALIC}\\1{ANSICode.RESET}',
        result,
        flags=re.DOTALL
    )

    # Process <b> tags (bold)
    result = re.sub(
        r'<b>(.*?)</b>',
        f'{ANSICode.BOLD}\\1{ANSICode.RESET}',
        result,
        flags=re.DOTALL
    )

    # Process <u> tags (underline)
    result = re.sub(
        r'<u>(.*?)</u>',
        f'{ANSICode.UNDERLINE}\\1{ANSICode.RESET}',
        result,
        flags=re.DOTALL
    )

    # Process <font color="#RRGGBB"> tags
    def replace_font_tag(match):
        color_attr = match.group(1)
        content = match.group(2)

        # Extract color value from color="#RRGGBB"
        color_match = re.search(r'color\s*=\s*["\']?(#?[0-9A-Fa-f]{6})["\']?', color_attr)
        if color_match:
            hex_color = color_match.group(1)
            ansi_color = hex_to_ansi_color(hex_color)
            return f'{ansi_color}{content}{ANSICode.RESET}'
        else:
            # If no valid color found, return original text without tags
            return content

    result = re.sub(
        r'<font\s+([^>]*?)>(.*?)</font>',
        replace_font_tag,
        result,
        flags=re.DOTALL | re.IGNORECASE
    )

    return result


def strip_html_tags(text: str) -> str:
    """
    Remove all HTML-like formatting tags from text.

    This is useful when ANSI formatting is disabled or not supported.

    Args:
        text: Text with HTML-like formatting tags

    Returns:
        Plain text without formatting tags
    """
    # Remove all HTML-like tags
    result = re.sub(r'<[^>]+>', '', text)
    return result


def format_subtitle_text(text: str, enable_formatting: bool = True) -> str:
    """
    Format subtitle text for display.

    Args:
        text: Subtitle text (may contain HTML-like tags)
        enable_formatting: If True, convert HTML to ANSI; if False, strip tags

    Returns:
        Formatted text ready for display
    """
    if enable_formatting:
        return html_to_ansi(text)
    else:
        return strip_html_tags(text)
