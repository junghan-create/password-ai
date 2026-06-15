import streamlit as st
import joblib

모델 및 벡터라이저 불러오기

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

페이지 설정

st.set_page_config(
page_title="AI 패스워드 보안 진단 시스템",
page_icon="🔐",
layout="centered"
)

제목

st.title("🔐 AI 패스워드 보안 진단 시스템")

st.write(
"실제 유출 데이터(RockYou) 기반 머신러닝 모델을 활용하여 "
"비밀번호의 위험도를 분석합니다."
)

비밀번호 입력

password = st.text_input(
"비밀번호를 입력하세요",
type="password"
)

진단 버튼

if st.button("진단하기"):

if not password:
    st.warning("비밀번호를 입력해주세요.")

else:
    vec = vectorizer.transform([password])

    prob = model.predict_proba(vec)[0]

    risk = round(prob[0] * 100, 1)
    secure = round(prob[1] * 100, 1)

    result = model.predict(vec)[0]

    st.divider()
    st.subheader("📊 분석 결과")

    st.write(f"위험도 : {risk}%")
    st.write(f"안전도 : {secure}%")

    st.progress(int(secure))

    if result == 0:
        st.error("🚨 위험한 비밀번호로 판단됩니다.")
    else:
        st.success("✅ 비교적 안전한 비밀번호로 판단됩니다.")

    feature_names = vectorizer.get_feature_names_out()
    nonzero_indices = vec.nonzero()[1]

    patterns = []

    for idx in nonzero_indices:
        patterns.append(
            (feature_names[idx], vec[0, idx])
        )

    patterns = sorted(
        patterns,
        key=lambda x: x[1],
        reverse=True
    )[:3]

    if patterns:
        st.subheader("🔍 탐지된 주요 패턴")

        for p, score in patterns:
            st.write(f"• {p}")

    st.subheader("🛠️ 개선 권고")

    suggestions = []

    if len(password) < 12:
        suggestions.append(
            f"비밀번호 길이를 늘리세요. 현재 {len(password)}자입니다."
        )

    if not any(c.isupper() for c in password):
        suggestions.append("대문자를 추가하세요.")

    if not any(c.islower() for c in password):
        suggestions.append("소문자를 추가하세요.")

    if not any(c.isdigit() for c in password):
        suggestions.append("숫자를 추가하세요.")

    if not any(not c.isalnum() for c in password):
        suggestions.append("특수문자를 추가하세요.")

    if suggestions:
        for s in suggestions:
            st.write("• " + s)
    else:
        st.success("✨ 현재 구조상 추가 개선 사항이 거의 없습니다.")
