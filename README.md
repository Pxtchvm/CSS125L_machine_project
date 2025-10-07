# SRT Subtitle Interpreter

A working interpreter for SubRip Text (.srt) subtitle files that can parse, validate, and execute time-synchronized subtitle display commands.

## Features

- Parse and tokenize .srt subtitle files
- Validate subtitle format and timing
- Execute time-synchronized subtitle display
- Multiple execution modes (real-time, accelerated, sequential)

## Requirements

- Python >= 3.13

## Installation

```bash
uv venv
source .venv/bin/activate
```

## Usage

```bash
python main.py <subtitle_file.srt>
```

## Project Structure

- `src/` - Source code
- `tests/` - Test files
- `examples/` - Sample .srt files
