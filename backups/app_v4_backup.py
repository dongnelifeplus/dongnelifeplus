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


if __name__ == "__main__":
    app.run(debug=True)