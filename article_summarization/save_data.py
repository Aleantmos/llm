import sqlite3


def save_books_to_db(books, db_name="books.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("create table if not exists books (title text, author text)")

    cursor.executemany("insert into books (author, title) values (?, ?)", books)
    connection.commit()
    connection.close()
