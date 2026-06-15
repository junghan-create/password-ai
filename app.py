import streamlit as st
import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.set_page_config(
page_title="AI 패스워드 보안 진단 시스템",
page_icon="🔐"
)

st.title("🔐 AI 패스워드 보안 진단 시스템")

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

    if risk >= 50:
        st.error(f"🚨 위험한 비밀번호 (위험도 {risk}%)")
    else:
        st.success(f"✅ 비교적 안전한 비밀번호 (안전도 {secure}%)")

    st.progress(int(secure))
