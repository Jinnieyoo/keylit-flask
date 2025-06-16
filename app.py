import streamlit as st
import pandas as pd
import requests
from xml.etree import ElementTree
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Keylit - KCI 논문 검색", layout="centered")

st.title("\U0001F4DA Keylit - KCI 논문 검색")

# --- 사이드바 ---
with st.sidebar:
    st.header("\U0001F4C2 메뉴")
    if st.button("홈"):
        st.experimental_rerun()
    if st.button("즐겨찾기 보기"):
        st.session_state["mode"] = "favorites"
    if st.button("최근 검색 보기"):
        st.session_state["mode"] = "recent"

# --- 상태 초기화 ---
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "recent" not in st.session_state:
    st.session_state.recent = []
if "mode" not in st.session_state:
    st.session_state.mode = "search"

# --- 추천 키워드 ---
st.markdown("추천 키워드: ")
cols = st.columns(5)
keywords = ["딥러닝", "자연어처리", "강화학습", "데이터마이닝", "AI"]
for i, word in enumerate(keywords):
    if cols[i].button(word):
        st.session_state.current_query = word
        st.session_state.mode = "search"

# --- 검색 입력 ---
query = st.text_input("\U0001F50D 키워드 또는 논문 제목을 입력하세요", "")
if st.button("검색"):
    if query.strip():
        st.session_state.recent.insert(0, query)
        st.session_state.recent = st.session_state.recent[:10]
        st.session_state.mode = "search"
        st.session_state["current_query"] = query
    else:
        st.warning("검색어를 입력해주세요.")

# --- 검색 결과 or 즐겨찾기/최근 ---
if st.session_state.mode == "search" and "current_query" in st.session_state:
    query = st.session_state["current_query"]
    st.subheader(f"\U0001F50D '{query}' 검색 결과")
    url = f"https://api.kci.go.kr/openapi/service/rest/ArticleInfoService/getArticleList"
    params = {
        "ServiceKey": "27502279",  # 인증키
        "searchKeyword": query,
        "numOfRows": 10,
        "pageNo": 1
    }
    try:
        r = requests.get(url, params=params)
        xml = ElementTree.fromstring(r.content)
        items = xml.findall(".//item")

        for item in items:
            title = item.findtext("title", "제목 없음")
            author = item.findtext("author", "저자 없음")
            abstract = item.findtext("abstract", "초록 없음")
            link = item.findtext("link", "#")

            st.markdown(f"### {title}")
            st.markdown(f"**저자**: {author}  \n**초록**: {abstract}  \n[논문 링크]({link})")
            if st.button(f"⭐ 즐겨찾기 추가", key=title):
                st.session_state.favorites.append({"title": title, "link": link})
                st.success("즐겨찾기에 추가됨!")

    except Exception as e:
        st.error("API 요청 실패 또는 파싱 오류")
        st.exception(e)

elif st.session_state.mode == "favorites":
    st.subheader("⭐ 즐겨찾기 목록")
    if not st.session_state.favorites:
        st.info("즐겨찾기가 비어 있습니다.")
    for f in st.session_state.favorites:
        st.markdown(f"- [{f['title']}]({f['link']})")

elif st.session_state.mode == "recent":
    st.subheader("\U0001F552 최근 검색어")
    for q in st.session_state.recent:
        st.markdown(f"- {q}")

# --- Google Drive 대용량 예시 불러오기 (CSV/PNG/Feather 등) ---
st.divider()
st.subheader("\U0001F4C2 추가 분석 자료 예시")

# CSV (from Google Drive)
csv_id = "CSV_FILE_ID_HERE"  # 공유 링크에서 추출한 ID
csv_url = f"https://drive.google.com/uc?id={csv_id}"
try:
    df = pd.read_csv(csv_url)
    st.write("데이터프레임 미리보기:")
    st.dataframe(df.head())
except:
    st.warning("CSV 불러오기를 위한 Google Drive ID를 입력해주세요.")

# PNG (이미지 불러오기)
png_id = "PNG_FILE_ID_HERE"
png_url = f"https://drive.google.com/uc?id={png_id}"
try:
    response = requests.get(png_url)
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="LDA 분석 시각화 예시")
except:
    st.info("PNG 불러오기를 위한 ID를 입력해주세요.")
