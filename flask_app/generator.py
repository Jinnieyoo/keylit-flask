# flask_app/generator.py
import pandas as pd
import json
import matplotlib.pyplot as plt
from analyzer import compute_tfidf_keywords
from wordcloud import WordCloud
from pathlib import Path

def save_keywords_as_json(df, output_path="output/top_keywords.json"):
    keywords = compute_tfidf_keywords(df)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)
    print(f"✅ 키워드 JSON 저장 완료: {output_path}")

def save_wordcloud_image(df, output_path="output/wordcloud.png"):
    keywords = compute_tfidf_keywords(df)
    wc = WordCloud(font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
                   background_color="white",
                   width=800, height=400)
    freq_dict = {k['word']: k['score'] for k in keywords}
    wc.generate_from_frequencies(freq_dict)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    wc.to_file(output_path)
    print(f"✅ 워드클라우드 이미지 저장 완료: {output_path}")

# 테스트용 실행 예시
if __name__ == "__main__":
    df = pd.read_csv("../data/your_tokens_data.csv")  # 'tokens_str' 열 포함
    save_keywords_as_json(df)
    save_wordcloud_image(df)
