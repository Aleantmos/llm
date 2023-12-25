import requests
from bs4 import BeautifulSoup


def fetch_article_data():
    url = 'https://en.wikipedia.org/wiki/Belt_and_Road_Initiative'

    response = requests.get(url)
    webpage = response.text

    soup = BeautifulSoup(webpage, "html.parser")
    content = soup.find('div', class_="mw-parser-output")

    article_text = ""
    for paragraph in content.find_all('p', limit=5):
        article_text += paragraph.get_text() + "\n"

    return article_text
