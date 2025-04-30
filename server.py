from flask import Flask
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

app = Flask(__name__)

@app.route('/api/news')
def crawl_and_translate_news():
    try:
#        url = "https://pokemongohub.net/post/category/news/"
        url = "https://poketory.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("h2.entry-title a")

        translator = GoogleTranslator(source='auto', target='ko')

        result = ""
        for item in items[:5]:  # 상위 5개 뉴스만
            title_en = item.get_text(strip=True)
            title_ko = translator.translate(title_en)
            link = item.get('href')
            result += f"<b>{title_ko}</b><br><a href='{link}'>{link}</a><br><br>"

        if not result:
            return "No news found.", 404

        return result

    except Exception as e:
        return f"An error occurred: {e}", 500
