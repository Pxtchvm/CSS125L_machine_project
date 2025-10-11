"""
SRT Subtitle Interpreter - Command Line Interface

A working interpreter for SubRip Text (.srt) subtitle files that can parse,
validate, translate, and execute time-synchronized subtitle display commands.
"""

import sys
import argparse
from src.interpreter import SRTInterpreter
from src.lexer import LexerError
from src.parser import ParserError
from src.translator import TranslationError, Translator
from src.executor import ExecutorError
from src.stats import StatisticsError
from src.export import ExportError


def main():
    """Main entry point for the SRT interpreter."""
    parser = argparse.ArgumentParser(
        description='SRT Subtitle Interpreter with multi-language translation support',
        epilog='Example: python main.py subtitles.srt --lang filipino --mode sequential'
    )

    # Required argument
    parser.add_argument(
        'filepath',
        type=str,
        help='Path to .srt subtitle file'
    )

    # Optional arguments
    parser.add_argument(
        '--mode',
        type=str,
        choices=['sequential', 'real_time', 'accelerated'],
        default='sequential',
        help='Execution mode (default: sequential)'
    )

    parser.add_argument(
        '--speed',
        type=float,
        default=5.0,
        help='Speed factor for accelerated mode (default: 5.0)'
    )

    parser.add_argument(
        '--lang',
        type=str,
        choices=['english', 'filipino', 'korean', 'chinese', 'japanese'],
        default='filipino',
        help='Target language for subtitle translation (default: filipino)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Display statistics about the subtitle file instead of executing it'
    )

    parser.add_argument(
        '--export-txt',
        nargs='?',
        const='output.txt',
        default=None,
        metavar='PATH',
        help='Export subtitle text to file (default: output.txt)'
    )

    parser.add_argument(
        '--export-srt',
        nargs='?',
        const='__AUTO__',  # Marker to compute default based on language
        default=None,
        metavar='PATH',
        help='Export translated SRT file (default: output_{language}.srt)'
    )

    parser.add_argument(
        '--export-format',
        choices=['plain', 'numbered', 'separated'],
        default='plain',
        help='Text export format: plain, numbered, or separated (default: plain)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Compute smart default for --export-srt if needed
    if args.export_srt == '__AUTO__':
        args.export_srt = f'output_{args.lang}.srt'

    # Create interpreter
    interpreter = SRTInterpreter()

    # Execute
    try:
        # Handle export operations (can combine with --stats)
        if args.export_txt:
            interpreter.export_text_from_file(
                filepath=args.filepath,
                output_path=args.export_txt,
                format_type=args.export_format
            )
            print()

        if args.export_srt:
            interpreter.export_srt_from_file(
                filepath=args.filepath,
                output_path=args.export_srt,
                target_lang=args.lang
            )
            print()

        # Handle statistics display
        if args.stats:
            interpreter.display_statistics_for_file(filepath=args.filepath)
            print()

        # If no export or stats flags, execute normally
        if not args.export_txt and not args.export_srt and not args.stats:
            interpreter.interpret_file(
                filepath=args.filepath,
                mode=args.mode,
                speed_factor=args.speed,
                target_lang=args.lang
            )

        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except LexerError as e:
        print(f"Lexer Error: {e}", file=sys.stderr)
        sys.exit(1)

    except ParserError as e:
        print(f"Parser Error: {e}", file=sys.stderr)
        sys.exit(1)

    except TranslationError as e:
        print(f"Translation Error: {e}", file=sys.stderr)
        sys.exit(1)

    except ExecutorError as e:
        print(f"Executor Error: {e}", file=sys.stderr)
        sys.exit(1)

    except StatisticsError as e:
        print(f"Statistics Error: {e}", file=sys.stderr)
        sys.exit(1)

    except ExportError as e:
        print(f"Export Error: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
