import json

KEYWORDS = {
    "정책자금": 40,
    "창업": 35,
    "소상공인": 30,
    "청년": 20,
    "전기요금": 10,
    "통신비": 10
}

with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

for post in posts:
    score = 0

    text = (
        post.get("title","")
        + " "
        + post.get("content","")
    )

    for keyword, value in KEYWORDS.items():
        if keyword in text:
            score += value

    post["score"] = score

posts.sort(
    key=lambda x: x.get("score",0),
    reverse=True
)

with open(
    "posts_scored.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        posts,
        f,
        ensure_ascii=False,
        indent=2
    )

print("점수 계산 완료")