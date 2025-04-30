from flask import Flask, request, jsonify

app = Flask(__name__)
cached_news = []

@app.route("/api/upload", methods=["POST"])
def upload_news():
    global cached_news
    cached_news = request.json
    return {"message": "뉴스 업로드 완료"}, 200

@app.route("/api/news", methods=["GET"])
def get_news():
    return jsonify(cached_news if cached_news else {"message": "아직 뉴스 없음"}), 200

@app.route("/")
def home():
    return "포켓몬고 뉴스 서버 정상 작동 중!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
