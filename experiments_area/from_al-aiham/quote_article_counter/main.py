
import random

quotes = [
    "The sun rises over the mountains every morning.",
    "A journey of a thousand miles begins with a single step.",
    "An apple a day keeps the doctor away.",
    "The best way to learn is to practice every day.",
    "A good programmer understands the problem before writing the code.",
    "The future belongs to those who believe in a dream.",
    "An opportunity is a chance to make the world better.",
    "The more you practice, the better you become.",
    "A small mistake can teach an important lesson.",
    "The theme of the story is another mystery.",
    "An honest person always tells the truth.",
    "A developer needs an idea and the courage to build it.",
    "The road to success is a long and difficult journey.",
    "Another day brings a new opportunity to learn.",
    "The answer to a problem is not always the easiest one.",
    "An engineer can turn a simple idea into a useful tool.",
    "A book is a window into the world of knowledge.",
    "The teacher gave an example to the students.",
    "A strong team needs the trust of every member.",
    "The artist created a beautiful painting in an hour.",
    "An unexpected challenge can become a valuable experience.",
    "The Python language is a powerful tool for developers.",
    "A curious mind asks the questions others forget.",
    "The adventure begins with an idea and a plan.",
    "THE cat found A toy near AN old house.",
]


# Function 1: Create quotes file
def create_quotes_file(file_path="quotes.txt"):
    selected_quotes = random.sample(quotes, 15)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for quote in selected_quotes:
                file.writelines(quote + "\n")

    except OSError as error:
        print(f"Something went wrong: {error}")
        return False

    else:
        print("Quotes file created successfully.")
        return True


# Function 2: Append analysis result
def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    try:
        with open(output_path, "a", encoding="utf-8") as analyzed:
            analyzed.write(
                f"{{a: {article_counts['a']}, "
                f"an: {article_counts['an']}, "
                f"the: {article_counts['the']}}} "
                f"{line.strip()}\n"
            )

    except OSError as error:
        print(f"Something went wrong: {error}")
        raise


# Function 3: Analyze quotes
def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            # Clear old analysis results
            with open(output_path, "w", encoding="utf-8"):
                pass

            # Read quotes line by line
            for line in file:
                article_counts = {"a": 0, "an": 0, "the": 0}

                words = line.lower().split()

                for word in words:
                    word = word.strip(".,!?;:\"'")

                    if word in article_counts:
                        article_counts[word] += 1

                append_result(line, article_counts, output_path)

    except FileNotFoundError as error:
        if error.filename == input_path:
            print(f"The file '{input_path}' was not found.")
        else:
            print(f"File not found: {error}")

    except OSError as error:
        print(f"Something went wrong: {error}")

    else:
        print("Quotes analysis completed successfully.")


def main():
    if create_quotes_file():
        analyze_quotes()


if __name__ == "__main__":
    main()
