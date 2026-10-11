
import random
import re

#  Write 15 randomly selected quotes to a text file 
def create_quotes_file(file_path="quotes.txt"):
   
    quotes = [
        "The best time to plant a tree is now.",
        "Knowledge is power.",
        "The future belongs to those who believe in their dreams.",
        "Success is the sum of small efforts repeated daily.",
        "A journey of a thousand miles begins with a single step.",
        "The secret of getting ahead is getting started.",
        "Learning never exhausts the mind.",
        "Believe you can and you are halfway there.",
        "The only way to do great work is to love what you do.",
        "Practice makes progress.",
        "Every moment is a fresh beginning.",
        "It always seems impossible until it is done.",
        "Great things are done by a series of small things.",
        "The second best time to start is today.",
        "Do what you can with what you have.",
        "A little progress each day adds up to big results.",
        "Action is the foundational key to success.",
        "Dream big and start small.",
        "Never stop learning.",
        "Hard work beats talent when talent does not work hard.",
    ]
    
    # chooses 15 quotes from the quotes list and save them in a list 
    selected_quotes = random.sample(quotes, 15)


    with open(file_path, "w", encoding="utf-8") as file:
        for quote in selected_quotes:
            file.write(quote + "\n")

# Append one formatted analysis line and return it.
def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    
    result = (
        f"[a: {article_counts['a']}, "
        f"an: {article_counts['an']}, "
        f"the: {article_counts['the']}] {line}"
    )

    with open(output_path, "a", encoding="utf-8") as file:
        file.write(result + "\n")

    return result

# Count articles in each quote and append the results
def analyze_quotes(input_path="quotes.txt",output_path="quotes_analysis.txt"):
    # re.IGNORECASE means uppercase and lowercase letters are treated the same
    article_pattern = re.compile(r"\b(a|an|the)\b", re.IGNORECASE)

    try:
        # Clear previous analysis so each run produces 15 lines.
        with open(output_path, "w", encoding="utf-8"):
            pass

        with open(input_path, "r", encoding="utf-8") as file:
            for line in file:
                original_line = line.strip()

                matches = article_pattern.findall(original_line)
                article_counts = {
                    "a": 0,
                    "an": 0,
                    "the": 0,
                }

                for match in matches:
                    article_counts[match.lower()] += 1
                
                # to print the analysis result in the output file
                append_result(
                    original_line,
                    article_counts,
                    output_path,
                )

        print("Quote analysis completed successfully.")

    except FileNotFoundError:
        print(f"Error: The input file '{input_path}' does not exist.")

    except OSError as error:
        print(f"File operation failed: {error}")

    finally:
        print("Done trying to analyze quotes.")


def main():
    try:
        create_quotes_file()
        analyze_quotes()

    except OSError as error:
        print(f"Could not create the quotes file: {error}")


if __name__ == "__main__":
    main()
