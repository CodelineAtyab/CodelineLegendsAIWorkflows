# ruff: noqa
import random



def create_quotes_file(file_path="quotes.txt"):

    # List of 20 quotes
    quotes = [
        "The sun is bright.",
        "a cat is sleeping.",
        "an apple is red.",
        "the sky is blue.",
        "a dog is running.",
        "an egg is small.",
        "the moon is shining.",
        "a bird can fly.",
        "an idea is great.",
        "the weather is nice.",
        "a book is useful.",
        "an ant is tiny.",
        "the food is ready.",
        "a flower is beautiful.",
        "an owl can fly.",
        "the water is cold.",
        "a student is learning.",
        "an orange is sweet.",
        "the day is sunny.",
        "a friend is kind.",
    ]

    # select 15 random qoutes from the list for that i use (import random) to use built-in function sample.random
    selected_qoutes = random.sample(quotes, 15)
    try:
        # here to write the 15 random qoutes in the file
        with (
            open(file_path, "w") as file
        ):  # because i used "w" everytime will write it and replace it with the old one
            for qoute in selected_qoutes:  # loops through the 15 selected quotes.
                file.write(qoute + "\n")

    except OSError as error:
        print("Error writing quotes:", error)

    else:
        print("Quotes file created successfully.")


# open the file to read
def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):

    try:
        with open(input_path, "r") as f:
            for line in f:  # to read each line
                line = line.strip()

                # add dictionary to count articles( a, an ,the)
                article_counts = {"a": 0, "an": 0, "the": 0}

                # Convert the line to lowercase and split it into words
                words = line.lower().split()

                # to find articles as whole words
                # Count each article
                for word in words:
                    word = word.strip(".,!?;:\"'")

                    if word in article_counts:
                        article_counts[word] += 1

                #save the result inside quotes_analysis.txt
                append_result(line, article_counts, output_path)
                print(line, article_counts)

    except FileNotFoundError:
        print("quotes.txt does not exist!")


def append_result(line, article_counts, output_path="quotes_analysis.txt"):

    try:
        # open the file in append mode
        with open(output_path, "a") as f:  # Appends text without deleting old content.
            # Format the article counts and original quote
            result = f"{{a: {article_counts['a']}, an: {article_counts['an']}, the: {article_counts['the']}}} {line}\n"

            f.write(result)  # writes exactly one line

    except OSError as error:
        print("Error writing analysis:", error)

    return


create_quotes_file()
analyze_quotes()
