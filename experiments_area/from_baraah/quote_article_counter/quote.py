import random


# Function1 Create a file with 15 random quotes
def create_quotes_file(file_path="quotes.txt"):
    quotes = [
        "A good friend makes life better.",
        "The sky is full of beautiful stars.",
        "An opportunity can change your future.",
        "A happy heart makes a happy life.",
        "The journey is more important than the destination.",
        "An early start makes a productive day.",
        "A smile can make someone's day better.",
        "The smallest actions can make a big difference.",
        "A strong mind can overcome challenges.",
        "An exciting adventure begins with a plan.",
        "The best lessons come from experience.",
        "A simple idea can lead to success.",
        "An important decision can change everything.",
        "The beauty of life is in the little things.",
        "A new challenge is an opportunity to grow.",
        "The best time to start is now.",
        "A journey begins with a single step.",
        "An honest person earns the trust of others.",
        "The future depends on what you do today.",
        "A little progress every day matters.",
    ]

    selected_quotes = random.sample(quotes, 15)

    try:
        with open(file_path, "w") as file:
            for quote in selected_quotes:
                file.write(quote + "\n")

    except OSError as error:
        print(f"Error creating quotes file: {error}")

    else:
        print("Quotes file created successfully.")


# Function2 Read quotes and count articles
def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r") as file:
            for line in file:
                line = line.strip()
                words = line.lower().split()

                article_counts = {
                    "a": 0,
                    "an": 0,
                    "the": 0,
                }

                for word in words:
                    word = word.strip(".,!?;:\"'")

                    if word in article_counts:
                        article_counts[word] += 1

                append_result(line, article_counts, output_path)

    except FileNotFoundError:
        print("Quotes file does not exist.")

    except OSError as error:
        print(f"Error reading file: {error}")

    else:
        print("Quotes analyzed successfully.")


# Function3 Append one result to the output file
def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    with open(output_path, "a") as file:
        result = (
            f"{{a: {article_counts['a']}, "
            f"an: {article_counts['an']}, "
            f"the: {article_counts['the']}}} {line}\n"
        )

        file.write(result)


# Run the functions
create_quotes_file()

with open("quotes_analysis.txt", "w"):
    pass

analyze_quotes()
