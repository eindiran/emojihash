# emojihash

Map an arbitrary string, number, byte string, or file to an emoji, or to a short string of
emoji when you need fewer collisions.

## Not cryptographically secure

With the default length of 1 there are only 1024 possible outputs. Two unrelated inputs share
an emoji with probability 1/1024, and an input that maps to a chosen emoji can be found in
about a thousand tries. A longer output makes accidental collisions rarer, but no length makes
this a security tool: lookalike emoji and per-platform rendering make visual comparison
unreliable. Use it for visual tagging: log lines, shell prompts, build IDs, telling hosts
apart at a glance. Do not use it for authentication, integrity checks, or key verification.

| Length | Outputs | ~50% chance of any collision after |
| --- | --- | --- |
| 1 | 2^10 | 38 inputs |
| 2 | 2^20 | 1,200 inputs |
| 3 | 2^30 | 39,000 inputs |
| 4 | 2^40 | 1.2 million inputs |

## Install

```bash
pip install git+https://github.com/eindiran/emojihash
```

Requires Python >= 3.12. No runtime dependencies.

## Library

```python
from pathlib import Path
from emojihash import emojihash

emojihash("hello")  # str
emojihash(b"hello")  # same emoji as "hello"
emojihash(42)  # same emoji as "42"
emojihash(Path("notes.txt"))  # file contents
with open("notes.txt", "rb") as f:
    emojihash(f)  # same emoji as the Path form

emojihash("hello", 4)  # four emoji; starts with emojihash("hello")
```

| Input | Bytes hashed |
| --- | --- |
| `str` | UTF-8 encoding; a `str` is never treated as a path |
| `bytes`, `bytearray`, `memoryview` | raw bytes |
| `int`, `float`, `complex`, `Decimal`, `Fraction` | UTF-8 of `str(value)`, so `1` and `1.0` differ |
| `bool` | UTF-8 of `"True"` or `"False"` (an `int` subclass, but `str()` differs from `1`/`0`) |
| `os.PathLike` | file contents, binary mode |
| open file object | remaining contents; text-mode files are re-encoded as UTF-8 |

Any other type raises `TypeError`; `length < 1` raises `ValueError`. `EMOJI` exposes the 1024-entry table.

## CLI

```bash
emojihash hello
```

```bash
emojihash -f a.txt b.txt
```

```bash
echo -n hello | emojihash
```

```bash
emojihash -n 4 hello
```

`-n`/`--length` sets the number of emoji per input (default 1). One input prints only the
emoji. Several print `<emoji>\t<input>` per line. Exit status is 1
if any file could not be read.

## How it works

SHAKE256 over the input bytes; each emoji takes the next 10 bits of the output stream as an
index into the table in `src/emojihash/_table.py`. Reading from the front of the stream makes
a shorter result a prefix of a longer one. Output is stable across processes, platforms, and Python
versions. Changing the table order changes every mapping.

The table holds every single-code-point emoji with default emoji presentation as of Unicode
13.0 (2020), minus 89 lookalikes (clock faces, moon phases, zodiac signs, and similar). Fonts
from before 2020 may be missing some entries.

## Development

```bash
python3 -m venv .venv && .venv/bin/pip install -e . pre-commit pytest ruff ty
```

```bash
.venv/bin/pre-commit install
```

```bash
.venv/bin/pre-commit run --all-files
```

Pre-commit runs Ruff (lint and format), Ty, yamllint, and pytest.

## License

MIT
