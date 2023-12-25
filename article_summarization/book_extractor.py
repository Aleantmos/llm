import re


def extract_books(text):
    book_pattern = re.compile(r'"\s*(.*?)\s*"\s*by\s*(.*)')
    books = book_pattern.findall(text)

    for book in books:
        print(book)
    return books
