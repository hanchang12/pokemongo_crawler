from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/news')
def crawl_news():
    try:
        url = "https://pokemongo.com/news?hl=ko"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div.NewsList-content-block a")

        result = ""
        for item in items[:5]:  # 상위 5개 뉴스만 출력
            title = item.get_text(strip=True)
            link = item.get('href')
            if link and not link.startswith("http"):
                link = "https://pokemongo.com" + link
            result += f"<b>{title}</b><br><a href='{link}'>{link}</a><br><br>"

        if not result:
            return "No news found.", 404

        return result

    except Exception as e:
        return f"An error occurred: {e}", 500

# (Flask 애플리케이션 엔트리포인트는 gunicorn이 자동으로 실행해줌)
