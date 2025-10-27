"""SRT Subtitle Interpreter - Command Line Interface"""

import sys
from src.interpreter import SRTInterpreter


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <srt_file> [language]")
        print("\nExamples:")
        print("  python main.py examples/valid_basic.srt")
        print("  python main.py examples/valid_basic.srt filipino")
        print("  python main.py examples/valid_basic.srt korean")
        print("\nSupported languages: english, filipino, korean, chinese, japanese")
        return

    filename = sys.argv[1]

    language = 'english'
    if len(sys.argv) >= 3:
        language = sys.argv[2]

    interpreter = SRTInterpreter()
    interpreter.run(filename, language)


if __name__ == "__main__":
    main()
