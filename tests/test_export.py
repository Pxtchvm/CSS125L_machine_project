"""
Test script for export functionality.

Tests text export (plain, numbered, separated formats) and SRT export
with validation and error handling.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lexer import Lexer
from src.parser import Parser
from src.export import export_to_text, export_to_srt, ExportError


def parse_file(filepath: str):
    """Helper function to parse an SRT file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lexer = Lexer()
    tokens = lexer.tokenize(content)

    parser = Parser(tokens)
    entries = parser.parse()

    return entries


def test_export_text_plain():
    """Test plain text export format."""
    print(f"\n{'='*70}")
    print(f"Test 1: Plain Text Export")
    print('='*70)

    filepath = "examples/valid_basic.srt"
    output_path = "test_output_plain.txt"

    print(f"\nSource file: {filepath}")
    print(f"Output file: {output_path}")

    entries = parse_file(filepath)
    print(f"Parsed: {len(entries)} subtitle entries")

    # Export as plain text
    print("\nExporting in plain format...")
    export_to_text(entries, output_path, format_type="plain")

    # Read back and validate
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\nExported content:")
    print(content)

    # Cleanup
    Path(output_path).unlink()

    # Validate: Should contain subtitle text, no metadata
    if "Hello world!" in content and "[1]" not in content:
        print("\nSUCCESS: Plain text export correct!")
    else:
        print("\nERROR: Plain format validation failed!")


def test_export_text_numbered():
    """Test numbered text export format."""
    print(f"\n{'='*70}")
    print(f"Test 2: Numbered Text Export")
    print('='*70)

    filepath = "examples/valid_complex.srt"
    output_path = "test_output_numbered.txt"

    print(f"\nSource file: {filepath}")
    print(f"Output file: {output_path}")

    entries = parse_file(filepath)
    print(f"Parsed: {len(entries)} subtitle entries")

    # Export as numbered
    print("\nExporting in numbered format...")
    export_to_text(entries, output_path, format_type="numbered")

    # Read back and validate
    with open(output_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"\nFirst 5 entries:")
    for i in range(min(5, len(lines))):
        print(f"  {lines[i].rstrip()}")

    # Cleanup
    Path(output_path).unlink()

    # Validate: Should have [1], [2], etc. prefixes
    if lines[0].startswith("[1]") and lines[1].startswith("[2]"):
        print("\nSUCCESS: Numbered text export correct!")
    else:
        print("\nERROR: Numbered format validation failed!")


def test_export_text_separated():
    """Test separated text export format."""
    print(f"\n{'='*70}")
    print(f"Test 3: Separated Text Export")
    print('='*70)

    filepath = "examples/valid_multiline.srt"
    output_path = "test_output_separated.txt"

    print(f"\nSource file: {filepath}")
    print(f"Output file: {output_path}")

    entries = parse_file(filepath)
    print(f"Parsed: {len(entries)} subtitle entries")

    # Export as separated
    print("\nExporting in separated format...")
    export_to_text(entries, output_path, format_type="separated")

    # Read back and validate
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\nExported content:")
    print(content)
    print(f"\nContent has blank lines for separation: {'\\n\\n' in content or content.endswith('\\n')}")

    # Cleanup
    Path(output_path).unlink()

    # Validate: Multi-line should be preserved
    if "multiple lines" in content:
        print("\nSUCCESS: Separated text export correct!")
    else:
        print("\nERROR: Separated format validation failed!")


def test_export_srt_structure():
    """Test SRT file export and structure validation."""
    print(f"\n{'='*70}")
    print(f"Test 4: SRT File Export")
    print('='*70)

    filepath = "examples/valid_formatting.srt"
    output_path = "test_output.srt"

    print(f"\nSource file: {filepath}")
    print(f"Output file: {output_path}")

    entries = parse_file(filepath)
    print(f"Parsed: {len(entries)} subtitle entries")

    # Export as SRT
    print("\nExporting as SRT file...")
    export_to_srt(entries, output_path)

    # Re-parse exported file to verify validity
    print("\nRe-parsing exported SRT file...")
    reparse_entries = parse_file(output_path)
    print(f"Re-parsed: {len(reparse_entries)} subtitle entries")

    # Compare entry counts
    if len(entries) == len(reparse_entries):
        print(f"\nEntry count match: {len(entries)} == {len(reparse_entries)}")
    else:
        print(f"\nERROR: Entry count mismatch: {len(entries)} != {len(reparse_entries)}")

    # Validate structure
    print("\nValidating structure:")
    print(f"  Index preserved: {entries[0].index == reparse_entries[0].index}")
    print(f"  Start time preserved: {entries[0].start_time == reparse_entries[0].start_time}")
    print(f"  End time preserved: {entries[0].end_time == reparse_entries[0].end_time}")
    print(f"  Text preserved: {entries[0].get_text() == reparse_entries[0].get_text()}")

    # Cleanup
    Path(output_path).unlink()

    if len(entries) == len(reparse_entries):
        print("\nSUCCESS: SRT export structure valid!")
    else:
        print("\nERROR: SRT export validation failed!")


def test_export_invalid_format_error():
    """Test error handling for invalid format type."""
    print(f"\n{'='*70}")
    print(f"Test 5: Error Handling - Invalid Format Type")
    print('='*70)

    entries = parse_file("examples/valid_basic.srt")

    print("\nAttempting to export with invalid format 'invalid'...")

    try:
        export_to_text(entries, "test_invalid.txt", format_type="invalid")
        print("\nUNEXPECTED: No error raised for invalid format!")

    except ExportError as e:
        print(f"\nExpected error caught: {e}")
        print("SUCCESS: Invalid format error handled correctly!")

    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")


def test_export_empty_entries_error():
    """Test error handling for empty entries list."""
    print(f"\n{'='*70}")
    print(f"Test 6: Error Handling - Empty Entries List")
    print('='*70)

    print("\nAttempting to export empty entries list...")

    try:
        export_to_text([], "test_empty.txt")
        print("\nUNEXPECTED: No error raised for empty list!")

    except ExportError as e:
        print(f"\nExpected error caught: {e}")

    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")

    # Also test SRT export with empty list
    try:
        export_to_srt([], "test_empty.srt")
        print("\nUNEXPECTED: No error raised for empty list in SRT export!")

    except ExportError as e:
        print(f"Expected error caught (SRT): {e}")
        print("SUCCESS: Empty list error handled correctly!")

    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")


def main():
    """Run all export tests."""
    print("="*70)
    print("EXPORT TEST SUITE")
    print("="*70)

    test_export_text_plain()
    test_export_text_numbered()
    test_export_text_separated()
    test_export_srt_structure()
    test_export_invalid_format_error()
    test_export_empty_entries_error()

    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
