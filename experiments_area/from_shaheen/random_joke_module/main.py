import sys

from jokes import get_random_jokes


def parse_count(text):
    try:
        count = int(text)
    except ValueError:
        raise SystemExit(f"Error: '{text}' is not a valid number of jokes.")
    if count < 1:
        raise SystemExit(f"Error: '{text}' is not a valid number of jokes.")
    return count


def run_non_interactive(count):
    for number, joke in enumerate(get_random_jokes(count), start=1):
        print(f"{number}. {joke}")


def main():
    if len(sys.argv) > 1:
        run_non_interactive(parse_count(sys.argv[1]))


if __name__ == "__main__":
    main()
