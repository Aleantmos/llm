import re

import save_data


def extract_books(text, url):
    book_pattern = re.compile(r'"\s*(.*?)\s*"\s*by\s*(.*)')
    books = book_pattern.findall(text)

    for book in books:
        print(book)

    save_data.save_books(books, url)

