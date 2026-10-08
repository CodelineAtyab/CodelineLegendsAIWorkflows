Text Analyzer Decorator

This Python project demonstrates how to create and use a custom decorator to analyze text.

The program defines three helper functions to calculate:

Number of words using split()

Number of spaces using count(" ")

Number of uppercase characters using isupper()

The main text_analyzer() function is a decorator factory that allows us to choose which text statistics should be calculated. It uses a nested decorator() function and a wrapper() function with *args and **kwargs so that it can work with different function arguments.

The @text_analyzer() decorator is applied to the get_news() function. When get_news() is called, the decorator analyzes the returned text and adds a summary containing the selected statistics before the original text.

Example

For the input:

The Codeline Legends team is learning Python decorators in Muscat this week.

The program produces output similar to:

[ No. of Words: 12, No. of Spaces: 11, No. of Uppercase Chars: 4 ] The Codeline Legends team is learning Python decorators in Muscat this week.

Concepts Demonstrated

1- Python decorators

2- Decorator factories

3- Nested functions

4- *args and **kwargs

5- String methods such as split(), count(), and isupper()

6- Higher-order functions

7- Conditional execution inside decorators

The project demonstrates how decorators can be used to add extra functionality to an existing function without modifying the original function itself.