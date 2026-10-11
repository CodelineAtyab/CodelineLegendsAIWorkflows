import random

QUOTES = [
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "A journey of a thousand miles begins with a single step.",
    "An apple a day keeps the doctor away.",
    "The early bird catches the worm.",
    "A picture is worth a thousand words.",
    "The pen is mightier than the sword.",
    "An ounce of prevention is worth a pound of cure.",
    "A rolling stone gathers no moss.",
    "The only way to do great work is to love what you do.",
    "Actions speak louder than words.",
    "A chain is only as strong as its weakest link.",
    "The grass is always greener on the other side of the fence.",
    "An idle mind is the devil's workshop.",
    "Knowledge is power.",
    "A friend in need is a friend indeed.",
    "The squeaky wheel gets the grease.",
    "Rome was not built in a day.",
    "A watched pot never boils.",
    "The apple does not fall far from the tree.",
    "An empty vessel makes the most noise.",
    "Fortune favors the bold.",
    "A bird in the hand is worth two in the bush.",
]


def create_quotes_file(file_path="quotes.txt"):
    selected = random.sample(QUOTES, 15)
    try:
        with open(file_path, "w") as file:
            file.writelines(quote + "\n" for quote in selected)
    except PermissionError:
        print(f"No permission to write {file_path}.")
    except OSError as error:
        print(f"Could not write {file_path}: {error}")
    else:
        print(f"Wrote {len(selected)} quotes to {file_path}")


def count_articles(line):
    counts = {"a": 0, "an": 0, "the": 0}
    for word in line.lower().split():
        word = word.strip(".,!?;:\"'()-")
        if word in counts:
            counts[word] += 1
    return counts


def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    formatted = (
        f"{{a: {article_counts['a']}, an: {article_counts['an']}, "
        f"the: {article_counts['the']}}} {line}\n"
    )
    with open(output_path, "a") as file:
        file.write(formatted)


def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r") as file:
            with open(output_path, "w"):
                pass
            for line in file:
                line = line.strip()
                if not line:
                    continue
                append_result(line, count_articles(line), output_path)
    except FileNotFoundError:
        print(f"'{input_path}' not found. Run create_quotes_file() first.")
    except PermissionError:
        print(f"No permission to read {input_path} or write {output_path}.")
    except OSError as error:
        print(f"Something went wrong while analyzing quotes: {error}")
    else:
        print(f"Analysis written to {output_path}")


create_quotes_file()
analyze_quotes()
