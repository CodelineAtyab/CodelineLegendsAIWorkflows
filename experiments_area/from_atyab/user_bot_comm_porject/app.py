import utils
# from utils import multiply as mul

def main():
    list_of_even_numbers = tuple([num for num in range(1000 + 1)])
    list_of_even_numbers = []

    # Initialize the list with ODD numbers upto 1000
    for num in range(1000 + 1):
        list_of_even_numbers.append(None)

    print(list_of_even_numbers)

if __name__ == "__main__":
    main()