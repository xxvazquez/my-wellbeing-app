import streamlit as st

st.set_page_config(page_title="My Wellbeing App", layout="centered")
st.title("🧠 My Wellbeing App")

# --- Session state setup ---
if "sleep_hours" not in st.session_state:
    st.session_state.sleep_hours = 7.0
if "tag_pool" not in st.session_state:
    st.session_state.tag_pool = []  # stores previous custom tags

# --- Sleep Tracker ---
st.subheader("🛌 Sleep")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("➖", key="minus_sleep"):
        st.session_state.sleep_hours = max(0, st.session_state.sleep_hours - 0.5)
with col2:
    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.sleep_hours:.1f} hours</h3>", unsafe_allow_html=True)
with col3:
    if st.button("➕", key="plus_sleep"):
        st.session_state.sleep_hours = min(24, st.session_state.sleep_hours + 0.5)

# --- Mood Selection ---
st.subheader("🙂 Mood (1–5)")
mood = st.radio("Select your mood:", [1, 2, 3, 4, 5], horizontal=True, index=2, label_visibility="collapsed")

# --- Tag Entry ---
st.subheader("🏷️ Tags")
new_tags_input = st.text_input("Add new tags (comma-separated)", placeholder="e.g. stress, bloated, nice walk")
new_tags = [t.strip() for t in new_tags_input.split(",") if t.strip()]

# Merge new tags into tag pool
if new_tags:
    for tag in new_tags:
        if tag not in st.session_state.tag_pool:
            st.session_state.tag_pool.append(tag)

# Multi-select from existing tags
selected_tags = st.multiselect("Select tags for today", st.session_state.tag_pool)

# --- Save Button ---
if st.button("✅ Save Entry"):
    st.success(f"Saved: {st.session_state.sleep_hours}h sleep, mood {mood}/5")
    if selected_tags:
        st.write("Tags:", ", ".join(selected_tags))
    else:
        st.write("No tags selected.")
