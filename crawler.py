import json
from datetime import datetime

sample_data = [
    {
        "title": "청년 월세지원",
        "content": "월 최대 20만원 지원"
    },
    {
        "title": "소상공인 정책자금",
        "content": "최대 7000만원 지원"
    }
]

posts = []

for item in sample_data:

    posts.append({
        "id": len(posts) + 1,
        "title": item["title"],
        "category": "자동수집",
        "content": item["content"],
        "created": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
    })

with open(
    "posts.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        posts,
        f,
        ensure_ascii=False,
        indent=2
    )

print("자동 수집 완료")