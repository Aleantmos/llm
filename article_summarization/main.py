import book_extractor
import fetch_article
import get_summary
import save_data


def main():
    article_text = fetch_article.fetch_article_data()
    response = get_summary.get_bullet_points(article_text)

    books = book_extractor.extract_books(response)
    save_data.save_books_to_db(books)

    print("Books have been saved to CSV and database.")

if __name__ == '__main__':
    main()
