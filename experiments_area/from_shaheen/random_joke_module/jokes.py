import random

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why do Java developers wear glasses? Because they don't C#.",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
    "Why did the developer go broke? Because he used up all his cache.",
    "What is a programmer's favourite hangout place? Foo Bar.",
    "Why was the computer cold? It left its Windows open.",
    "Why did the function return early? It had a date with a break statement.",
    "What do you call 8 hobbits? A hobbyte.",
    "Why do Python programmers have low self-esteem? They're constantly comparing their self to others.",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
]


def get_random_joke():
    return random.choice(JOKES)


def get_random_jokes(count):
    return random.sample(JOKES, min(count, len(JOKES)))
