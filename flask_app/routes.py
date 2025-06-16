from flask import Flask, jsonify, request
from analyzer import compute_tfidf_keywords
import pandas as pd

app = Flask(__name__)

@app.route("/")
def hello():
    return "Keylit Flask 서버 실행 중!"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    df = pd.DataFrame(data)
    keywords = compute_tfidf_keywords(df)
    return jsonify(keywords)

if __name__ == "__main__":
    app.run(debug=True)
