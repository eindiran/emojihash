"""Tests for emojihash: table shape, stability, per-type conversion, and the CLI."""

import io
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from emojihash import EMOJI, emojihash
from emojihash.cli import main


def test_table_has_1024_unique_single_code_point_emoji() -> None:
    assert len(EMOJI) == 1024
    assert len(set(EMOJI)) == 1024
    # U+231A WATCH is the lowest Emoji_Presentation code point.
    assert all(len(e) == 1 and ord(e) >= 0x231A for e in EMOJI)


@pytest.mark.parametrize(
    ("value", "index"),
    [("", 510), ("hello", 205), ("emojihash", 867), (42, 509), (3.14, 514)],
)
def test_output_is_stable(value: str | int | float, index: int) -> None:
    # Pinned so any change to the table or the hashing scheme fails loudly.
    assert emojihash(value) == EMOJI[index]


def test_text_and_bytes_like_match() -> None:
    expected = emojihash("hello")
    assert emojihash(b"hello") == expected
    assert emojihash(bytearray(b"hello")) == expected
    assert emojihash(memoryview(b"hello")) == expected


def test_numbers_hash_as_their_str() -> None:
    assert emojihash(42) == emojihash("42")
    assert emojihash(1.5) == emojihash("1.5")
    assert emojihash(1j) == emojihash("1j")
    assert emojihash(Decimal("1.10")) == emojihash("1.10")
    assert emojihash(Fraction(1, 3)) == emojihash("1/3")


def test_files_hash_their_contents(tmp_path: Path) -> None:
    path = tmp_path / "data.bin"
    path.write_bytes(b"hello")
    assert emojihash(path) == emojihash("hello")
    with path.open("rb") as f:
        assert emojihash(f) == emojihash("hello")
    assert emojihash(io.BytesIO(b"hello")) == emojihash("hello")
    assert emojihash(io.StringIO("hello")) == emojihash("hello")


def test_large_stream_matches_bytes() -> None:
    data = bytes(range(256)) * 1024
    assert emojihash(io.BytesIO(data)) == emojihash(data)


def test_str_is_never_a_path(tmp_path: Path) -> None:
    path = tmp_path / "data.bin"
    path.write_bytes(b"contents")
    assert emojihash(str(path)) == emojihash(str(path).encode())


@pytest.mark.parametrize("value", [None, [1, 2], {"a": 1}, object()])
def test_unsupported_types_raise(value: object) -> None:
    with pytest.raises(TypeError):
        emojihash(value)  # ty: ignore[invalid-argument-type]


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        emojihash(tmp_path / "missing")


def test_covers_whole_table() -> None:
    assert {emojihash(i) for i in range(10_000)} == set(EMOJI)


def test_cli_single_input(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["hello"]) == 0
    assert capsys.readouterr().out == f"{emojihash('hello')}\n"


def test_cli_multiple_inputs(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["a", "b"]) == 0
    assert capsys.readouterr().out == f"{emojihash('a')}\ta\n{emojihash('b')}\tb\n"


def test_cli_files(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "data.txt"
    path.write_bytes(b"hello")
    missing = tmp_path / "missing"
    assert main(["-f", str(path), str(missing)]) == 1
    captured = capsys.readouterr()
    assert captured.out == f"{emojihash('hello')}\t{path}\n"
    assert str(missing) in captured.err


def test_cli_stdin(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b"hello")))
    assert main([]) == 0
    assert capsys.readouterr().out == f"{emojihash('hello')}\n"
