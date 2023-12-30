from flask import Flask, render_template, request

import data_extractor
import fetch_article
import get_summary
import save_data

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('templates/index.html')




@app.route('/process', methods=['Post'])
def process():
    url = request.form['url']
    article_text = fetch_article.fetch_article_data(url)
    response = get_summary.get_bullet_points(article_text, url)
    data_extractor.extract_books(response, url)

    print("Books have been saved to CSV and database.")


if __name__ == '__main__':
    app.run(debug=True)
