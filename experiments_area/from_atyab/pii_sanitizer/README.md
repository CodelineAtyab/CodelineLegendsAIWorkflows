# PII Sanitizer

A tiny command-line script that masks personal data in customer chat logs so the
logs can be shared for analysis. It streams the input file line by line, so it
works on large logs without loading them into memory.

## What gets masked

| Data | Rule | Example |
| --- | --- | --- |
| Email | Keep the domain, replace the local part with `***` | `john.doe@example.com` → `***@example.com` |
| Phone | Replace every digit with `*` | `+1 (555) 123-4567` → `+* (***) ***-****` |
| Card | Replace every digit in 12-16 digit runs with `*` | `<digits>` -> `**** **** **** ****` |

Card-like numbers are masked before phone numbers so the broader phone pattern
cannot swallow them.

## How to run

Requires Python 3.14+ (or [uv](https://docs.astral.sh/uv/)).

```bash
cd experiments_area/from_atyab/pii_sanitizer

# With uv (installs the dev dependencies from uv.lock)
uv run python sanitize.py --input sample.txt --output cleaned.txt

# Or with a plain Python install
python sanitize.py --input sample.txt --output cleaned.txt
```

The command prints how many lines were processed and writes the masked copy to
`cleaned.txt`:

```text
Sanitized 5 line(s) into cleaned.txt
```

Exit codes:

| Code | Meaning |
| --- | --- |
| `0` | Success |
| `1` | Input file not found |
| `2` | Another file/OS error |

## Tests, formatting, and type checking

```bash
cd experiments_area/from_atyab/pii_sanitizer

uv run pytest                        # unit tests
uvx ruff format .                    # format
uvx ruff@0.16.10 check .             # lint (same version as CI)
uv run --frozen --with 'mypy==2.4.0' mypy --ignore-missing-imports .
uv run --frozen --with 'mypy==2.4.0' mypy --strict sanitize.py
```

## Debugging in VS Code

1. Open the repository root in VS Code.
2. Create `.vscode/launch.json` (the folder is git-ignored) with:

   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Sanitize sample.txt",
         "type": "debugpy",
         "request": "launch",
         "program": "${workspaceFolder}/experiments_area/from_atyab/pii_sanitizer/sanitize.py",
         "args": ["--input", "sample.txt", "--output", "cleaned.txt"],
         "cwd": "${workspaceFolder}/experiments_area/from_atyab/pii_sanitizer",
         "console": "integratedTerminal",
         "justMyCode": true
       }
     ]
   }
   ```

3. Set a breakpoint inside `read_lines` or `mask_line`, then press <kbd>F5</kbd>.
   Because the file is read lazily, the breakpoint in the generator fires once
   per line — you can step through and watch each line being masked.

If VS Code cannot find the interpreter, run `uv sync` in the project folder and
select `.venv/bin/python` with **Python: Select Interpreter**.

## Why a generator instead of reading the whole file?

`read_lines` is a generator:

```python
def read_lines(path: str | Path) -> Iterator[str]:
    with open(path, encoding="utf-8") as handle:
        yield from handle
```

- **Constant memory:** only the current line is held in memory, so a 2 GB log
  uses the same memory as a 2 KB one.
- **Streaming:** the first line can be masked before the rest of the file is
  read, which keeps startup fast and enables pipes or network streams later.
- **Predictable:** no `readlines()` list of every line, and no accidental
  duplication of the file in memory.

The trade-off is that a generator can only be consumed once; if the same data is
needed twice, re-open the file or materialise it deliberately.
