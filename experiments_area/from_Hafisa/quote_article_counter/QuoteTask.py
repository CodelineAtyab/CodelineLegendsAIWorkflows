import random


def create_quotes_file(file_path="quotes.txt"):
    quotes = [
        "A walk in Muttrah can make the day better.",
        "The mountains of Oman are full of beautiful views.",
        "An evening in Muscat can feel peaceful.",
        "A trip to Nizwa can teach you a lot about history.",
        "The sea in Oman is calm and beautiful.",
        "An early morning in Salalah can feel refreshing.",
        "A cup of Omani coffee can bring people together.",
        "The roads through Jebel Akhdar have amazing views.",
        "A visit to Sur can be an exciting adventure.",
        "An old fort can tell the story of Oman.",
        "The beaches of Oman are perfect for relaxing.",
        "A drive through the desert can be unforgettable.",
        "An Omani village can show beautiful traditions.",
        "The beauty of Oman is in its nature and culture.",
        "A weekend in Muscat can be full of activities.",
        "The markets in Oman are full of local products.",
        "An evening at Qurum beach can be very relaxing.",
        "A visit to Wadi Shab can be an amazing experience.",
        "The mountains and beaches make Oman special.",
        "An open road in Oman can lead to a beautiful place.",
    ]

    selected_quotes = random.sample(quotes, 15)

    try:
        with open(file_path, "w") as file:
            file.writelines(quote + "\n" for quote in selected_quotes)

    except OSError as error:
        print(f"Something went wrong: {error}")

    else:
        print("Quotes file created.")

    finally:
        print("Finished creating quotes.")


def append_result(
    line,
    article_counts,
    output_path="quotes_analysis.txt"
):
    try:
        with open(output_path, "a") as file:
            file.write(
                f"{{a: {article_counts['a']}, "
                f"an: {article_counts['an']}, "
                f"the: {article_counts['the']}}} "
                f"{line}\n"
            )

    except OSError as error:
        print(f"Something went wrong: {error}")


def analyze_quotes(
    input_path="quotes.txt",
    output_path="quotes_analysis.txt"
):
    try:
        with open(output_path, "w"):
            pass

        with open(input_path, "r") as file:
            for line in file:
                line = line.strip()

                article_counts = {
                    "a": 0,
                    "an": 0,
                    "the": 0
                }

                words = line.lower().split()

                for word in words:
                    word = word.strip(".,!?;:\"'")

                    if word == "a":
                        article_counts["a"] += 1

                    elif word == "an":
                        article_counts["an"] += 1

                    elif word == "the":
                        article_counts["the"] += 1

                append_result(
                    line,
                    article_counts,
                    output_path
                )

    except FileNotFoundError:
        print("quotes.txt does not exist.")

    except OSError as error:
        print(f"Something went wrong: {error}")

    else:
        print("Quotes analyzed successfully.")

    finally:
        print("Finished analyzing quotes.")