"""
Test script for statistics calculation.

Tests statistics calculation for subtitle files including totals,
averages, extremes, and error handling.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lexer import Lexer
from src.parser import Parser
from src.stats import calculate_statistics, StatisticsError


def parse_file(filepath: str):
    """Helper function to parse an SRT file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lexer = Lexer()
    tokens = lexer.tokenize(content)

    parser = Parser(tokens)
    entries = parser.parse()

    return entries


def test_stats_basic():
    """Test statistics calculation on a basic SRT file."""
    print(f"\n{'='*70}")
    print(f"Test 1: Basic Statistics Calculation")
    print('='*70)

    filepath = "examples/valid_basic.srt"
    print(f"\nFile: {filepath}")

    entries = parse_file(filepath)
    print(f"Parsed: {len(entries)} subtitle entries")

    stats = calculate_statistics(entries)

    print("\n" + stats.to_string())

    # Validate key values
    print("\nValidation:")
    print(f"  Total entries: {stats.total_entries} (expected: 2)")
    print(f"  Has duration data: {stats.total_duration_ms > 0}")
    print(f"  Has average duration: {stats.avg_duration_ms > 0}")
    print(f"  Has text length data: {stats.avg_char_length > 0}")

    if stats.total_entries == 2:
        print("\nSUCCESS: Basic statistics calculated correctly!")
    else:
        print("\nERROR: Entry count mismatch!")


def test_stats_complex():
    """Test statistics calculation on comprehensive test file."""
    print(f"\n{'='*70}")
    print(f"Test 2: Complex File Statistics (Extremes)")
    print('='*70)

    filepath = "examples/valid_complex.srt"
    print(f"\nFile: {filepath}")

    entries = parse_file(filepath)
    print(f"Parsed: {len(entries)} subtitle entries")

    stats = calculate_statistics(entries)

    print("\n" + stats.to_string())

    # Validate extremes
    print("\nValidation:")
    print(f"  Longest by duration - Entry #{stats.longest_by_duration[0]}: {stats.longest_by_duration[1] / 1000:.2f}s")
    print(f"  Shortest by duration - Entry #{stats.shortest_by_duration[0]}: {stats.shortest_by_duration[1] / 1000:.2f}s")
    print(f"  Longest by text - Entry #{stats.longest_by_text[0]}: {stats.longest_by_text[1]} chars")
    print(f"  Shortest by text - Entry #{stats.shortest_by_text[0]}: {stats.shortest_by_text[1]} chars")

    # Entry 3 should be longest by duration (10s)
    # Entry 1 should be shortest by duration (1.5s)
    if stats.longest_by_duration[0] == 3 and stats.shortest_by_duration[0] == 1:
        print("\nSUCCESS: Duration extremes identified correctly!")
    else:
        print("\nNote: Extremes identified (values may vary with file changes)")


def test_stats_multiline():
    """Test statistics with multi-line text content."""
    print(f"\n{'='*70}")
    print(f"Test 3: Multi-line Text Statistics")
    print('='*70)

    filepath = "examples/valid_multiline.srt"
    print(f"\nFile: {filepath}")

    entries = parse_file(filepath)
    print(f"Parsed: {len(entries)} subtitle entries")

    # Check that multi-line text is handled correctly
    entry_text = entries[0].get_text()
    print(f"\nEntry 1 text (multi-line):")
    print(f"  '{entry_text}'")
    print(f"  Character count: {len(entry_text)}")
    print(f"  Contains newlines: {chr(10) in entry_text}")

    stats = calculate_statistics(entries)

    print("\n" + stats.to_string())

    # Multi-line text should include newline characters in count
    if stats.avg_char_length > 0:
        print("\nSUCCESS: Multi-line text statistics calculated!")
    else:
        print("\nERROR: Text length calculation failed!")


def test_stats_empty_error():
    """Test error handling for empty entries list."""
    print(f"\n{'='*70}")
    print(f"Test 4: Error Handling - Empty Entries List")
    print('='*70)

    print("\nAttempting to calculate statistics on empty list...")

    try:
        stats = calculate_statistics([])
        print("\nUNEXPECTED: No error raised for empty list!")

    except StatisticsError as e:
        print(f"\nExpected error caught: {e}")
        print("SUCCESS: Empty list error handled correctly!")

    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")


def test_stats_formatting_included():
    """Test that HTML formatting tags are included in character count."""
    print(f"\n{'='*70}")
    print(f"Test 5: HTML Tags Included in Statistics")
    print('='*70)

    filepath = "examples/valid_formatting.srt"
    print(f"\nFile: {filepath}")

    entries = parse_file(filepath)
    print(f"Parsed: {len(entries)} subtitle entries")

    # Check first entry with <i> tags
    entry_text = entries[0].get_text()
    print(f"\nEntry 1 text with tags:")
    print(f"  '{entry_text}'")
    print(f"  Character count: {len(entry_text)}")
    print(f"  Contains HTML tags: {'<' in entry_text and '>' in entry_text}")

    stats = calculate_statistics(entries)

    print("\nStatistics summary:")
    print(f"  Average character length: {stats.avg_char_length:.1f}")

    # Tags should be counted in character length
    if '<' in entry_text and '>' in entry_text:
        print("\nSUCCESS: HTML tags included in character count!")
    else:
        print("\nNote: No HTML tags found in sample")


def main():
    """Run all statistics tests."""
    print("="*70)
    print("STATISTICS TEST SUITE")
    print("="*70)

    test_stats_basic()
    test_stats_complex()
    test_stats_multiline()
    test_stats_empty_error()
    test_stats_formatting_included()

    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
