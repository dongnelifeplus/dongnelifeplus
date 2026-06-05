import requests
from datetime import datetime
import os

SERVICE_KEY = "3d3dabc9d1fd62b04feccda19172466f925c89aab1a5f815b952e649ec73a8df"

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

print("상태코드:", response.status_code)
print(response.text)

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

print("===== 우리동네라이프플러스 =====")
print("현재 기온:", temp, "도")
print("강수확률:", pop, "%")
print("하늘상태:", sky_text)

if int(pop) >= 60:
    print("한줄요약: 우산을 챙기는 것이 좋겠습니다.")
else:
    print("한줄요약: 외출하기 무난한 날씨입니다.")
    html = f"""
<html>
<head>
    <meta charset="utf-8">
    <title>우리동네라이프플러스</title>
</head>

<body>

<h1>우리동네라이프플러스</h1>

<h2>오늘의 날씨</h2>

<p>현재 기온 : {temp}도</p>
<p>강수확률 : {pop}%</p>
<p>하늘상태 : {sky_text}</p>

<hr>

<h2>AI 생활 추천</h2>

<p>
{"우산을 챙기는 것이 좋겠습니다." if int(pop) >= 60 else "외출하기 무난한 날씨입니다."}
</p>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html)

os.system("git add .")
os.system('git commit -m "자동 날씨 업데이트"')
os.system("git push")

print("GitHub 자동 업로드 완료")