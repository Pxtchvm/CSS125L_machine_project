"""
Test script for full pipeline integration.

Tests complete workflows from file reading through lexing, parsing,
translation, execution, statistics, and export.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lexer import Lexer, LexerError
from src.parser import Parser, ParserError
from src.translator import Translator
from src.executor import Executor
from src.stats import calculate_statistics
from src.export import export_to_text, export_to_srt


def test_full_pipeline_basic():
    """Test complete pipeline with basic file."""
    print(f"\n{'='*70}")
    print(f"Test 1: Full Pipeline - Basic File")
    print('='*70)

    filepath = "examples/valid_basic.srt"
    print(f"\nFile: {filepath}")

    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Tokenize
        lexer = Lexer()
        tokens = lexer.tokenize(content)
        print(f"Lexer: {len(tokens)} tokens generated")

        # Parse
        parser = Parser(tokens)
        entries = parser.parse()
        print(f"Parser: {len(entries)} entries parsed")

        # Execute (sequential mode for speed)
        print("\nExecuting subtitles (sequential mode)...")
        executor = Executor()
        executor.execute(entries, mode="sequential", enable_formatting=False)

        print("\nSUCCESS: Full pipeline completed without errors!")

    except Exception as e:
        print(f"\nERROR: Pipeline failed: {e}")


def test_pipeline_with_translation():
    """Test pipeline with translation enabled."""
    print(f"\n{'='*70}")
    print(f"Test 2: Pipeline with Translation")
    print('='*70)

    filepath = "examples/valid_basic.srt"
    print(f"\nFile: {filepath}")
    print("Target language: Filipino")

    try:
        # Read and parse
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lexer = Lexer()
        tokens = lexer.tokenize(content)

        parser = Parser(tokens)
        entries = parser.parse()
        print(f"Parsed: {len(entries)} entries")

        # Translate
        print("\nTranslating to Filipino...")
        translator = Translator('filipino')
        translated_entries = translator.translate_entries(entries, file_content=content)
        print(f"Translated: {len(translated_entries)} entries")

        # Verify translation occurred
        original_text = entries[0].get_text()
        translated_text = translated_entries[0].get_text()

        print(f"\nOriginal:   {original_text}")
        print(f"Translated: {translated_text}")

        if original_text != translated_text:
            print("\nSUCCESS: Translation applied successfully!")
        else:
            print("\nNote: Translation may have returned same text (cached or identical)")

    except Exception as e:
        print(f"\nERROR: Translation pipeline failed: {e}")


def test_pipeline_with_formatting():
    """Test pipeline with ANSI formatting enabled."""
    print(f"\n{'='*70}")
    print(f"Test 3: Pipeline with ANSI Formatting")
    print('='*70)

    filepath = "examples/valid_formatting.srt"
    print(f"\nFile: {filepath}")

    try:
        # Read and parse
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lexer = Lexer()
        tokens = lexer.tokenize(content)

        parser = Parser(tokens)
        entries = parser.parse()
        print(f"Parsed: {len(entries)} entries with formatting tags")

        # Execute with formatting enabled
        print("\nExecuting with ANSI formatting enabled...")
        executor = Executor()
        executor.execute(entries, mode="sequential", enable_formatting=True)

        print("\nSUCCESS: Formatting pipeline completed!")

    except Exception as e:
        print(f"\nERROR: Formatting pipeline failed: {e}")


def test_pipeline_with_stats():
    """Test pipeline with statistics calculation."""
    print(f"\n{'='*70}")
    print(f"Test 4: Pipeline with Statistics")
    print('='*70)

    filepath = "examples/valid_complex.srt"
    print(f"\nFile: {filepath}")

    try:
        # Read and parse
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lexer = Lexer()
        tokens = lexer.tokenize(content)

        parser = Parser(tokens)
        entries = parser.parse()
        print(f"Parsed: {len(entries)} entries")

        # Calculate statistics
        print("\nCalculating statistics...")
        stats = calculate_statistics(entries)

        print(f"\nStatistics Summary:")
        print(f"  Total entries: {stats.total_entries}")
        print(f"  Total duration: {stats.format_duration(stats.total_duration_ms)}")
        print(f"  Avg duration: {stats.avg_duration_ms / 1000:.2f}s")
        print(f"  Avg text length: {stats.avg_char_length:.1f} chars")

        print("\nSUCCESS: Statistics pipeline completed!")

    except Exception as e:
        print(f"\nERROR: Statistics pipeline failed: {e}")


def test_pipeline_with_export():
    """Test pipeline with export functionality."""
    print(f"\n{'='*70}")
    print(f"Test 5: Pipeline with Export")
    print('='*70)

    filepath = "examples/valid_basic.srt"
    text_output = "test_integration_text.txt"
    srt_output = "test_integration.srt"

    print(f"\nFile: {filepath}")

    try:
        # Read and parse
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lexer = Lexer()
        tokens = lexer.tokenize(content)

        parser = Parser(tokens)
        entries = parser.parse()
        print(f"Parsed: {len(entries)} entries")

        # Translate
        translator = Translator('filipino')
        translated_entries = translator.translate_entries(entries, file_content=content)

        # Export as text
        print("\nExporting as plain text...")
        export_to_text(translated_entries, text_output, format_type="plain")
        print(f"  Text exported to: {text_output}")

        # Export as SRT
        print("Exporting as SRT file...")
        export_to_srt(translated_entries, srt_output)
        print(f"  SRT exported to: {srt_output}")

        # Verify files exist
        if Path(text_output).exists() and Path(srt_output).exists():
            print("\nSUCCESS: Export pipeline completed!")

            # Cleanup
            Path(text_output).unlink()
            Path(srt_output).unlink()
        else:
            print("\nERROR: Export files not created!")

    except Exception as e:
        print(f"\nERROR: Export pipeline failed: {e}")


def test_pipeline_all_modes():
    """Test all execution modes."""
    print(f"\n{'='*70}")
    print(f"Test 6: All Execution Modes")
    print('='*70)

    filepath = "examples/valid_basic.srt"
    print(f"\nFile: {filepath}")

    try:
        # Parse once
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lexer = Lexer()
        tokens = lexer.tokenize(content)
        parser = Parser(tokens)
        entries = parser.parse()

        executor = Executor()

        # Test sequential mode
        print("\n--- Mode: Sequential ---")
        executor.execute(entries, mode="sequential")

        # Test accelerated mode (10x speed for testing)
        print("\n--- Mode: Accelerated (10x) ---")
        executor.execute(entries, mode="accelerated", speed_factor=10.0)

        # Test real-time mode (comment out as it takes actual time)
        # print("\n--- Mode: Real-time ---")
        # executor.execute(entries, mode="real_time")

        print("\nSUCCESS: All execution modes tested!")
        print("Note: Real-time mode skipped (takes actual duration)")

    except Exception as e:
        print(f"\nERROR: Mode testing failed: {e}")


def test_pipeline_all_languages():
    """Test translation to all supported languages."""
    print(f"\n{'='*70}")
    print(f"Test 7: All Supported Languages")
    print('='*70)

    filepath = "examples/valid_basic.srt"
    languages = ['english', 'filipino', 'korean', 'chinese', 'japanese']

    print(f"\nFile: {filepath}")
    print(f"Testing {len(languages)} languages: {', '.join(languages)}")

    try:
        # Parse once
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lexer = Lexer()
        tokens = lexer.tokenize(content)
        parser = Parser(tokens)
        entries = parser.parse()

        original_text = entries[0].get_text()
        print(f"\nOriginal text: {original_text}")

        success_count = 0
        for lang in languages:
            try:
                translator = Translator(lang)
                translated = translator.translate_entries(entries, file_content=content)
                translated_text = translated[0].get_text()
                print(f"  {lang.capitalize()}: {translated_text}")
                success_count += 1
            except Exception as e:
                print(f"  {lang.capitalize()}: ERROR - {e}")

        if success_count == len(languages):
            print(f"\nSUCCESS: All {success_count} languages tested successfully!")
        else:
            print(f"\nPartial success: {success_count}/{len(languages)} languages worked")

    except Exception as e:
        print(f"\nERROR: Language testing failed: {e}")


def test_pipeline_error_handling():
    """Test error handling through the pipeline."""
    print(f"\n{'='*70}")
    print(f"Test 8: Pipeline Error Handling")
    print('='*70)

    invalid_files = [
        ("examples/invalid_missing_index.srt", "Missing index"),
        ("examples/invalid_timestamp_order.srt", "Start time after end time"),
        ("examples/invalid_malformed_time.srt", "Invalid timestamp"),
        ("examples/invalid_no_text.srt", "Missing text content")
    ]

    print(f"\nTesting {len(invalid_files)} invalid files...")

    errors_caught = 0
    for filepath, expected_error in invalid_files:
        print(f"\n  Testing: {filepath}")
        print(f"  Expected: {expected_error}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            lexer = Lexer()
            tokens = lexer.tokenize(content)

            parser = Parser(tokens)
            entries = parser.parse()

            print(f"  UNEXPECTED: No error raised!")

        except (LexerError, ParserError) as e:
            print(f"  Error caught: {type(e).__name__} - {e}")
            errors_caught += 1

        except Exception as e:
            print(f"  UNEXPECTED ERROR: {e}")

    if errors_caught == len(invalid_files):
        print(f"\nSUCCESS: All {errors_caught} errors caught correctly!")
    else:
        print(f"\nPartial success: {errors_caught}/{len(invalid_files)} errors caught")


def main():
    """Run all integration tests."""
    print("="*70)
    print("INTEGRATION TEST SUITE")
    print("="*70)
    print("\nNote: These tests verify the complete pipeline from file to output.")
    print("Some tests may take longer due to translation API calls.")

    test_full_pipeline_basic()
    test_pipeline_with_translation()
    test_pipeline_with_formatting()
    test_pipeline_with_stats()
    test_pipeline_with_export()
    test_pipeline_all_modes()
    test_pipeline_all_languages()
    test_pipeline_error_handling()

    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
