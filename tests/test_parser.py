"""
Test script for the parser.

Tests both valid and invalid SRT files to demonstrate parser functionality.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lexer import Lexer, LexerError
from src.parser import Parser, ParserError


def test_valid_file(filepath: str):
    """Test parsing a valid SRT file."""
    print(f"\n{'='*70}")
    print(f"Testing VALID file: {filepath}")
    print('='*70)

    with open(filepath, 'r') as f:
        content = f.read()

    print("\nFile content:")
    print(content)

    try:
        # Tokenize
        lexer = Lexer()
        tokens = lexer.tokenize(content)
        print(f"\n✓ Lexer: {len(tokens)} tokens generated")

        # Parse
        parser = Parser(tokens)
        entries = parser.parse()
        print(f"✓ Parser: {len(entries)} subtitle entries parsed successfully")

        # Display parsed entries
        print("\nParsed subtitle entries:")
        for entry in entries:
            print(f"\n  Entry {entry.index}:")
            print(f"    Start: {entry.start_time}")
            print(f"    End:   {entry.end_time}")
            print(f"    Text:  {entry.get_text()!r}")

        print("\n✓ SUCCESS: File parsed correctly!")

    except (LexerError, ParserError) as e:
        print(f"\n✗ ERROR: {e}")


def test_invalid_file(filepath: str, expected_error: str = ""):
    """Test parsing an invalid SRT file (should raise error)."""
    print(f"\n{'='*70}")
    print(f"Testing INVALID file: {filepath}")
    if expected_error:
        print(f"Expected error: {expected_error}")
    print('='*70)

    with open(filepath, 'r') as f:
        content = f.read()

    print("\nFile content:")
    print(content)

    try:
        # Tokenize
        lexer = Lexer()
        tokens = lexer.tokenize(content)
        print(f"\n✓ Lexer: {len(tokens)} tokens generated")

        # Parse (should fail)
        parser = Parser(tokens)
        entries = parser.parse()

        print(f"\n✗ UNEXPECTED: File parsed without error ({len(entries)} entries)")
        print("   This file should have failed validation!")

    except LexerError as e:
        print(f"\n✓ Lexer caught error: {e}")

    except ParserError as e:
        print(f"\n✓ Parser caught error: {e}")


def main():
    """Run all parser tests."""
    print("="*70)
    print("PARSER TEST SUITE")
    print("="*70)

    # Test valid files
    print("\n" + "="*70)
    print("VALID FILES (should parse successfully)")
    print("="*70)

    test_valid_file("examples/valid_basic.srt")
    test_valid_file("examples/valid_multiline.srt")
    test_valid_file("examples/valid_formatting.srt")

    # Test invalid files
    print("\n" + "="*70)
    print("INVALID FILES (should raise errors)")
    print("="*70)

    test_invalid_file("examples/invalid_missing_index.srt", "Missing index")
    test_invalid_file("examples/invalid_timestamp_order.srt", "Start time after end time")
    test_invalid_file("examples/invalid_malformed_time.srt", "Invalid timestamp ranges")
    test_invalid_file("examples/invalid_no_text.srt", "Missing text content")

    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
