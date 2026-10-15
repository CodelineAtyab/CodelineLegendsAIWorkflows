
def add(a, b):
    return a + b
 
 
def subtract(a, b):
    return a - b
 
 
def multiply(a, b):
    return a * b
 
 
def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b
 
 
def get_number(prompt):
    "Keeps asking until the user enters a valid number."
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
 
 
def main():
    print("=== Simple Calculator ===")
    print("Operations: + (add), - (subtract), * (multiply), / (divide)")
    print("Type 'q' at any time to quit.")
 
    while True:
        choice = input("Choose operation (+, -, *, /) or 'q' to quit: ").strip()

 
        if choice.lower() == "q":
            print("Goodbye!")
            break
 
        if choice not in ("+", "-", "*", "/"):
            print("Invalid operation. Please choose +, -, *, / or q.")
            continue
 
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")
 
        if choice == "+":
            result = add(num1, num2)
        elif choice == "-":
            result = subtract(num1, num2)
        elif choice == "*":
            result = multiply(num1, num2)
        else:
            result = divide(num1, num2)
 
        print(f"Result: {result}\n")
 
 
if __name__ == "__main__":
    main()