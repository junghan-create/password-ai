import streamlit as st
import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("🔐 AI 패스워드 보안 진단 시스템")

password = st.text_input("비밀번호를 입력하세요", type="password")

if st.button("진단하기"):
st.write("분석 중...")

```
vec = vectorizer.transform([password])

prob = model.predict_proba(vec)[0]

risk = round(prob[0] * 100, 1)
secure = round(prob[1] * 100, 1)

st.write(f"위험도: {risk}%")
st.write(f"안전도: {secure}%")
```
