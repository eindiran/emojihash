"""
Map arbitrary input to a short string of emoji.

The input is converted to bytes and hashed with SHAKE256. Each emoji takes the next 10 bits
of the output stream as an index into the 1024-entry table in `EMOJI`. Because the bits are
read from the front of the stream, a shorter result is always a prefix of a longer one for
the same input. Output is stable across processes, platforms, and Python versions, unlike
the builtin `hash()`, which is salted per process for `str` and `bytes`.

NOT CRYPTOGRAPHICALLY SECURE. With the default length of 1 there are only 1024 possible
outputs: two unrelated inputs match with probability 1/1024, and anyone can find an input
that maps to a chosen emoji in about a thousand tries. Each extra emoji multiplies the output
space by 1024, which makes accidental collisions rarer, but no length makes this a security
tool: lookalike emoji and per-platform rendering make visual comparison unreliable. Use it
for visual tagging (log lines, shell prompts, build IDs, hosts), never for authentication,
integrity checks, or key verification.
"""

import hashlib
import io
import os
from collections.abc import Iterator
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
# log2(len(EMOJI)); the table size must stay a power of two so every index is equally likely.
_BITS_PER_EMOJI = 10
_INDEX_MASK = len(EMOJI) - 1


def emojihash(value: EmojiHashable, length: int = 1) -> str:
    """
    Return `length` emoji for `value`. Not cryptographically secure; see the module docstring.

    Each emoji is a single code point, so `len()` of the result equals `length`, and
    `emojihash(v, n)` is always a prefix of `emojihash(v, m)` for `n < m`.

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

    Raises `ValueError` if `length < 1`, `TypeError` for an unsupported input type, and
    `OSError` if a path cannot be read.
    """
    if length < 1:
        raise ValueError(f"length must be >= 1, got {length}")
    hasher = hashlib.shake_256()
    for chunk in _byte_chunks(value):
        hasher.update(chunk)
    n_bits = length * _BITS_PER_EMOJI
    n_bytes = -(-n_bits // 8)
    # Drop the trailing bits past n_bits so index 0 comes from the first 10 bits of the stream.
    bits = int.from_bytes(hasher.digest(n_bytes)) >> (n_bytes * 8 - n_bits)
    return "".join(
        EMOJI[(bits >> (_BITS_PER_EMOJI * (length - 1 - i))) & _INDEX_MASK] for i in range(length)
    )


def _byte_chunks(value: EmojiHashable) -> Iterator[bytes]:
    if isinstance(value, str):
        yield value.encode()
    elif isinstance(value, bytes | bytearray | memoryview):
        yield bytes(value)
    elif isinstance(value, _NUMBER_TYPES):
        yield str(value).encode()
    elif isinstance(value, os.PathLike):
        with open(value, "rb") as f:
            yield from _stream_chunks(f)
    elif isinstance(value, io.IOBase):
        yield from _stream_chunks(value)
    else:
        raise TypeError(f"emojihash() does not support {type(value).__name__}")


def _stream_chunks(stream: IO[bytes] | IO[str]) -> Iterator[bytes]:
    while chunk := stream.read(_CHUNK_SIZE):
        yield chunk.encode() if isinstance(chunk, str) else chunk
