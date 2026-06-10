from flask import Flask, jsonify, send_file
import json
import requests
from datetime import datetime

app = Flask(__name__)
app.json.ensure_ascii = False

SERVICE_KEY = "3d3dabc9d1fd62b04feccda19172466f925c89aab1a5f815b952e649ec73a8df"

@app.route("/")
def home():
return send_file("index.html")

@app.route("/api/benefits")
def benefits():

```
with open("benefits.json", "r", encoding="utf-8") as f:
    data = json.load(f)

return jsonify(data)
```

@app.route("/api/score")
def score():

```
with open("benefits.json", "r", encoding="utf-8") as f:
    benefits = json.load(f)

total = sum(item["saving"] for item in benefits)

score = min(100, int(total / 1000))

return jsonify({
    "score": score,
    "saving": total,
    "count": len(benefits)
})
```

@app.route("/api/recommendation")
def recommendation():

```
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
```

@app.route("/api/weather")
def weather():

```
today = datetime.now().strftime("%Y%m%d")

url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

params = {
    "serviceKey": SERVICE_KEY,
    "pageNo": "1",
    "numOfRows": "100",
    "dataType": "JSON",
    "base_date": today,
    "base_time": "0500",
    "nx": "59",
    "ny": "123"
}

response = requests.get(url, params=params)
data = response.json()

items = data["response"]["body"]["items"]["item"]

temp = ""
pop = ""
sky = ""

for item in items:

    if item["category"] == "TMP" and temp == "":
        temp = item["fcstValue"]

    if item["category"] == "POP" and pop == "":
        pop = item["fcstValue"]

    if item["category"] == "SKY" and sky == "":
        sky = item["fcstValue"]

sky_text = {
    "1": "맑음",
    "3": "구름많음",
    "4": "흐림"
}.get(sky, "정보없음")

return jsonify({
    "location": "관양동",
    "temp": temp,
    "pop": pop,
    "sky": sky_text
})
```

if __name__ == "__main__":
app.run(debug=True)
