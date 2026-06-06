import json

import requests
from datetime import datetime

SERVICE_KEY = "3d3dabc9d1fd62b04feccda19172466f925c89aab1a5f815b952e649ec73a8df"

from datetime import datetime, timedelta

today = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

AREA_NAME = input("지역명을 입력하세요: ")

with open("areas.json", "r", encoding="utf-8") as file:
    AREAS = json.load(file)

url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

if AREA_NAME not in AREAS:
    print("지원하지 않는 지역입니다.")
    exit()
    
nx = AREAS[AREA_NAME]["nx"]
ny = AREAS[AREA_NAME]["ny"]

params = {
    "serviceKey": SERVICE_KEY,
    "pageNo": "1",
    "numOfRows": "100",
    "dataType": "JSON",
    "base_date": today,
    "base_time": "0230",
    "nx": nx,
    "ny": ny
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("API 오류")
    exit()
    
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

if sky == "1":
    sky_text = "맑음"
elif sky == "3":
    sky_text = "구름많음"
elif sky == "4":
    sky_text = "흐림"
else:
    sky_text = "정보없음"

opportunity_score = 100

if int(pop) >= 60:
    opportunity_score -= 20

if sky == "4":
    opportunity_score -= 10

if int(temp) < 5:
    opportunity_score -= 15

benefit_count = 3
saving_amount = 74000
benefits = []

if int(pop) >= 60:
    benefits.append({
        "title": "우산 할인 쿠폰",
        "saving": 5000
    })

if int(temp) >= 25:
    benefits.append({
        "title": "여름 전기요금 지원",
        "saving": 30000
    })

if int(temp) <= 10:
    benefits.append({
        "title": "난방비 지원사업",
        "saving": 50000
    })

benefit_count = len(benefits)

saving_amount = sum(
    item["saving"] for item in benefits
)

benefit_html = ""

for item in benefits:
    benefit_html += f"""
    <div style="border:1px solid #ddd;padding:10px;margin:10px;">
        <h3>{item['title']}</h3>
        <p>예상 절감액 {item['saving']:,}원</p>
    </div>
    """

html = f"""

<html>
<head>
<meta charset="utf-8">
<title>우리동네라이프플러스</title>

<style>

body{{
    font-family: Arial;
    max-width:900px;
}}

.card{{
    background:white;
}}

.score{{
    font-size:40px;
}}

</style>

</head>

<body>

<h1>우리동네라이프플러스</h1>

<h2>오늘의 날씨</h2>

<p>지역 : {AREA_NAME}</p>
<p>현재 기온 : {temp}도</p>
<p>강수확률 : {pop}%</p>
<p>하늘상태 : {sky_text}</p>

<hr>

<div class="card">

<h2>오늘의 기회 점수</h2>

<div class="score">
{opportunity_score}점
</div>

<p>발견된 혜택 : {benefit_count}건</p>

<p>예상 절감액 : {saving_amount:,}원</p>

</div>

<hr>

<h2>오늘 놓치면 안되는 정보</h2>

{benefit_html}

<hr>

<h2>AI 생활 추천</h2>

<p>
{"우산을 챙기세요." if int(pop) >= 60 else "외출하기 좋은 날씨입니다."}
</p>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html)

print("index.html 생성 완료")