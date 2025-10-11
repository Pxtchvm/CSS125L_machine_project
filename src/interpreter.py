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
from src.stats import calculate_statistics, StatisticsError
from src.export import export_to_text, export_to_srt, ExportError


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
        target_lang: str = "filipino",
        enable_formatting: bool = False
    ) -> None:
        """
        Interpret and execute an SRT subtitle file.

        Args:
            filepath: Path to .srt file
            mode: Execution mode ("sequential", "real_time", or "accelerated")
            speed_factor: Speed factor for accelerated mode
            target_lang: Target language for translation
            enable_formatting: Enable ANSI formatting for HTML tags (default: False)

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
        if enable_formatting:
            print(f"  Formatting: Enabled (ANSI)")
        print()

        self.executor.execute(entries, mode=mode, speed_factor=speed_factor, enable_formatting=enable_formatting)

        print()
        print(f"Interpretation complete!")

    def display_statistics_for_file(self, filepath: str) -> None:
        """
        Calculate and display statistics for an SRT subtitle file.

        Args:
            filepath: Path to .srt file

        Raises:
            FileNotFoundError: If file doesn't exist
            LexerError: If tokenization fails
            ParserError: If parsing fails
            StatisticsError: If statistics calculation fails
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
        print()

        # Calculate statistics
        print(f"Calculating statistics...")
        stats = calculate_statistics(entries)

        # Display statistics
        print()
        print(stats.to_string())

    def display_statistics_for_content(self, content: str) -> None:
        """
        Calculate and display statistics for SRT content.

        Args:
            content: Raw SRT file content

        Raises:
            LexerError: If tokenization fails
            ParserError: If parsing fails
            StatisticsError: If statistics calculation fails
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
        print()

        # Calculate statistics
        print(f"Calculating statistics...")
        stats = calculate_statistics(entries)

        # Display statistics
        print()
        print(stats.to_string())

    def interpret(
        self,
        content: str,
        mode: str = "sequential",
        speed_factor: float = 1.0,
        target_lang: str = "filipino",
        enable_formatting: bool = False
    ) -> None:
        """
        Interpret SRT content directly (not from file).

        Args:
            content: Raw SRT file content
            mode: Execution mode
            speed_factor: Speed factor for accelerated mode
            target_lang: Target language for translation
            enable_formatting: Enable ANSI formatting for HTML tags (default: False)

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
        if enable_formatting:
            print(f"  Formatting: Enabled (ANSI)")
        print()

        self.executor.execute(entries, mode=mode, speed_factor=speed_factor, enable_formatting=enable_formatting)

        print()
        print(f"Interpretation complete!")

    def export_text_from_file(
        self,
        filepath: str,
        output_path: str,
        format_type: str = "plain"
    ) -> None:
        """
        Export subtitle text content to a plain text file.

        Args:
            filepath: Path to source .srt file
            output_path: Path where text file should be written
            format_type: Export format ("plain", "numbered", or "separated")

        Raises:
            FileNotFoundError: If file doesn't exist
            LexerError: If tokenization fails
            ParserError: If parsing fails
            ExportError: If export fails
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

        # Export
        print(f"Exporting text ({format_type} format)...")
        export_to_text(entries, output_path, format_type)
        print(f"  Text exported to: {output_path}")

    def export_srt_from_file(
        self,
        filepath: str,
        output_path: str,
        target_lang: str = "filipino"
    ) -> None:
        """
        Export translated subtitle file as a new SRT file.

        Args:
            filepath: Path to source .srt file
            output_path: Path where translated .srt file should be written
            target_lang: Target language for translation

        Raises:
            FileNotFoundError: If file doesn't exist
            LexerError: If tokenization fails
            ParserError: If parsing fails
            TranslationError: If translation fails
            ExportError: If export fails
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
            print(f"Language: English (no translation needed)")

        # Export
        print(f"Exporting SRT file...")
        export_to_srt(entries, output_path)
        print(f"  SRT file exported to: {output_path}")
