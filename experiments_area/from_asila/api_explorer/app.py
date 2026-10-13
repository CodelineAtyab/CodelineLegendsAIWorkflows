import requests # to use requests library to can communicate with Apis


# send a GET request to the API
def get_books(book_title):
    response = requests.get(
        "https://openlibrary.org/search.json",
        params={
            "q": book_title,
            "fields": "title,author_name",
            "limit": 5 #return up five matching books.
        }
    )
    
    data = response.json()  # to convert JSON response into a Python dictionary
    return data

#to display the result
def display_result(data):
    for book in data.get("docs", []):
        print("Title:", book.get("title"))
        print("Author:", book.get("author_name"))
        print()


def main(): #to start the program and run all the functions in order.
    book_title = input("Enter a book title: ")

    books = get_books(book_title)
    display_result(books)


if __name__ == "__main__":
    main()
    
    
# I chose the Open Library API to search for books.
# I chose it because the user can enter a title and get matching books.