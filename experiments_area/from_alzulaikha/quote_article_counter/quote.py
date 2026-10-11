import random

# Function1 create_quotes_file with 15 random quotes
def create_quotes_file(file_path="quotes.txt"):
    quotes = [
    "A brave person never gives up.",
    "The ocean is full of hidden wonders.",
    "An old friend is a special treasure.",
    "A new day brings new hope.",
    "The moon looks beautiful tonight.",
    "An active mind loves to learn.",
    "A warm smile can spread happiness.",
    "The little things make life special.",
    "An amazing story begins with an idea.",
    "A clear goal helps you succeed.",
    "The rain makes the flowers grow.",
    "An empty mind cannot learn much.",
    "A good habit improves your life.",
    "The right choice can change everything.",
    "An unexpected moment can bring joy.",
    "A strong team works together.",
    "The morning breeze feels refreshing.",
    "An interesting book opens new doors.",
    "A little kindness goes a long way.",
    "The road to success starts with effort.",
    ]


    selected_quotes = random.sample(quotes, 15)
    try:
        with open(file_path, "w") as file:
            file.writelines(quote + "\n" for quote in selected_quotes)

    except OSError as error:
        print(f"Error creating quotes file: {error}")
    else:
        print("Quotes file created successfully.")

#Function 2 reads the quotes and counts articles per line
def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r") as file:
            for line in file:
                line = line.strip()
                article_counts = {"a": 0, "an": 0, "the": 0}

                words = line.lower().split()

                for word in words:
                    word = word.strip(".,!?;:\"'()[]")

                    if word in article_counts:
                        article_counts[word] += 1

                        append_result(line, article_counts, output_path)

    except FileNotFoundError:
        print(f"Input file not found: {input_path}")
    except OSError as error:
        print(f"Error reading quotes file: {error}")
    else:
        print("Quotes analyzed successfully.")

# Function 3  appends one formatted line and returns
def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    try:
        with open(output_path, "a") as file:
            result = (
                f"{{a: {article_counts['a']}, "
                f"an: {article_counts['an']}, "
                f"the: {article_counts['the']}}} {line}\n"
            )
            file.write(result)
            return result

    except OSError as error:
        print(f"Error writing analysis results: {error}")
        return None


# Run the functions
create_quotes_file()

with open("quotes_analysis.txt", "w"):
    pass

analyze_quotes()
