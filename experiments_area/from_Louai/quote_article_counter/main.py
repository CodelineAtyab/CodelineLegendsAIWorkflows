import random


def create_quotes_file(file_path="quotes.txt"):
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "An apple a day keeps the doctor away.",
        "The journey of a thousand miles begins with a single step.",
        "To be or not to be, that is the question.",
        "A room without books is like a body without a soul.",
        "The only thing we have to fear is fear itself.",
        "An unexamined life is not worth living.",
        "Where there is a will, there is a way.",
        "The mind is everything. What you think you become.",
        "Life is what happens when you are busy making other plans.",
        "A change is as good as a rest.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "An investment in knowledge pays the best interest.",
        "The secret of getting ahead is getting started.",
        "A person who never made a mistake never tried anything new.",
        "Design is not just what it looks like and feels like. Design is how it works. - Steve Jobs",
    ]

    selected_quotes = random.sample(quotes, 15)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(f"{quote}\n" for quote in selected_quotes)


def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    a_count = article_counts.get("a", 0)
    an_count = article_counts.get("an", 0)
    the_count = article_counts.get("the", 0)

    formatted_line = (
        f"{line.strip()} | a: {a_count}, an: {an_count}, the: {the_count}\n"
    )

    with open(output_path, "a", encoding="utf-8") as output_file:
        output_file.write(formatted_line)


def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            for line in file:
                clean_line = line.strip()
                words = clean_line.split()

                counts = {"a": 0, "an": 0, "the": 0}

                for word in words:
                    cleaned_word = word.strip(".,!?;:\"'").lower()
                    if cleaned_word in counts:
                        counts[cleaned_word] += 1

                append_result(clean_line, counts, output_path)

    except FileNotFoundError:
        print(f"error: file '{input_path}' not found! Please create it first.")
    except OSError as error:
        print(f"An error occurred while handling the file: {error}")
    else:
        print("Analysis completed successfully without errors!")
    finally:
        print("Attempt to analyze quotes file completed.")


if __name__ == "__main__":
    with open("quotes_analysis.txt", "w", encoding="utf-8") as f:
        pass

    create_quotes_file()
    analyze_quotes()
