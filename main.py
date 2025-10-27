"""
SRT Subtitle Interpreter - Simple Command Line Interface

Run an SRT file through our interpreter!
"""

import sys
from src.interpreter import SRTInterpreter


def main():
    """Main function - run the interpreter"""

    # Check if user provided a file
    if len(sys.argv) < 2:
        print("Usage: python main.py <srt_file> [language]")
        print("\nExamples:")
        print("  python main.py examples/valid_basic.srt")
        print("  python main.py examples/valid_basic.srt filipino")
        print("  python main.py examples/valid_basic.srt korean")
        print("\nSupported languages: english, filipino, korean, chinese, japanese")
        return

    # Get the filename from command line
    filename = sys.argv[1]

    # Get the language if provided (default to english)
    language = 'english'
    if len(sys.argv) >= 3:
        language = sys.argv[2]

    # Create and run the interpreter
    interpreter = SRTInterpreter()
    interpreter.run(filename, language)


if __name__ == "__main__":
    main()
