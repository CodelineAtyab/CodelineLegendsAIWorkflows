"""Example usage of the analyze_text decorator."""

from decorators import analyze_text


@analyze_text(words=True, vowels=True)
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    greet("Alice")
