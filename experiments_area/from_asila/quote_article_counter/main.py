import random

def create_quotes_file(file_path="quotes.txt"):

    # List of 20 quotes
    quotes = [
        "The sun is bright.",
        "A cat is sleeping.",
        "An apple is red.",
        "The sky is blue.",
        "A dog is running.",
        "An egg is small.",
        "The moon is shining.",
        "A bird can fly.",
        "An idea is great.",
        "The weather is nice.",
        "A book is useful.",
        "An ant is tiny.",
        "The food is ready.",
        "A flower is beautiful.",
        "An owl can fly.",
        "The water is cold.",
        "A student is learning.",
        "An orange is sweet.",
        "The day is sunny.",
        "A friend is kind."
    ]

#select 15 random qoutes from the list for that i use (import random) to use built-in function sample.random
    selected_qoutes = random.sample(quotes ,15)

