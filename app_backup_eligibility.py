from flask import Flask, jsonify, send_file, request
import json
import os

app = Flask(__name__)
app.json.ensure_ascii = False

# -----------------------------
# 메인 페이지
# -----------------------------
@app.route("/")
def home():
    return send_file("index.html")

# -----------------------------
# 사용자 등록
# -----------------------------
@app.route("/api/register")
def register():
    user = {
        "name": request.args.get("name", ""),
        "age": int(request.args.get("age", 30)),
        "gender": request.args.get("gender", ""),
        "area": request.args.get("area", ""),
        "family": request.args.get("family", ""),
        "income": request.args.get("income", ""),
        "job": request.args.get("job", ""),
        "house": request.args.get("house", ""),
        "business": request.args.get("business", ""),
        "marriage": request.args.get("marriage", ""),
        "children": request.args.get("children", ""),
        "car": request.args.get("car", "no")
    }
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    else:
        users = []
    users.append(user)
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    return jsonify({"message":"등록 완료","user":user})

# -----------------------------
# 사용자 목록
# -----------------------------
@app.route("/api/users")
def users():
    if not os.path.exists("users.json"):
        return jsonify([])
    with open("users.json","r",encoding="utf-8") as f:
        return jsonify(json.load(f))

# -----------------------------
# 혜택 목록
# -----------------------------
@app.route("/api/benefits")
def benefits():
    with open("real_benefits.json","r",encoding="utf-8") as f:
        return jsonify(json.load(f))

# -----------------------------
# 대시보드 (마지막 등록자 기준)
# -----------------------------
@app.route("/api/dashboard")
def dashboard_api():
    import os
    import json
    from flask import jsonify

    # 사용자 정보 읽기
    if not os.path.exists("users.json"):
        return jsonify({"message":"사용자 정보 없음"})

    with open("users.json","r",encoding="utf-8") as f:
        users=json.load(f)

    if not users:
        return jsonify({"message":"사용자 정보 없음"})

    user=users[-1]

    # 혜택 데이터 읽기
    if not os.path.exists("real_benefits.json"):
        return jsonify({"message":"혜택 데이터 없음"})

    with open("real_benefits.json","r",encoding="utf-8") as f:
        benefits=json.load(f)

    matched=[]
    hidden=[]

    total_support=0
    hidden_support=0

    for item in benefits:
        fit=0

        if item["area"]=="안양시":
            fit+=30

        if item["target"]=="전체":
            fit+=40
        elif item["target"]=="청년":
            if user["age"]<=39:
                fit+=40
        elif item["target"]=="사업자":
            if user.get("business"):
                fit+=40

        fit=min(fit,100)

        benefit_data={
            "title":item["title"],
            "fit":fit,
            "saving":item["saving"],
            "reason":item["reason"],
            "link":item["link"]
        }

        if fit>=60:
            matched.append(benefit_data)
            total_support+=item["saving"]
        else:
            hidden.append(benefit_data)
            hidden_support+=item["saving"]

    # 프로필 정보완성도 계산
    fields=[
        "gender",
        "family",
        "income",
        "job",
        "house",
        "business",
        "marriage",
        "children",
        "interest",
        "lifestyle",
        "location_agree"
    ]

    completed=0
    for field in fields:
        value=user.get(field)
        if value not in ["",[],None,"N"]:
            completed+=1

    profile_score=int((completed/len(fields))*100)

    # 최종 JSON 반환
    return jsonify({
        "name":user["name"],
        "area":user["area"],
        "profile_score":profile_score,
        "benefit_count":len(matched),
        "hidden_count":len(hidden),
        "saving":total_support,
        "hidden_saving":hidden_support,
        "benefits":matched,
        "hidden_benefits":hidden[:3]
    })

# -----------------------------
# 관리자 페이지
# -----------------------------
@app.route("/admin")
def admin():
    return send_file("admin.html")

# -----------------------------
# 혜택 등록
# -----------------------------
@app.route("/api/add-benefit",methods=["POST"])
def add_benefit():
    new_item=request.json
    if os.path.exists("real_benefits.json"):
        with open("real_benefits.json","r",encoding="utf-8") as f:
            data=json.load(f)
    else:
        data=[]
    data.append(new_item)
    with open("real_benefits.json","w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
    return jsonify({"message":"saved"})

# -----------------------------
# 상담 저장
# -----------------------------
@app.route("/api/leads",methods=["POST"])
def save_lead():
    lead=request.json
    leads=[]
    if os.path.exists("leads.json"):
        with open("leads.json","r",encoding="utf-8") as f:
            leads=json.load(f)
    leads.append(lead)
    with open("leads.json","w",encoding="utf-8") as f:
        json.dump(leads,f,ensure_ascii=False,indent=2)
    return jsonify({"message":"saved"})

# -----------------------------
# 상담 목록 조회
# -----------------------------
@app.route("/api/get-leads")
def get_leads():
    if not os.path.exists("leads.json"):
        return jsonify([])
    with open("leads.json","r",encoding="utf-8") as f:
        return jsonify(json.load(f))

# -----------------------------
# 예상 매출 계산
# -----------------------------
@app.route("/api/revenue")
def revenue():
    if not os.path.exists("leads.json") or not os.path.exists("partners.json"):
        return jsonify({"count":0,"revenue":0,"data":[]})
    with open("leads.json","r",encoding="utf-8") as f:
        leads=json.load(f)
    with open("partners.json","r",encoding="utf-8") as f:
        partners=json.load(f)
    total_revenue=0
    data=[]
    for lead in leads:
        lead_revenue=0
        for p in partners:
            if p["type"]==lead["type"]:
                lead_revenue+=p["price"]
        total_revenue+=lead_revenue
        data.append({
            "name":lead["name"],
            "type":lead["type"],
            "company":next((p["company"] for p in partners if p["type"]==lead["type"]),""),
            "revenue":lead_revenue
        })
    return jsonify({"count":len(leads),"revenue":total_revenue,"data":data})

# -----------------------------
# 광고 조회
# -----------------------------
@app.route("/api/ads")
def get_ads():
    area = request.args.get("area", "")
    if not os.path.exists("ads.json"):
        return jsonify([])
    with open("ads.json", "r", encoding="utf-8") as f:
        ads = json.load(f)
    filtered_ads = [ad for ad in ads if ad["area"] == area]
    return jsonify(filtered_ads)

# -----------------------------
# 구독자 저장
# -----------------------------
@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    subscribers = request.json
    with open("subscribers.json", "w", encoding="utf-8") as f:
        json.dump(subscribers, f, ensure_ascii=False, indent=2)
    return jsonify({"message": "saved"})

# -----------------------------
# posts.json 제공
# -----------------------------

@app.route("/posts.json")
def posts():
    return send_file("posts.json")

@app.route("/api/favorite", methods=["POST"])
def favorite():
    data = request.json

    if os.path.exists("favorites.json"):
        with open("favorites.json", "r", encoding="utf-8") as f:
            favorites = json.load(f)
    else:
        favorites = []

    favorites.append(data)

    with open("favorites.json", "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "saved"})


@app.route("/api/plan", methods=["POST"])
def plan():
    data = request.json

    if os.path.exists("plans.json"):
        with open("plans.json", "r", encoding="utf-8") as f:
            plans = json.load(f)
    else:
        plans = []

    plans.append(data)

    with open("plans.json", "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "saved"})


@app.route("/api/alert", methods=["POST"])
def alert():
    data = request.json

    if os.path.exists("alerts.json"):
        with open("alerts.json", "r", encoding="utf-8") as f:
            alerts = json.load(f)
    else:
        alerts = []

    alerts.append(data)

    with open("alerts.json", "w", encoding="utf-8") as f:
        json.dump(alerts, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "saved"})

# -----------------------------
# 뉴스 페이지
# -----------------------------
@app.route("/news")
def news():
    return send_file("news.html")


# -----------------------------
# 대시보드 페이지
# -----------------------------
@app.route("/dashboard")
def dashboard():
    return send_file("dashboard.html")

@app.route("/calendar")
def calendar():
    return send_file("calendar.html")

# -----------------------------
# 실행
# -----------------------------

@app.route("/api/beta-stats")
def beta_stats():

    if not os.path.exists("beta_stats.json"):
        return jsonify({})

    with open("beta_stats.json","r",encoding="utf-8") as f:
        data=json.load(f)

    return jsonify(data)

@app.route("/api/log-click", methods=["POST"])
def log_click():

    data = request.json

    logs = []

    if os.path.exists("user_logs.json"):
        with open("user_logs.json","r",encoding="utf-8") as f:
            logs = json.load(f)

    logs.append(data)

    with open("user_logs.json","w",encoding="utf-8") as f:
        json.dump(logs,f,ensure_ascii=False,indent=2)

    return jsonify({"message":"saved"})

@app.route("/api/log-stats")
def log_stats():

    if not os.path.exists("user_logs.json"):
        return jsonify([])

    with open("user_logs.json","r",encoding="utf-8") as f:
        logs = json.load(f)

    stats = {}

    for item in logs:

        benefit = item.get("benefit","기타")

        stats[benefit] = stats.get(benefit,0) + 1

    result = []

    for name,count in stats.items():

        result.append({
            "benefit":name,
            "count":count
        })

    result.sort(key=lambda x:x["count"], reverse=True)

    return jsonify(result)

@app.route("/api/favorite", methods=["POST"])
def save_favorite():

    data = request.json

    favorites = []

    if os.path.exists("favorites.json"):
        with open("favorites.json","r",encoding="utf-8") as f:
            favorites = json.load(f)

    favorites.append(data)

    with open("favorites.json","w",encoding="utf-8") as f:
        json.dump(favorites,f,ensure_ascii=False,indent=2)

    return jsonify({
        "result":"ok"
})

@app.route("/api/calendar")
def get_calendar():

    if not os.path.exists("calendar_events.json"):
        return jsonify([])

    with open(
        "calendar_events.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return jsonify(data)

@app.route("/api/master-benefits")
def master_benefits():

    if not os.path.exists("benefit_master.json"):
        return jsonify([])

    with open(
        "benefit_master.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return jsonify(data)

@app.route("/api/stats")
def stats():

    if not os.path.exists(
        "benefit_master.json"
    ):
        return jsonify({})

    with open(
        "benefit_master.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    total_count = len(data)

    total_amount = sum(
        item.get("amount",0)
        for item in data
    )

    return jsonify({
        "benefit_count": total_count,
        "total_amount": total_amount
    })


if __name__ == "__main__":
    app.run(debug=True)