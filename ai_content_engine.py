import json
import os
from datetime import datetime

POST_FILE = "posts.json"


def load_posts():
    if not os.path.exists(POST_FILE):
        return []

    with open(
        POST_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_posts(posts):
    with open(
        POST_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            posts,
            f,
            ensure_ascii=False,
            indent=2
        )


def create_post(
    title,
    category,
    content
):

    posts = load_posts()

    post = {
        "id": len(posts) + 1,
        "title": title,
        "category": category,
        "content": content,
        "created": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
    }

    posts.insert(
        0,
        post
    )

    save_posts(posts)

    print("콘텐츠 생성 완료")


if __name__ == "__main__":

    create_post(
        "2026 청년 월세지원 총정리",
        "청년",
        """
월 최대 20만원 지원

신청 대상

만 19~39세

무주택 청년

신청기간 확인 필요
        """
    )