import os

import psycopg2


def get_connection():
    db_username = os.environ.get('DB_USERNAME')
    db_password = os.environ.get('DB_PASSWORD')

    connection = psycopg2.connect(
        dbname="article_summary",
        user=db_username,
        password=db_password,
        host='localhost'
    )

    return connection


def save_article_data(title, url):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        insert_query = "insert into articles (url, title) values (%s %s)"
        cursor.execute(insert_query, (url, title))

        connection.commit()

        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


def save_bullet_points(bullet_points, url):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        article_id = get_article_id_by_url(connection, url)

        if article_id:
            for point in bullet_points:
                insert_query = "insert into bullet_points (article_id, content) values (%s, %s)"
                cursor.execute(insert_query, (article_id, point))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


def get_article_id_by_url(url, cursor):
    try:
        cursor.execute("select id from article where url = %s", (url,))

        article_id = cursor.fetchone()[0]
        return article_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_book_id_by_title(cursor, book):
    try:
        cursor.execute("select id from books where title = %s", (book,))

        books_id = cursor.fetchone()[0]
        return books_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def save_books(books, url):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        article_id = get_article_id_by_url(connection, url)

        if article_id is None:
            raise Exception("No article with id=" + str(article_id))

        for book in books:
            book_id = get_book_id_by_title(cursor, book)
            if book_id is None:
                cursor.execute("insert into books (title) values (%s)", (book,))
                book_id = get_book_id_by_title(cursor, book)

            cursor.execute("insert into articles_books (article_id, book_id) values (%s, %s)", (article_id, book_id))

        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        connection.close()
