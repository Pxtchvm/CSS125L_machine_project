"""
Main SRT Interpreter.

This module orchestrates all components to provide a complete
SRT subtitle interpretation pipeline with translation support.
"""

from pathlib import Path
from src.lexer import Lexer, LexerError
from src.parser import Parser, ParserError
from src.translator import Translator, TranslationError
from src.executor import Executor, ExecutorError


class SRTInterpreter:
    """
    Main interpreter for SRT subtitle files.

    Orchestrates lexing, parsing, translation, and execution.
    """

    def __init__(self):
        """Initialize the interpreter."""
        self.lexer = Lexer()
        self.executor = Executor()

    def interpret_file(
        self,
        filepath: str,
        mode: str = "sequential",
        speed_factor: float = 1.0,
        target_lang: str = "filipino"
    ) -> None:
        """
        Interpret and execute an SRT subtitle file.

        Args:
            filepath: Path to .srt file
            mode: Execution mode ("sequential", "real_time", or "accelerated")
            speed_factor: Speed factor for accelerated mode
            target_lang: Target language for translation

        Raises:
            FileNotFoundError: If file doesn't exist
            LexerError: If tokenization fails
            ParserError: If parsing fails
            TranslationError: If translation setup fails
            ExecutorError: If execution fails
        """
        # Validate file exists
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        if not file_path.is_file():
            raise FileNotFoundError(f"Not a file: {filepath}")

        print(f"Reading file: {filepath}")

        # Read file content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"Failed to read file: {e}")

        # Lexing
        print(f"Tokenizing...")
        tokens = self.lexer.tokenize(content)
        print(f"  Generated {len(tokens)} tokens")

        # Parsing
        print(f"Parsing...")
        parser = Parser(tokens)
        entries = parser.parse()
        print(f"  Parsed {len(entries)} subtitle entries")

        # Translation
        if target_lang.lower() != 'english':
            print(f"Translating to {target_lang.title()}...")
            translator = Translator(target_lang)
            entries = translator.translate_entries(entries, file_content=content)
            print(f"  Translation complete")
        else:
            print(f"Language: English (no translation)")

        # Execution
        print(f"Executing subtitles ({mode} mode)...")
        if mode == "accelerated":
            print(f"  Speed: {speed_factor}x")
        print()

        self.executor.execute(entries, mode=mode, speed_factor=speed_factor)

        print()
        print(f"Interpretation complete!")

    def interpret(
        self,
        content: str,
        mode: str = "sequential",
        speed_factor: float = 1.0,
        target_lang: str = "filipino"
    ) -> None:
        """
        Interpret SRT content directly (not from file).

        Args:
            content: Raw SRT file content
            mode: Execution mode
            speed_factor: Speed factor for accelerated mode
            target_lang: Target language for translation

        Raises:
            LexerError: If tokenization fails
            ParserError: If parsing fails
            TranslationError: If translation setup fails
            ExecutorError: If execution fails
        """
        # Lexing
        print(f"Tokenizing...")
        tokens = self.lexer.tokenize(content)
        print(f"  Generated {len(tokens)} tokens")

        # Parsing
        print(f"Parsing...")
        parser = Parser(tokens)
        entries = parser.parse()
        print(f"  Parsed {len(entries)} subtitle entries")

        # Translation
        if target_lang.lower() != 'english':
            print(f"Translating to {target_lang.title()}...")
            translator = Translator(target_lang)
            entries = translator.translate_entries(entries, file_content=content)
            print(f"  Translation complete")
        else:
            print(f"Language: English (no translation)")

        # Execution
        print(f"Executing subtitles ({mode} mode)...")
        if mode == "accelerated":
            print(f"  Speed: {speed_factor}x")
        print()

        self.executor.execute(entries, mode=mode, speed_factor=speed_factor)

        print()
        print(f"Interpretation complete!")
