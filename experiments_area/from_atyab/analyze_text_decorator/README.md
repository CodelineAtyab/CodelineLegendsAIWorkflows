# Analyze Text Decorator

A reusable `@analyze_text` decorator that prints simple statistics about the
string returned by any function, without changing that function's code or
result.

## Usage

```python
from decorators import analyze_text


@analyze_text(words=True, vowels=True)
def greet(name: str) -> str:
    return f"Hello, {name}!"


greet("Alice")
```

Output:

```text
Words: 2
Vowels: 5
```

The decorator accepts three keyword-only flags. Only the requested metrics are
printed, in this order:

| Flag | Prints | Counts |
| --- | --- | --- |
| `words=True` | `Words: <n>` | Whitespace-separated words (`str.split()`) |
| `vowels=True` | `Vowels: <n>` | `a e i o u`, case-insensitive |
| `spaces=True` | `Spaces: <n>` | Literal space characters only |

When all flags are omitted or `False`, the decorator prints nothing and returns
the decorated function's result unchanged.

## Run the example

Requires Python 3.14+ or [uv](https://docs.astral.sh/uv/).

```bash
cd experiments_area/from_atyab/analyze_text_decorator
uv run python example.py
```

## Tests and checks

```bash
cd experiments_area/from_atyab/analyze_text_decorator

uv run pytest
uvx ruff@0.16.10 check .
uvx ruff@0.16.10 format --check .
uv run --frozen --with 'mypy==2.4.0' mypy --ignore-missing-imports .
```
