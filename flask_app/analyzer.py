from sklearn.feature_extraction.text import TfidfVectorizer

def compute_tfidf_keywords(df):
    docs = df['tokens_str'].fillna("").tolist()
    vectorizer = TfidfVectorizer(max_df=0.9, min_df=2)
    X = vectorizer.fit_transform(docs)
    scores = X.mean(axis=0).A1
    words = vectorizer.get_feature_names_out()
    tfidf_dict = dict(zip(words, scores))
    top_keywords = sorted(tfidf_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    return [{"word": w, "score": float(s)} for w, s in top_keywords]
