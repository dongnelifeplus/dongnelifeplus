from flask import Flask
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def home():

    area_name = "관양동"

    today = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    nx = 59
    ny = 123

    SERVICE_KEY = "3d3dabc9d1fd62b04feccda19172466f925c89aab1a5f815b952e649ec73a8df"

    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": "1",
        "numOfRows": "100",
        "dataType": "JSON",
        "base_date": today,
        "base_time": "0200",
        "nx": nx,
        "ny": ny
    }

    response = requests.get(url, params=params)
    data = response.json()

    items = data["response"]["body"]["items"]["item"]

    temp = "0"
    pop = "0"
    sky = "1"

    for item in items:

        if item["category"] == "TMP" and temp == "0":
            temp = item["fcstValue"]

        if item["category"] == "POP" and pop == "0":
            pop = item["fcstValue"]

        if item["category"] == "SKY" and sky == "1":
            sky = item["fcstValue"]

    if sky == "1":
        sky_text = "맑음"
    elif sky == "3":
        sky_text = "구름많음"
    else:
        sky_text = "흐림"

    opportunity_score = 100

    if int(pop) >= 60:
        opportunity_score -= 20

    if int(temp) <= 5:
        opportunity_score -= 15

    with open("benefits.json", "r", encoding="utf-8") as file:
        benefits = json.load(file)

    benefit_count = len(benefits)

    saving_amount = sum(
        item["saving"] for item in benefits
    )

    benefit_html = ""

    for item in benefits:
        benefit_html += f"""
        <div class="benefit-card">
            <h3>{item['title']}</h3>
            <p>예상 절감액 {item['saving']:,}원</p>
        </div>
        """

    return f"""
    <html>
    <head>
    <meta charset="utf-8">

    <style>

    body {{
        font-family: Arial;
        background:#f5f7fb;
        max-width:900px;
        margin:auto;
        padding:20px;
    }}

    .card {{
        background:white;
        padding:20px;
        margin-bottom:20px;
        border-radius:12px;
        box-shadow:0 2px 8px rgba(0,0,0,0.1);
    }}

    .score {{
        font-size:48px;
        color:#2563eb;
        font-weight:bold;
    }}

    .benefit-card {{
        background:white;
        border-radius:12px;
        padding:15px;
        margin-bottom:15px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
    }}

    </style>
    </head>

    <body>

    <h1>우리동네라이프플러스</h1>

    <div class="card">
        <h2>오늘의 날씨</h2>
        <p>지역 : {area_name}</p>
        <p>현재 기온 : {temp}도</p>
        <p>강수확률 : {pop}%</p>
        <p>하늘상태 : {sky_text}</p>
    </div>

    <div class="card">
        <h2>오늘의 기회 점수</h2>
        <div class="score">{opportunity_score}점</div>

        <p>발견된 혜택 : {benefit_count}건</p>
        <p>예상 절감액 : {saving_amount:,}원</p>
    </div>

    <div class="card">
        <h2>오늘 놓치면 안되는 정보</h2>
        {benefit_html}
    </div>

    <div class="card">
        <h2>AI 생활 추천</h2>
        <p>외출하기 좋은 날씨입니다.</p>
    </div>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
