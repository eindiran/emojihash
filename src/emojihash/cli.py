"""
Command-line entry point: print the emoji hash of each argument, file, or stdin.

With one input, prints only the emoji. With several, prints the emoji, a tab, and the input on
each line so the output can be matched back to its input.
"""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from emojihash import emojihash


def _positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"not an integer: {text!r}") from e
    if value < 1:
        raise argparse.ArgumentTypeError(f"must be >= 1, got {value}")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return the exit status: 0 on success, 1 if any file was unreadable."""
    parser = argparse.ArgumentParser(
        prog="emojihash",
        description="Map input to a short string of emoji. Not cryptographically secure.",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        help="treat each argument as a file path and hash its contents",
    )
    parser.add_argument(
        "-n",
        "--length",
        type=_positive_int,
        default=1,
        help="number of emoji to print per input; longer means fewer collisions (default: 1)",
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        metavar="INPUT",
        help="strings (or files with -f) to hash; reads stdin if none are given",
    )
    args = parser.parse_args(argv)

    if not args.inputs:
        print(emojihash(sys.stdin.buffer, args.length))
        return 0

    status = 0
    for item in args.inputs:
        try:
            emoji = emojihash(Path(item) if args.file else item, args.length)
        except OSError as e:
            print(f"emojihash: {item}: {e.strerror}", file=sys.stderr)
            status = 1
            continue
        print(emoji if len(args.inputs) == 1 else f"{emoji}\t{item}")
    return status


if __name__ == "__main__":
    sys.exit(main())
