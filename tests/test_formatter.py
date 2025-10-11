"""
Test script for HTML to ANSI formatting converter.

Tests HTML tag conversion to ANSI escape codes, tag stripping,
color conversion, and error handling.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.formatter import (
    html_to_ansi,
    strip_html_tags,
    hex_to_ansi_color,
    format_subtitle_text,
    ANSICode,
    FormatterError
)


def test_italic_tag():
    """Test italic tag conversion to ANSI."""
    print(f"\n{'='*70}")
    print(f"Test 1: Italic Tag Conversion")
    print('='*70)

    input_text = "<i>italic text</i>"
    output = html_to_ansi(input_text)

    print(f"\nInput:  {input_text!r}")
    print(f"Output: {output!r}")
    print(f"\nContains italic code (\\033[3m): {ANSICode.ITALIC in output}")
    print(f"Contains reset code (\\033[0m): {ANSICode.RESET in output}")

    if ANSICode.ITALIC in output and ANSICode.RESET in output:
        print("\nSUCCESS: Italic tag converted correctly!")
    else:
        print("\nERROR: Italic conversion failed!")


def test_bold_tag():
    """Test bold tag conversion to ANSI."""
    print(f"\n{'='*70}")
    print(f"Test 2: Bold Tag Conversion")
    print('='*70)

    input_text = "<b>bold text</b>"
    output = html_to_ansi(input_text)

    print(f"\nInput:  {input_text!r}")
    print(f"Output: {output!r}")
    print(f"\nContains bold code (\\033[1m): {ANSICode.BOLD in output}")
    print(f"Contains reset code (\\033[0m): {ANSICode.RESET in output}")

    if ANSICode.BOLD in output and ANSICode.RESET in output:
        print("\nSUCCESS: Bold tag converted correctly!")
    else:
        print("\nERROR: Bold conversion failed!")


def test_underline_tag():
    """Test underline tag conversion to ANSI."""
    print(f"\n{'='*70}")
    print(f"Test 3: Underline Tag Conversion")
    print('='*70)

    input_text = "<u>underline text</u>"
    output = html_to_ansi(input_text)

    print(f"\nInput:  {input_text!r}")
    print(f"Output: {output!r}")
    print(f"\nContains underline code (\\033[4m): {ANSICode.UNDERLINE in output}")
    print(f"Contains reset code (\\033[0m): {ANSICode.RESET in output}")

    if ANSICode.UNDERLINE in output and ANSICode.RESET in output:
        print("\nSUCCESS: Underline tag converted correctly!")
    else:
        print("\nERROR: Underline conversion failed!")


def test_font_color_tag():
    """Test font color tag conversion to ANSI RGB."""
    print(f"\n{'='*70}")
    print(f"Test 4: Font Color Tag Conversion")
    print('='*70)

    # Test red color
    input_text = '<font color="#FF0000">red text</font>'
    output = html_to_ansi(input_text)

    print(f"\nTest: Red color")
    print(f"Input:  {input_text!r}")
    print(f"Output: {output!r}")

    # RGB for red: 255, 0, 0 (note: \033 and \x1b are the same escape character)
    expected_code = "\033[38;2;255;0;0m"
    print(f"\nContains RGB code for red: {expected_code in output}")

    # Test green color
    input_text2 = '<font color="#00FF00">green text</font>'
    output2 = html_to_ansi(input_text2)
    expected_code2 = "\033[38;2;0;255;0m"

    print(f"\nTest: Green color")
    print(f"Input:  {input_text2!r}")
    print(f"Output: {output2!r}")
    print(f"Contains RGB code for green: {expected_code2 in output2}")

    # Test blue color
    input_text3 = '<font color="#0000FF">blue text</font>'
    output3 = html_to_ansi(input_text3)
    expected_code3 = "\033[38;2;0;0;255m"

    print(f"\nTest: Blue color")
    print(f"Input:  {input_text3!r}")
    print(f"Output: {output3!r}")
    print(f"Contains RGB code for blue: {expected_code3 in output3}")

    if expected_code in output and expected_code2 in output2 and expected_code3 in output3:
        print("\nSUCCESS: Color tag conversion works for all tested colors!")
    else:
        print("\nERROR: Color conversion failed!")


def test_nested_tags():
    """Test nested HTML tags."""
    print(f"\n{'='*70}")
    print(f"Test 5: Nested Tags")
    print('='*70)

    input_text = "<i><b>nested text</b></i>"
    output = html_to_ansi(input_text)

    print(f"\nInput:  {input_text!r}")
    print(f"Output: {output!r}")
    print(f"\nContains italic code: {ANSICode.ITALIC in output}")
    print(f"Contains bold code: {ANSICode.BOLD in output}")
    print(f"Contains reset codes: {output.count(ANSICode.RESET) >= 2}")

    if ANSICode.ITALIC in output and ANSICode.BOLD in output:
        print("\nSUCCESS: Nested tags converted correctly!")
    else:
        print("\nERROR: Nested tag conversion failed!")


def test_strip_html_tags():
    """Test HTML tag stripping."""
    print(f"\n{'='*70}")
    print(f"Test 6: Strip HTML Tags")
    print('='*70)

    input_text = "<i>italic</i> and <b>bold</b>"
    output = strip_html_tags(input_text)

    print(f"\nInput:  {input_text!r}")
    print(f"Output: {output!r}")
    print(f"\nExpected: 'italic and bold'")
    print(f"No HTML tags in output: {'<' not in output and '>' not in output}")

    if output == "italic and bold":
        print("\nSUCCESS: HTML tags stripped correctly!")
    else:
        print("\nERROR: Tag stripping failed!")


def test_hex_to_ansi_valid():
    """Test hex color to ANSI conversion with valid inputs."""
    print(f"\n{'='*70}")
    print(f"Test 7: Hex to ANSI Color Conversion (Valid)")
    print('='*70)

    # Test with # prefix
    print("\nTest: #FF0000 (red)")
    color1 = hex_to_ansi_color("#FF0000")
    print(f"  Output: {color1!r}")
    print(f"  Expected: '\\033[38;2;255;0;0m' (same as \\x1b)")
    print(f"  Match: {color1 == '\033[38;2;255;0;0m'}")

    # Test without # prefix
    print("\nTest: 00FF00 (green, no #)")
    color2 = hex_to_ansi_color("00FF00")
    print(f"  Output: {color2!r}")
    print(f"  Expected: '\\033[38;2;0;255;0m' (same as \\x1b)")
    print(f"  Match: {color2 == '\033[38;2;0;255;0m'}")

    # Test mixed case
    print("\nTest: #0000ff (blue, lowercase)")
    color3 = hex_to_ansi_color("#0000ff")
    print(f"  Output: {color3!r}")
    print(f"  Expected: '\\033[38;2;0;0;255m' (same as \\x1b)")
    print(f"  Match: {color3 == '\033[38;2;0;0;255m'}")

    if (color1 == '\033[38;2;255;0;0m' and
        color2 == '\033[38;2;0;255;0m' and
        color3 == '\033[38;2;0;0;255m'):
        print("\nSUCCESS: Hex to ANSI conversion works correctly!")
    else:
        print("\nERROR: Hex conversion failed!")


def test_hex_to_ansi_invalid_error():
    """Test hex color conversion error handling."""
    print(f"\n{'='*70}")
    print(f"Test 8: Hex to ANSI Error Handling (Invalid)")
    print('='*70)

    invalid_colors = ["GGGGGG", "12345", "ZZZZZZ", "FF00", "#12345G"]

    errors_caught = 0
    for color in invalid_colors:
        print(f"\nTesting invalid color: {color!r}")
        try:
            result = hex_to_ansi_color(color)
            print(f"  UNEXPECTED: No error raised, got: {result!r}")
        except FormatterError as e:
            print(f"  Expected error caught: {e}")
            errors_caught += 1
        except Exception as e:
            print(f"  UNEXPECTED ERROR: {e}")

    if errors_caught == len(invalid_colors):
        print(f"\nSUCCESS: All {errors_caught} invalid colors caught correctly!")
    else:
        print(f"\nERROR: Only {errors_caught}/{len(invalid_colors)} errors caught!")


def test_format_subtitle_text_enabled():
    """Test format_subtitle_text with formatting enabled."""
    print(f"\n{'='*70}")
    print(f"Test 9: format_subtitle_text (Formatting Enabled)")
    print('='*70)

    input_text = "<i>italic</i> and <b>bold</b>"
    output = format_subtitle_text(input_text, enable_formatting=True)

    print(f"\nInput:  {input_text!r}")
    print(f"Output: {output!r}")
    print(f"\nContains ANSI codes: {ANSICode.ITALIC in output and ANSICode.BOLD in output}")

    if ANSICode.ITALIC in output and ANSICode.BOLD in output:
        print("\nSUCCESS: HTML converted to ANSI when formatting enabled!")
    else:
        print("\nERROR: Formatting conversion failed!")


def test_format_subtitle_text_disabled():
    """Test format_subtitle_text with formatting disabled."""
    print(f"\n{'='*70}")
    print(f"Test 10: format_subtitle_text (Formatting Disabled)")
    print('='*70)

    input_text = "<i>italic</i> and <b>bold</b>"
    output = format_subtitle_text(input_text, enable_formatting=False)

    print(f"\nInput:  {input_text!r}")
    print(f"Output: {output!r}")
    print(f"Expected: 'italic and bold'")
    print(f"\nNo HTML tags: {'<' not in output and '>' not in output}")
    print(f"No ANSI codes: {ANSICode.ITALIC not in output and ANSICode.BOLD not in output}")

    if output == "italic and bold":
        print("\nSUCCESS: HTML tags stripped when formatting disabled!")
    else:
        print("\nERROR: Tag stripping failed!")


def main():
    """Run all formatter tests."""
    print("="*70)
    print("FORMATTER TEST SUITE")
    print("="*70)

    test_italic_tag()
    test_bold_tag()
    test_underline_tag()
    test_font_color_tag()
    test_nested_tags()
    test_strip_html_tags()
    test_hex_to_ansi_valid()
    test_hex_to_ansi_invalid_error()
    test_format_subtitle_text_enabled()
    test_format_subtitle_text_disabled()

    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
