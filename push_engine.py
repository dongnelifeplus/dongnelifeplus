import json
from datetime import datetime

with open(
    "recommendations.json",
    "r",
    encoding="utf-8"
) as f:

    recommendations = json.load(f)

messages = []

for item in recommendations:

    msg = {
        "name": item["subscriber_name"],
        "phone": item["subscriber_phone"],
        "title": item["title"],
        "score": item["score"],
        "message":
            f"[나만 모르는 숨은 돈]\n"
            f"{item['title']} 혜택이 확인되었습니다.\n"
            f"지금 확인해보세요.",
        "created":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
        "status": "waiting"
    }

    messages.append(msg)

with open(
    "push_queue.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        messages,
        f,
        ensure_ascii=False,
        indent=2
    )

print("발송대기 생성 완료")