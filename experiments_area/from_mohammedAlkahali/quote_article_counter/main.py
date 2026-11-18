import random

QUOTES_FILE = "quotes.txt"
ANALYSIS_FILE = "quotes_analysis.txt"

QUOTES = [
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "An apple a day keeps the doctor away.",
    "A journey of a thousand miles begins with a single step.",
    "The only way to do great work is to love what you do.",
    "An investment in knowledge pays the best interest.",
    "A picture is worth a thousand words.",
    "The early bird catches the worm.",
    "Knowledge is power.",
    "An idea is only as good as the action behind it.",
    "The secret of getting ahead is getting started.",
    "A smooth sea never made a skilled sailor.",
    "Practice makes perfect.",
    "The pen is mightier than the sword.",
    "An ounce of prevention is worth a pound of cure.",
    "Actions speak louder than words.",
    "A goal without a plan is just a wish.",
    "The best way to predict the future is to create it.",
    "Simplicity is the soul of efficiency.",
    "An expert is a person who has made all the mistakes in a narrow field.",
    "Theory without practice is another kind of guessing.",
    "Every expert was once a beginner.",
    "The harder you work, the luckier you get.",
]


def create_quotes_file(file_name):
    selected = random.sample(QUOTES, 15)
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            for quote in selected:
                file.write(quote + "\n")
    except OSError as error:
        print(f"Could not write {file_name}: {error}")
    else:
        print(f"Wrote {len(selected)} quotes to {file_name}")


def count_articles(text):
    counts = {"a": 0, "an": 0, "the": 0}
    for word in text.lower().split():
        clean_word = word.strip(".,!?;:\"'")
        if clean_word in counts:
            counts[clean_word] += 1
    return counts


def append_result(file_name, line, counts):
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(
            f"{{a: {counts['a']}, an: {counts['an']}, the: {counts['the']}}} {line}\n"
        )


def analyze_quotes(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            # Clear old results only after we know the input exists,
            # so every run produces a fresh file with one line per quote.
            with open(output_file, "w", encoding="utf-8"):
                pass

            for line in file:
                quote = line.strip()
                if not quote:
                    continue
                counts = count_articles(quote)
                append_result(output_file, quote, counts)
    except FileNotFoundError:
        print(f"'{input_file}' does not exist yet. Create the quotes file first.")
    except OSError as error:
        print(f"Something went wrong while working with the files: {error}")
    else:
        print(f"Analysis saved to {output_file}")
    finally:
        print("Analysis step finished.")


def main():
    create_quotes_file(QUOTES_FILE)
    analyze_quotes(QUOTES_FILE, ANALYSIS_FILE)


if __name__ == "__main__":
    main()