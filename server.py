from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/news')
def crawl_news():
    url = "https://pokemongo.com/news?hl=ko"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("div.NewsList-content-block a")

    result = ""
    for item in items[:5]:  # 상위 5개만
        title = item.get_text(strip=True)
        link = item.get('href')
        if not link.startswith("http"):
            link = "https://pokemongo.com" + link
        result += f"<b>{title}</b><br><a href='{link}'>{link}</a><br><br>"

    return result
