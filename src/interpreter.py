"""Interpreter - coordinates all components: Read -> Tokenize -> Parse -> Execute."""

from src.lexer import Lexer, LexerError
from src.parser import Parser, ParserError
from src.executor import Executor, ExecutorError


class SRTInterpreter:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = None
        self.executor = Executor()

    def run(self, filepath, language='english'):
        print(f"Reading file: {filepath}\n")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found - {filepath}")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        print("Step 1: Tokenizing...")
        try:
            tokens = self.lexer.tokenize(content)
            print(f"  Found {len(tokens)} tokens\n")
        except LexerError as e:
            print(f"Lexer Error: {e}")
            return

        print("Step 2: Parsing...")
        try:
            parser = Parser(tokens)
            entries = parser.parse()
            print(f"  Found {len(entries)} subtitles\n")
        except ParserError as e:
            print(f"Parser Error: {e}")
            return

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
