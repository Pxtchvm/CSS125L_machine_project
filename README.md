# SRT Subtitle Interpreter

A Python interpreter for SubRip Text (.srt) subtitle files that can parse, validate, translate, and display subtitles.

By: **Group 1 - Shakra**
- Bagallon, Radzie, R.
- Castro, Joselito Miguel C.
- Duldulao, Jacob O.
- Gigante, Raphael Nicolai M.


The interpreter follows a simple 3-stage pipeline:

```
1. Lexer (lexer.py)
   └─> Breaks the file into tokens (like words in a sentence)

2. Parser (parser.py)
   └─> Checks structure and creates subtitle entries

3. Executor (executor.py)
   └─> Displays subtitles (with optional translation)
```

Translation is integrated directly into the executor using Google Translate API (no caching, direct calls).

## Installation (We recommend using `uv` but you can use `pip` or other python package managers as well)

### Installing `uv`

1. Run the installation command:
   - Windows:
      ```powershell
      powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
      ```
   - macOS and Linux:
      ```bash
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```

2. Verify installation by checking the version:

   ```powershell
   uv --version
   ```

### Project Setup

1. Clone or navigate to the project directory:

   ```bash
   cd CSS125L_machine_project
   ```

2. Sync dependencies using uv:

   ```bash
   uv sync
   ```

3. Activate the virtual environment:

   Windows (PowerShell):

   ```powershell
   .venv\Scripts\activate
   ```

   Linux/MacOS:

   ```bash
   source .venv/bin/activate
   ```

4. Verify installation:

   ```bash
   python --version
   python main.py
   ```

## Quick Start

### Basic Usage

Run a subtitle file (English, no translation):

```bash
python main.py examples/valid_basic.srt
```

### With Translation

Translate to Filipino (Tagalog):

```bash
python main.py examples/valid_basic.srt filipino
```

Translate to Korean:

```bash
python main.py examples/valid_basic.srt korean
```

### Supported Languages

- `english` - Original text (no translation)
- `filipino` - Filipino/Tagalog
- `korean` - Korean
- `chinese` - Simplified Chinese
- `japanese` - Japanese

## Project Structure

```
CSS125L_machine_project/
├── src/                        # Source code
│   ├── ast.py                  # Token, TimeStamp, SubtitleEntry classes
│   ├── lexer.py                # Tokenization
│   ├── parser.py               # Parsing and validation
│   ├── executor.py             # Display + translation
│   ├── interpreter.py          # Orchestrator
│   └── __init__.py
├── examples/                   # Sample .srt files
│   ├── valid_basic.srt         # Simple 2-subtitle example
│   ├── valid_multiline.srt     # Multiline subtitle example
│   ├── valid_complex.srt       # Complex example with formatting
│   └── invalid_*.srt           # Error test cases
├── main.py                     # Command-line interface
├── group1shakra_final.ipynb    # Jupyter demo notebook
├── pyproject.toml              # Dependencies (deep-translator, ipykernel)
└── README.md                   # This file
```

### Module Overview

| Module           | Purpose               | Key Classes                     |
| ---------------- | --------------------- | ------------------------------- |
| `ast.py`         | Data structures       | Token, TimeStamp, SubtitleEntry |
| `lexer.py`       | Tokenization          | Lexer, LexerError               |
| `parser.py`      | Parsing & validation  | Parser, ParserError             |
| `executor.py`    | Display & translation | Executor, ExecutorError         |
| `interpreter.py` | Orchestration         | SRTInterpreter                  |
| `main.py`        | CLI                   | main() function                 |
