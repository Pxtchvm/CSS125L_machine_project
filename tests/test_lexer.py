"""
Simple test script for the lexer.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lexer import Lexer


def test_file(filepath: str):
    """Test the lexer on a given file."""
    print(f"\n{'='*60}")
    print(f"Testing: {filepath}")
    print('='*60)

    with open(filepath, 'r') as f:
        content = f.read()

    print("\nFile content:")
    print(content)

    print("\nTokens:")
    lexer = Lexer()
    tokens = lexer.tokenize(content)

    for token in tokens:
        print(f"  {token}")

    print(f"\nTotal tokens: {len(tokens)}")


if __name__ == "__main__":
    test_file("examples/valid_basic.srt")
    test_file("examples/valid_multiline.srt")
