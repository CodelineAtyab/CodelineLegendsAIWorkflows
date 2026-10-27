import sys

from jokes import get_random_joke, get_random_jokes


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


def run_interactive():
    print("Joke bot! Press Enter for a joke, or type 'exit' / 'quit' to stop.")
    while True:
        user_input = input("> ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(get_random_joke())


def main():
    if len(sys.argv) > 1:
        run_non_interactive(parse_count(sys.argv[1]))
    else:
        run_interactive()


if __name__ == "__main__":
    main()
