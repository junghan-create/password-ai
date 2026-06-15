import streamlit as st
import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.set_page_config(
page_title="AI 패스워드 보안 진단 시스템",
page_icon="🔐",
layout="centered"
)

st.title("🔐 AI 패스워드 보안 진단 시스템")

st.write(
"실제 유출 데이터(RockYou) 기반 머신러닝 모델을 활용하여 "
"비밀번호의 위험도를 분석합니다."
)

password = st.text_input(
"비밀번호를 입력하세요",
type="password"
)

if st.button("진단하기"):

if not password:
    st.warning("비밀번호를 입력해주세요.")

else:
    vec = vectorizer.transform([password])

    prob = model.predict_proba(vec)[0]

    risk = round(prob[0] * 100, 1)
    secure = round(prob[1] * 100, 1)

    result = model.predict(vec)[0]

    st.subheader("📊 분석 결과")

    st.write(f"위험도 : {risk}%")
    st.write(f"안전도 : {secure}%")

    st.progress(int(secure))

    if result == 0:
        st.error("🚨 위험한 비밀번호")
    else:
        st.success("✅ 비교적 안전한 비밀번호")
