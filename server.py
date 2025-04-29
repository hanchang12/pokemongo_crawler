from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/news')
def crawl_news():
    try:
        url = "https://pokemongolive.com/news"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("section.NewsList__Grid-sc-1cm8g4x-2 article a")

        result = ""
        base_url = "https://pokemongolive.com"

        for item in items[:5]:  # 상위 5개 뉴스만 출력
            title = item.get_text(strip=True)
            link = item.get('href')
            if link and not link.startswith("http"):
                link = base_url + link
            result += f"<b>{title}</b><br><a href='{link}'>{link}</a><br><br>"

        if not result:
            return "No news found.", 404

        return result

    except Exception as e:
        return f"An error occurred: {e}", 500
