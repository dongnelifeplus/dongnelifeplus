from flask import Flask, jsonify, send_file, request
import json
import os

app = Flask(__name__)
app.json.ensure_ascii = False


@app.route("/")
def home():
    return send_file("index.html")


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

    return jsonify({
        "message": "등록 완료",
        "user": user
    })


@app.route("/api/users")
def users():

    if not os.path.exists("users.json"):
        return jsonify([])

    with open("users.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)


@app.route("/api/benefits")
def benefits():

    with open("real_benefits.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)


@app.route("/api/dashboard")
def dashboard():

    if not os.path.exists("users.json"):
        return jsonify({"message": "등록된 사용자가 없습니다."})

    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    user = users[-1]

    with open("real_benefits.json", "r", encoding="utf-8") as f:
        benefits = json.load(f)

    result = []
    saving = 0

    for item in benefits:

        if item["area"] != user["area"]:
            continue

        target = item["target"]

        if target == "전체":
            result.append(item)
            saving += item["saving"]

        elif target == "청년" and user["age"] <= 39:
            result.append(item)
            saving += item["saving"]

        elif target == "차량" and user["car"] == "yes":
            result.append(item)
            saving += item["saving"]

    score = min(100, int(saving / 2000))

    return jsonify({
        "name": user["name"],
        "area": user["area"],
        "score": score,
        "saving": saving,
        "count": len(result),
        "benefits": result
    })


if __name__ == "__main__":
    app.run(debug=True)