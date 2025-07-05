import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# === Load data ===
@st.cache_data
def load_data():
    df = pd.read_csv("bearable_export.csv")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df["date_formatted"] = pd.to_datetime(df["date_formatted"], errors="coerce")

    def parse_sleep(val):
        try:
            if ":" in str(val):
                h, m = val.split(":")
                return int(h) + int(m) / 60
            return float(val)
        except:
            return None

    def parse_mood_energy(val):
        try:
            return float(val)
        except:
            return None

    relevant = df[df["category"].isin(["Mood", "Sleep", "Energy"])].copy()
    relevant["rating/amount"] = relevant["rating/amount"].astype(str).str.strip()
    relevant["value"] = relevant.apply(
        lambda row: parse_sleep(row["rating/amount"]) if row["category"] == "Sleep" else parse_mood_energy(row["rating/amount"]),
        axis=1
    )

    summary = relevant.groupby(["date_formatted", "category"])["value"].mean().unstack()
    summary = summary.rename(columns={
        "Mood": "mood_avg",
        "Sleep": "sleep_hours",
        "Energy": "energy_avg"
    }).reset_index()
    return summary.dropna(subset=["mood_avg", "sleep_hours"])

df = load_data()

# === Layout ===
st.set_page_config(page_title="Wellbeing Tracker", layout="centered")

st.title("🧠 My Wellbeing Tracker")

tab1, tab2, tab3 = st.tabs(["📈 Trends", "🔁 Sleep vs Mood", "📄 Raw Data"])

with tab1:
    st.subheader("Daily Mood, Sleep & Energy")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date_formatted"], df["mood_avg"], label="Mood (1–5)", marker="o")
    ax.plot(df["date_formatted"], df["sleep_hours"], label="Sleep (h)", marker="s")
    if "energy_avg" in df.columns:
        ax.plot(df["date_formatted"], df["energy_avg"], label="Energy (1–5)", marker="^")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    st.subheader("How does sleep affect mood?")
    fig2, ax2 = plt.subplots()
    ax2.scatter(df["sleep_hours"], df["mood_avg"], alpha=0.7)
    ax2.set_xlabel("Sleep (hours)")
    ax2.set_ylabel("Mood (1–5)")
    ax2.grid(True)
    st.pyplot(fig2)

with tab3:
    st.subheader("Raw Processed Data")
    st.dataframe(df, use_container_width=True)
