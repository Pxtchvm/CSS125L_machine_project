"""
Test script for the translator.

Tests translation to all supported languages and error handling.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.translator import Translator, TranslationError
from src.ast_nodes import SubtitleEntry, TimeStamp


def create_test_entries():
    """Create sample subtitle entries for testing."""
    entries = [
        SubtitleEntry(
            index=1,
            start_time=TimeStamp(0, 0, 1, 0),
            end_time=TimeStamp(0, 0, 3, 0),
            text=["Hello world!"]
        ),
        SubtitleEntry(
            index=2,
            start_time=TimeStamp(0, 0, 4, 0),
            end_time=TimeStamp(0, 0, 6, 0),
            text=["This is a test."]
        ),
    ]
    return entries


def test_language(lang_name: str):
    """Test translation to a specific language."""
    print(f"\n{'='*70}")
    print(f"Testing Translation: {lang_name.upper()}")
    print('='*70)

    entries = create_test_entries()

    print("\nOriginal English text:")
    for entry in entries:
        print(f"  {entry.index}. {entry.get_text()}")

    try:
        translator = Translator(lang_name)
        translated = translator.translate_entries(entries)

        print(f"\nTranslated to {lang_name.title()}:")
        for entry in translated:
            print(f"  {entry.index}. {entry.get_text()}")

        print(f"\nSUCCESS: Translation to {lang_name} completed!")

    except TranslationError as e:
        print(f"\nERROR: {e}")

    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")


def test_english_passthrough():
    """Test that English language returns original text."""
    print(f"\n{'='*70}")
    print(f"Testing English Passthrough (No Translation)")
    print('='*70)

    entries = create_test_entries()

    print("\nOriginal English text:")
    for entry in entries:
        print(f"  {entry.index}. {entry.get_text()}")

    translator = Translator('english')
    result = translator.translate_entries(entries)

    # Check that the entries are the same objects (no translation occurred)
    if result is entries:
        print("\nSUCCESS: English passthrough returns original entries!")
    else:
        print("\nNote: New entry objects created, but text should be identical")
        print("\nResult text:")
        for entry in result:
            print(f"  {entry.index}. {entry.get_text()}")


def test_unsupported_language():
    """Test error handling for unsupported language."""
    print(f"\n{'='*70}")
    print(f"Testing Unsupported Language Error")
    print('='*70)

    try:
        translator = Translator('bisaya')
        print("\nUNEXPECTED: No error raised for unsupported language!")

    except TranslationError as e:
        print(f"\nExpected error caught: {e}")
        print("SUCCESS: Unsupported language properly rejected!")


def test_multiline_translation():
    """Test translation of multi-line subtitle."""
    print(f"\n{'='*70}")
    print(f"Testing Multi-line Translation")
    print('='*70)

    entry = SubtitleEntry(
        index=1,
        start_time=TimeStamp(0, 0, 1, 0),
        end_time=TimeStamp(0, 0, 4, 0),
        text=[
            "This is the first line.",
            "This is the second line.",
            "This is the third line."
        ]
    )

    print("\nOriginal English text (3 lines):")
    for i, line in enumerate(entry.text, 1):
        print(f"  Line {i}: {line}")

    try:
        translator = Translator('filipino')
        translated = translator.translate_entries([entry])

        print(f"\nTranslated to Filipino (3 lines):")
        for i, line in enumerate(translated[0].text, 1):
            print(f"  Line {i}: {line}")

        print("\nSUCCESS: Multi-line translation completed!")

    except Exception as e:
        print(f"\nERROR: {e}")


def main():
    """Run all translator tests."""
    print("="*70)
    print("TRANSLATOR TEST SUITE")
    print("="*70)

    # Test all supported languages
    print("\n" + "="*70)
    print("TESTING ALL SUPPORTED LANGUAGES")
    print("="*70)
    print("\nNote: Translation requires internet connection.")
    print("If translation fails, English fallback will be used.")

    test_language('filipino')
    test_language('korean')
    test_language('chinese')
    test_language('japanese')

    # Test English passthrough
    test_english_passthrough()

    # Test error handling
    print("\n" + "="*70)
    print("TESTING ERROR HANDLING")
    print("="*70)

    test_unsupported_language()

    # Test multi-line translation
    print("\n" + "="*70)
    print("TESTING MULTI-LINE TRANSLATION")
    print("="*70)

    test_multiline_translation()

    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
