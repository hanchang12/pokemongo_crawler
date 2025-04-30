from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)
CACHE_FILE = "cached_news.json"

# 현재 커스텀 네우스 저장된 데이터를 로드해서 설정함
def load_cached_news():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding='utf-8') as f:
            return json.load(f)
    return []

# 저장 후 파일에 기록
def save_cached_news(news):
    with open(CACHE_FILE, "w", encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)

# 복잡되지 않도록 처리한 네우스 데이터
deduplicated_news = {n['link']: n for n in load_cached_news()}

@app.route("/api/upload", methods=["POST"])
def upload_news():
    global deduplicated_news
    uploaded = request.json
    for news in uploaded:
        deduplicated_news[news['link']] = news
    save_cached_news(list(deduplicated_news.values()))
    return {"message": "뉴스 업로드 완료"}, 200

@app.route("/api/news", methods=["GET"])
def get_news():
    news = list(deduplicated_news.values())
    return jsonify(news if news else {"message": "아직 데이터 없음"}), 200

@app.route("/api/news/<string:date>", methods=["GET"])
def get_news_by_date(date):
    try:
        # 날짜는 YYYY.MM.DD 형식으로 추종할 것이다
        filtered = [n for n in deduplicated_news.values() if date in n['date']]
        return jsonify(filtered if filtered else {"message": "이름의 뉴스 없음"}), 200
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/", methods=["GET"])
def render_news():
    news = list(deduplicated_news.values())
    html_template = """
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><title>포켐몬고 뉴스</title></head>
    <body>
      <h1>포켐몬고 뉴스</h1>
      {% if news %}
        <ul>
        {% for item in news %}
          <li><strong>{{ item.date }}</strong> - <a href="{{ item.link }}" target="_blank">{{ item.title }}</a></li>
        {% endfor %}
        </ul>
      {% else %}
        <p>뉴스 데이터가 없습니다.</p>
      {% endif %}
    </body>
    </html>
    """
    return render_template_string(html_template, news=news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
