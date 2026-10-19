"""
Map arbitrary input to a single emoji.

The input is converted to bytes, hashed with BLAKE2b, and the first digest byte indexes the
256-entry table in `EMOJI`. Output is stable across processes, platforms, and Python
versions, unlike the builtin `hash()`, which is salted per process for `str` and `bytes`.

NOT CRYPTOGRAPHICALLY SECURE. There are only 256 possible outputs: two unrelated inputs
match with probability 1/256, and anyone can find an input that maps to a chosen emoji in a
few hundred tries. Use it for visual tagging (log lines, shell prompts, build IDs, hosts),
never for authentication, integrity checks, or key verification.
"""

import hashlib
import io
import os
from decimal import Decimal
from fractions import Fraction
from typing import IO

from emojihash._table import EMOJI

__all__ = ["EMOJI", "EmojiHashable", "emojihash"]

type EmojiHashable = (
    str
    | bytes
    | bytearray
    | memoryview
    | int
    | float
    | complex
    | Decimal
    | Fraction
    | os.PathLike[str]
    | IO[bytes]
    | IO[str]
)
"""Input types accepted by `emojihash`."""

_NUMBER_TYPES = (int, float, complex, Decimal, Fraction)
_CHUNK_SIZE = 1 << 16


def emojihash(value: EmojiHashable) -> str:
    """
    Return the emoji for `value`. Not cryptographically secure; see the module docstring.

    How each input type is converted to bytes before hashing:

    - `str`: its UTF-8 encoding, so `"hi"` and `b"hi"` map to the same emoji. A `str` is
      always treated as text, never as a file path
    - `bytes`, `bytearray`, `memoryview`: the raw bytes
    - Numbers: the UTF-8 encoding of `str(value)`, so `42` matches `"42"` but `1` and `1.0`
      differ
    - `os.PathLike` (e.g. `pathlib.Path`): the file's contents, read in binary mode
    - Open file objects: the remaining contents from the current position. Text-mode files
      are re-encoded as UTF-8, so newline translation can make them differ from the same
      file read in binary mode

    Raises `TypeError` for any other type, and `OSError` if a path cannot be read.
    """
    digest = hashlib.blake2b(digest_size=1)
    if isinstance(value, str):
        digest.update(value.encode())
    elif isinstance(value, bytes | bytearray | memoryview):
        digest.update(value)
    elif isinstance(value, _NUMBER_TYPES):
        digest.update(str(value).encode())
    elif isinstance(value, os.PathLike):
        with open(value, "rb") as f:
            _update_from_stream(digest, f)
    elif isinstance(value, io.IOBase):
        _update_from_stream(digest, value)
    else:
        raise TypeError(f"emojihash() does not support {type(value).__name__}")
    return EMOJI[digest.digest()[0]]


def _update_from_stream(digest: hashlib.blake2b, stream: IO[bytes] | IO[str]) -> None:
    while chunk := stream.read(_CHUNK_SIZE):
        digest.update(chunk.encode() if isinstance(chunk, str) else chunk)
