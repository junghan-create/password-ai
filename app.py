import streamlit as st
import joblib
import re

# 1. 모델 및 벡터라이저 로드
@st.cache_resource
def load_models():
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

try:
    model, vectorizer = load_models()
except Exception as e:
    st.error(f"모델 파일을 로드하는 중 오류가 발생했습니다: {e}")

# 2. 규칙성 및 개선방안 분석 함수
def analyze_password_rules(password):
    feedback = []
    rule_score = 0  # 규칙성 감점/가점 점수 (기본 0에서 시작)
    
    length = len(password)
    if length == 0:
        return 0, []

    # (1) 길이 검사
    if length < 8:
        feedback.append("❌ 비밀번호가 너무 짧습니다. 최소 8자 이상, 권장 12자 이상으로 설정하세요.")
        rule_score -= 20
    elif length >= 12:
        feedback.append("✅ 비밀번호 길이가 12자 이상으로 아주 훌륭합니다.")
        rule_score += 15
    else:
        feedback.append("⚠️ 길이는 8자 이상이지만, 더 강력한 보안을 위해 12자 이상을 추천합니다.")
        rule_score += 5

    # (2) 문자 종류 다양성 검사 (대문자, 소문자, 숫자, 특수문자)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>_~-]', password))
    
    types_count = sum([has_upper, has_lower, has_digit, has_special])
    
    if types_count >= 3:
        feedback.append("✅ 대문자, 소문자, 숫자, 특수문자 중 3가지 이상을 조합하여 안전성이 높습니다.")
        rule_score += 10
    else:
        feedback.append("❌ 조합이 단순합니다. 영문 대/소문자, 숫자, 특수문자를 섞어주세요.")
        rule_score -= 15

    # (3) 동일 문자 반복 검사 (예: aaa, 111)
    if re.search(r'(.)\1\1', password):
        feedback.append("❌ 동일한 문자가 3번 이상 연속으로 반복됩니다. (예: aaa, 111) 이를 제거하세요.")
        rule_score -= 20

    # (4) 연속 문자 검사 (예: abc, 123, qwe - 순서 및 키보드 배열)
    is_sequential = False
    
    # 알파벳/숫자 순서 연속성 확인 (정방향, 역방향)
    for i in range(len(password) - 2):
        chunk = password[i:i+3]
        if chunk.isdigit() or chunk.isalpha():
            if (ord(chunk[1]) - ord(chunk[0]) == 1 and ord(chunk[2]) - ord(chunk[1]) == 1) or \
               (ord(chunk[0]) - ord(chunk[1]) == 1 and ord(chunk[1]) - ord(chunk[2]) == 1):
                is_sequential = True
                break
                
    # 키보드 배열(Qwerty) 연속성 확인
    qwerty = "qwertyuiopasdfghjklzxcvbnm"
    for i in range(len(password) - 2):
        chunk = password[i:i+3].lower()
        if chunk in qwerty or chunk[::-1] in qwerty:
            is_sequential = True
            break

    if is_sequential:
        feedback.append("❌ 키보드 배열이나 순서상 연속된 문자열이 포함되어 있습니다. (예: 123, abc, qwe)")
        rule_score -= 20

    return rule_score, feedback


# 3. Streamlit UI 구성
st.set_page_config(page_title="AI 패스워드 보안 진단 시스템", page_icon="🔐")

st.title("🔐 AI 패스워드 보안 진단 시스템 v2")
st.markdown("머신러닝 예측 모델과 규칙성 검사를 결합하여 비밀번호의 취약점을 정밀 분석합니다.")

password = st.text_input("비밀번호를 입력하세요", type="password")

if st.button("진단하기"):
    if not password:
        st.warning("비밀번호를 입력해주세요.")
    else:
        # A. AI 모델 기반 예측
        vec = vectorizer.transform([password])
        prob = model.predict_proba(vec)[0]

        ai_risk = prob[0] * 100
        ai_secure = prob[1] * 100

        # B. 휴리스틱 규칙성 검사 수행
        rule_score, feedbacks = analyze_password_rules(password)

        # C. 최종 점수 보정 (AI 예측값에 규칙성 검사 가점/감점 반영)
        # 규칙성 점수를 반영하되, 최종 안전도는 0% ~ 100% 사이로 제한합니다.
        final_secure = max(0.0, min(100.0, ai_secure + rule_score))
        final_risk = 100.0 - final_secure

        final_risk = round(final_risk, 1)
        final_secure = round(final_secure, 1)

        # 결과 화면 출력
        st.write("---")
        st.subheader("📊 종합 진단 결과")
        
        col1, col2 = st.columns(2)
        col1.metric(label="🚨 위험도", value=f"{final_risk}%")
        col2.metric(label="✅ 안전도", value=f"{final_secure}%")

        st.progress(int(final_secure))

        # 최종 스코어 기반 등급 판정
        if final_secure >= 70:
            st.success("🟢 강력하고 안전한 비밀번호입니다.")
        elif final_secure >= 40:
            st.warning("🟡 보통 수준의 비밀번호입니다. 아래 개선방안을 참고하세요.")
        else:
            st.error("🔴 위험한 비밀번호입니다! 즉시 수정을 권장합니다.")

        # D. 맞춤형 개선방안 제공
        st.write("---")
        st.subheader("💡 비밀번호 맞춤형 개선방안")
        if feedbacks:
            for fb in feedbacks:
                st.write(fb)
        else:
            st.write("✨ 특별한 구조적 취약점이 발견되지 않았습니다.")

        # 보안 팁 추가
        st.info("💡 **안전한 비밀번호 Tip:** 본인만 기억할 수 있는 긴 문장(예: `my_hobby_is_singing_7!`)의 형태를 활용하면 기억하기 쉬우면서도 해킹이 불가능에 가까운 강력한 패스워드를 만들 수 있습니다.")
