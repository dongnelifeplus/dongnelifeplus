import requests

SERVICE_KEY = "3d3dabc9d1fd62b04feccda19172466f925c89aab1a5f815b952e649ec73a8df"

url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

params = {
    "serviceKey": SERVICE_KEY,
    "pageNo": "1",
    "numOfRows": "100",
    "dataType": "JSON",
    "base_date": "20260605",
    "base_time": "0500",
    "nx": "59",
    "ny": "123"
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.text)

data = response.json()

items = data["response"]["body"]["items"]["item"]

for item in items:
    if item["category"] == "TMP":
        print("현재 기온:", item["fcstValue"], "도")
        break