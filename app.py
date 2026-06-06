from flask import Flask, jsonify, send_file
import json

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/api/benefits")
def benefits():

    with open("benefits.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

@app.route("/api/score")
def score():

    with open("benefits.json", "r", encoding="utf-8") as f:
        benefits = json.load(f)

    total = sum(item["saving"] for item in benefits)

    score = min(100, int(total / 1000))

    return jsonify({
        "score": score,
        "saving": total,
        "count": len(benefits)
    })

@app.route("/api/recommendation")
def recommendation():

    with open("benefits.json", "r", encoding="utf-8") as f:
        benefits = json.load(f)

    total = sum(item["saving"] for item in benefits)

    if total >= 100000:
        message = f"현재 발견된 혜택을 활용하면 최대 {total:,}원 절약 가능합니다."
    else:
        message = f"추가 혜택 탐색을 추천합니다. 현재 예상 절감액 {total:,}원"

    return jsonify({
        "message": message
    })

if __name__ == "__main__":
    app.run(debug=True)