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

    name = request.args.get("name", "")
    age = int(request.args.get("age", 30))
    area = request.args.get("area", "")
    car = request.args.get("car", "no")

    user = {
        "name": name,
        "age": age,
        "area": area,
        "car": car
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
        "message": "저장 완료",
        "user": user
    })


@app.route("/api/users")
def users():

    with open("users.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)


@app.route("/api/benefits")
def benefits():

    with open("real_benefits.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)


@app.route("/api/recommend")
def recommend():

    age = int(request.args.get("age", 30))
    area = request.args.get("area", "관양동")
    car = request.args.get("car", "no")

    with open("real_benefits.json", "r", encoding="utf-8") as f:
        benefits = json.load(f)

    result = []
    saving = 0

    for item in benefits:

        if item["area"] != area:
            continue

        if item["target"] == "전체":
            result.append(item)
            saving += item["saving"]

        elif item["target"] == "청년" and age <= 39:
            result.append(item)
            saving += item["saving"]

        elif item["target"] == "차량" and car == "yes":
            result.append(item)
            saving += item["saving"]

    score = min(100, int(saving / 2000))

    return jsonify({
        "score": score,
        "saving": saving,
        "count": len(result),
        "benefits": result
    })


@app.route("/api/dashboard")
def dashboard():

    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    if len(users) == 0:
        return jsonify({"message": "등록된 사용자가 없습니다."})

    user = users[-1]

    with open("real_benefits.json", "r", encoding="utf-8") as f:
        benefits = json.load(f)

    result = []
    saving = 0

    for item in benefits:

        if item["area"] != user["area"]:
            continue

        if item["target"] == "전체":
            result.append(item)
            saving += item["saving"]

        elif item["target"] == "청년" and user["age"] <= 39:
            result.append(item)
            saving += item["saving"]

        elif item["target"] == "차량" and user["car"] == "yes":
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