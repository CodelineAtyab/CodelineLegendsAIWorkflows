# Quote Article Counter

## Description
This project generates 15 random quotes and counts the occurrences of the articles **"a", "an", and "the"** in each quote.

## Features
- Selects 15 random quotes from a list.
- Saves quotes to `quotes_file.txt`.
- Counts articles using regular expressions.
- Saves the results to `quotes_analysis.txt`.
- Handles file errors using exception handling.

## How to Run
Run the following command:

```bash
uv run main.py
```

## Output Files
- `quotes_file.txt` — Contains the 15 selected quotes.
- `quotes_analysis.txt` — Contains each quote with its article counts.

## Technologies
- Python 3.14
- `random` and `re` modules
- File handling and exception handling