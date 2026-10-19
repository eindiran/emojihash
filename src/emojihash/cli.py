"""
Command-line entry point: print the emoji for each argument, file, or stdin.

With one input, prints only the emoji. With several, prints the emoji, a tab, and the input on
each line so the output can be matched back to its input.
"""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from emojihash import emojihash


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return the exit status: 0 on success, 1 if any file was unreadable."""
    parser = argparse.ArgumentParser(
        prog="emojihash",
        description="Map input to a single emoji. Not cryptographically secure.",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        help="treat each argument as a file path and hash its contents",
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        metavar="INPUT",
        help="strings (or files with -f) to hash; reads stdin if none are given",
    )
    args = parser.parse_args(argv)

    if not args.inputs:
        print(emojihash(sys.stdin.buffer))
        return 0

    status = 0
    for item in args.inputs:
        try:
            emoji = emojihash(Path(item)) if args.file else emojihash(item)
        except OSError as e:
            print(f"emojihash: {item}: {e.strerror}", file=sys.stderr)
            status = 1
            continue
        print(emoji if len(args.inputs) == 1 else f"{emoji}\t{item}")
    return status


if __name__ == "__main__":
    sys.exit(main())
