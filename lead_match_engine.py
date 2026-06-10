import json

# 구독자
with open("subscribers.json", "r", encoding="utf-8") as f:
    subscribers = json.load(f)

# 점수 계산 완료된 포스트
with open("posts_scored.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

matches = []

for post in posts:
    for sub in subscribers:
        # 구독자 관심사와 포스트 카테고리 매칭
        if any(cat in post.get("category","") for cat in sub.get("interest",[])):
            matches.append({
                "title": post["title"],
                "subscriber_name": sub["name"],
                "subscriber_phone": sub["phone"],
                "category": post.get("category",""),
                "score": post.get("score",0)
            })

# 결과 저장
with open("recommendations.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, ensure_ascii=False, indent=2)

print("추천 대상 생성 완료")