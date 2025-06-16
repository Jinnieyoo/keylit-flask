# ✅ keylit-flask/app.py
from flask import Flask, jsonify, request, send_file, render_template
import pandas as pd
import json
import io
import matplotlib.pyplot as plt

app = Flask(__name__)

# 파일 경로 설정
PROCESSED_CSV = "cache/processed_data_with_lda.csv"
TOPIC_KEYWORDS_JSON = "cache/topic_keywords.json"
TFIDF_KEYWORDS_JSON = "cache/top_keywords.json"
LDA_CHART_PNG = "cache/lda_topics.png"

df = pd.read_csv(PROCESSED_CSV)
with open(TOPIC_KEYWORDS_JSON, encoding="utf-8") as f:
    topic_keywords = json.load(f)
with open(TFIDF_KEYWORDS_JSON, encoding="utf-8") as f:
    tfidf_keywords = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lda_topics")
def lda_topics():
    return jsonify(topic_keywords)

@app.route("/lda_chart")
def lda_chart():
    return send_file(LDA_CHART_PNG, mimetype='image/png')

@app.route("/tfidf_keywords")
def tfidf_keywords_api():
    return jsonify(tfidf_keywords)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    results = df[df['tokens_str'].str.contains(query)].head(10)
    papers = []
    for _, row in results.iterrows():
        papers.append({
            "title": row.get("title", "제목 없음"),
            "author": row.get("author", "저자 없음"),
            "abstract": row.get("abstract", "초록 없음"),
            "link": "#",
            "topic": f"Topic {int(row['lda_topic'])+1}"
        })
    return jsonify(papers)

if __name__ == '__main__':
    app.run(debug=True)
