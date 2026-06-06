from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "우리동네라이프플러스 정상동작"

if __name__ == "__main__":
    app.run(debug=True)