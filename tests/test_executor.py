"""
Test script for the executor.

Tests all three execution modes with sample SRT files.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lexer import Lexer
from src.parser import Parser
from src.executor import Executor


def test_executor(filepath: str, mode: str = "sequential", speed_factor: float = 1.0):
    """
    Test the executor with a given file and mode.

    Args:
        filepath: Path to .srt file
        mode: Execution mode ("sequential", "real_time", or "accelerated")
        speed_factor: Speed factor for accelerated mode
    """
    print(f"\n{'='*70}")
    print(f"Testing Executor - Mode: {mode.upper()}")
    if mode == "accelerated":
        print(f"Speed Factor: {speed_factor}x")
    print(f"File: {filepath}")
    print('='*70)

    # Read file
    with open(filepath, 'r') as f:
        content = f.read()

    # Tokenize
    lexer = Lexer()
    tokens = lexer.tokenize(content)
    print(f"\nLexer: {len(tokens)} tokens generated")

    # Parse
    parser = Parser(tokens)
    entries = parser.parse()
    print(f"Parser: {len(entries)} subtitle entries parsed")

    # Execute
    print(f"\n--- Executing subtitles ({mode} mode) ---\n")
    executor = Executor()
    executor.execute(entries, mode=mode, speed_factor=speed_factor)

    print(f"\n--- Execution complete ---")


def main():
    """Run executor tests."""
    print("="*70)
    print("EXECUTOR TEST SUITE")
    print("="*70)

    # Test 1: Sequential mode (fastest for demonstration)
    print("\n" + "="*70)
    print("TEST 1: SEQUENTIAL MODE")
    print("="*70)
    print("Description: Displays each subtitle one after another with brief pause")
    print("Expected: Quick display of all subtitles in order")
    test_executor("examples/valid_basic.srt", mode="sequential")

    # Ask user if they want to test other modes (they take time)
    print("\n" + "="*70)
    print("Additional tests available:")
    print("  - Real-time mode (displays at actual timestamps)")
    print("  - Accelerated mode (displays at 5x speed)")
    print("\nTo test these modes, uncomment the lines in the script")
    print("="*70)

    # Uncomment below to test other modes:

    # # Test 2: Accelerated mode (5x speed for demonstration)
    # print("\n" + "="*70)
    # print("TEST 2: ACCELERATED MODE (5x speed)")
    # print("="*70)
    # print("Description: Displays subtitles at 5x normal speed")
    # print("Expected: Faster than real-time but maintains timing relationships")
    # test_executor("examples/valid_basic.srt", mode="accelerated", speed_factor=5.0)

    # # Test 3: Real-time mode (takes actual time)
    # print("\n" + "="*70)
    # print("TEST 3: REAL-TIME MODE")
    # print("="*70)
    # print("Description: Displays subtitles at their actual timestamps")
    # print("Expected: Subtitle 1 at 1s, subtitle 2 at 4s (with proper timing)")
    # test_executor("examples/valid_basic.srt", mode="real_time")


if __name__ == "__main__":
    main()
