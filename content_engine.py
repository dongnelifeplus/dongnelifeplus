import json

with open("real_benefits.json","r",encoding="utf-8") as f:
benefits=json.load(f)

posts=[]

for b in benefits:

```
posts.append({

    "title": b["title"],

    "news_content":
    f"{b['title']} 신청이 가능합니다. "
    f"예상 혜택 금액은 {b['saving']:,}원 입니다.",

})
```

with open("posts.json","w",encoding="utf-8") as f:
json.dump(posts,f,ensure_ascii=False,indent=2)

print("posts.json 생성 완료")
