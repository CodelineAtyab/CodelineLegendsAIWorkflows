
import random


# Function 1: Create quotes file
def create_quotes_file(file_path="quotes.txt"):

    quotes = [
    "The sea is calm and beautiful in the morning.",
    "A walk along the beach brings peace to the mind.",
    "An ocean breeze makes the day feel fresh.",
    "The waves dance gently along the shore.",
    "A sunset over the ocean is a beautiful sight.",
    "The deep blue sea is full of mysteries.",
    "An adventure in the ocean can be unforgettable.",
    "A boat sailing across the sea looks peaceful.",
    "The sound of the waves helps people relax.",
    "An island in the ocean is a wonderful place to visit.",
    "The ocean is home to many amazing creatures.",
    "A dolphin swimming in the sea is a beautiful sight.",
    "The beach is the perfect place to enjoy nature.",
    "An early morning by the sea feels refreshing.",
    "A beautiful seashell can be found on the shore.",
    "The ocean connects different places around the world.",
    "An underwater adventure reveals the beauty of marine life.",
    "A gentle wave touches the golden sand.",
    "The sea becomes magical under the moonlight.",
    "A peaceful evening by the ocean makes the heart happy.",
    "The ocean's vastness inspires awe and wonder.",]
      

    try:
        selected_quotes = random.sample(quotes, 15)

        with open(file_path, "w") as file:
            for quote in selected_quotes:
                file.write(quote + "\n")

    except OSError as error:
        print(f"Error creating quotes file: {error}")

    else:
        print("Quotes file created successfully.")


# Function 2: Append result to file
def append_result(line, article_counts, output_path="quotes_analysis.txt"):

    with open(output_path, "a") as file:
        file.write(
            f'{{a: {article_counts["a"]}, '
            f'an: {article_counts["an"]}, '
            f'the: {article_counts["the"]}}} '
            f'{line}\n'
        )


# Function 3: Analyze quotes
def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):

    try:
        with open(input_path, "r") as file:

            with open(output_path, "w") as output_file:
                pass

            for line in file:

                line = line.strip()

                words = line.lower().split()

                article_counts = {
                    "a": 0,
                    "an": 0,
                    "the": 0
                }

                for word in words:
                    word = word.strip(".,!?;:\"'")

                    if word in article_counts:
                        article_counts[word] += 1

                append_result(line, article_counts, output_path)

    except FileNotFoundError:
        print("Quotes file not found.")

    except OSError as error:
        print(f"File error: {error}")

    else:
        print("Quotes analyzed successfully.")

    finally:
        print("Analysis finished.")


# Run the program
if __name__ == "__main__":

    create_quotes_file()

    analyze_quotes()
