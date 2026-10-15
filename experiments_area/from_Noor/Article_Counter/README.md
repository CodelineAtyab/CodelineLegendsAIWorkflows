The Quote Article Counter is a Python program that generates a collection of random quotes, counts the occurrences of the English articles a, an, and the in each quote, and saves the results to a text file.

The project demonstrates file handling, regular expressions, dictionaries, functions, and exception handling in Python.

Features:

1- Generate random quotes: Selects 15 random quotes from a predefined list.

2- Analyze articles: Counts occurrences of a, an, and the in each quote.

3- Case-insensitive matching: Counts articles regardless of capitalization.

4- Save analysis results: Writes the article counts alongside each quote in an output file.

5- Handle file errors: Uses exception handling to manage missing files and other file   operation errors.

6- Manage files safely: Uses with statements to ensure files are closed automatically.

Project Structure:
quote_article_counter/
├── main.py
├── quotes.txt
└── quotes_analysis.txt

main.py: Contains the functions for generating quotes, analyzing articles, and saving results.

quotes.txt: Stores the randomly selected quotes.

quotes_analysis.txt: Stores the article counts and corresponding quotes.

The text files are generated or updated when the program runs.