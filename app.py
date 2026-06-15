import streamlit as st
import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("AI Password Checker")

password = st.text_input("Password", type="password")

if st.button("Check"):
      st.write("Working...")

      vec = vectorizer.transform([password])
      prob = model.predict_proba(vec)[0]

      st.write(prob)
