import streamlit as st
import pandas as pd

st.title("🧠 My Wellbeing App")

st.subheader("Track your day")
sleep = st.slider("Sleep (hours)", 0.0, 12.0, 7.0, 0.5)
mood = st.slider("Mood (1 = bad, 10 = great)", 1, 10, 5)

if st.button("Save"):
    st.success(f"Saved: {sleep}h sleep, mood {mood}/10")
