import requests
from bs4 import BeautifulSoup

import save_data


def fetch_article_data(url):
    response = requests.get(url)
    webpage = response.text

    soup = BeautifulSoup(webpage, "html.parser")
    title = soup.find('div', class_='mw-body-header')
    content = soup.find('div', class_="mw-parser-output")

    article_text = ""
    for paragraph in content.find_all('p', limit=5):
        article_text += paragraph.get_text() + "\n"

    save_data.save_article_data(title, url)

    return article_text
