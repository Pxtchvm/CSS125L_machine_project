"""
Interpreter - the main class that ties everything together.
Read file -> Tokenize -> Parse -> Execute (with optional translation)
"""

from src.lexer import Lexer, LexerError
from src.parser import Parser, ParserError
from src.executor import Executor, ExecutorError


class SRTInterpreter:
    """Main interpreter that coordinates all the parts"""

    def __init__(self):
        """Set up the interpreter"""
        self.lexer = Lexer()
        self.parser = None
        self.executor = Executor()

    def run(self, filepath, language='english'):
        """
        Run the interpreter on an SRT file.

        Args:
            filepath: Path to the .srt file
            language: Language to translate to (default: 'english' for no translation)
        """
        print(f"Reading file: {filepath}\n")

        # Step 1: Read the file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found - {filepath}")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        # Step 2: Tokenize (Lexer)
        print("Step 1: Tokenizing...")
        try:
            tokens = self.lexer.tokenize(content)
            print(f"  Found {len(tokens)} tokens\n")
        except LexerError as e:
            print(f"Lexer Error: {e}")
            return

        # Step 3: Parse (Parser)
        print("Step 2: Parsing...")
        try:
            parser = Parser(tokens)
            entries = parser.parse()
            print(f"  Found {len(entries)} subtitles\n")
        except ParserError as e:
            print(f"Parser Error: {e}")
            return

        # Step 4: Execute (show subtitles, with optional translation)
        print(f"Step 3: Displaying subtitles")
        if language.lower() != 'english':
            print(f"  (will translate to {language})")
        print()

        try:
            self.executor.execute(entries, translate_to=language)
        except ExecutorError as e:
            print(f"Executor Error: {e}")
            return

        print("\nDone!")
