# emojihash

Map an arbitrary string, number, byte string, or file to a single emoji.

## Not cryptographically secure

There are only 256 possible outputs. Two unrelated inputs share an emoji with probability
1/256, and an input that maps to a chosen emoji can be found in a few hundred tries. Use it
for visual tagging: log lines, shell prompts, build IDs, telling hosts apart at a glance. Do
not use it for authentication, integrity checks, or key verification.

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
```

| Input | Bytes hashed |
| --- | --- |
| `str` | UTF-8 encoding; a `str` is never treated as a path |
| `bytes`, `bytearray`, `memoryview` | raw bytes |
| `int`, `float`, `complex`, `Decimal`, `Fraction` | UTF-8 of `str(value)`, so `1` and `1.0` differ |
| `os.PathLike` | file contents, binary mode |
| open file object | remaining contents; text-mode files are re-encoded as UTF-8 |

Any other type raises `TypeError`. `EMOJI` exposes the 256-entry table.

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

One input prints only the emoji. Several print `<emoji>\t<input>` per line. Exit status is 1
if any file could not be read.

## How it works

BLAKE2b with a 1-byte digest over the input bytes; the byte indexes the table in
`src/emojihash/_table.py`. Output is stable across processes, platforms, and Python
versions. Changing the table order changes every mapping.

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
