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

    # Parse arguments
    args = parser.parse_args()

    # Create interpreter
    interpreter = SRTInterpreter()

    # Execute
    try:
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

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
