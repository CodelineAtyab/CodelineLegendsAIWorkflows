import random
import re

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
        "a friend is kind."
    ]

#select 15 random qoutes from the list for that i use (import random) to use built-in function sample.random
    selected_qoutes = random.sample(quotes ,15)

#here to write the 15 random qoutes in the file
    with open(file_path ,"w") as file: #because i used "w" everytime will write it and replace it with the old one
        for qoute in selected_qoutes : # loops through the 15 selected quotes.
            file.write(qoute + "\n")
            
create_quotes_file()

#open the file to read 
def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    with open (input_path, "r") as f:
        for line in f:  #to read each line
            line = line.strip()
            
            #add dictionary to count articles( a, an ,the)
            article_counts = {
                "a": 0,
                "an": 0,
                "the": 0
            }
            
            # to find articles as whole words
            pattern = re.compile(r"\b(a|an|the)\b") #re.compile Prepares a search pattern.
            articles = pattern.findall(line.lower())
            
            # Count each article
            for article in articles:
                article_counts[article] += 1
    
            print(line, article_counts)
            
analyze_quotes()