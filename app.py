import streamlit as st
import pandas as pd
import json
import plotly.express as px
import smtplib
from email.message import EmailMessage

@st.cache_data
def load_doctors():
    return pd.read_csv("doctors.csv")

@st.cache_data
def load_feedback():
    try:
        return pd.read_csv("feedback.csv")
    except:
        return pd.DataFrame(columns=["name", "comment"])

doctors_df = load_doctors()
feedback_df = load_feedback()

st.set_page_config(page_title="Doctor Recommender", layout="wide")

# Simulated Google Sign-in (just email input for demo)
if "user_email" not in st.session_state:
    with st.form("login_form"):
        st.title("🔐 Login with Google")
        email = st.text_input("Enter your Google Email")
        submitted = st.form_submit_button("Login")
        if submitted and "@gmail.com" in email:
            st.session_state.user_email = email
            st.success("Logged in as " + email)
        elif submitted:
            st.error("Please enter a valid Gmail address.")

if "user_email" not in st.session_state:
    st.stop()

# Sidebar Navigation
st.sidebar.title("🩺 Doctor Recommender")
page = st.sidebar.radio("Go to", ["🏠 Home", "🔍 Find Doctor", "📈 Stats", "🗣️ Feedback", "📧 Email Doctor", "🚪 Logout"])

# Home Dashboard
if page == "🏠 Home":
    st.title("Welcome to the Doctor Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("👨‍⚕️ Total Doctors", len(doctors_df))
    col2.metric("📋 Specialties", doctors_df['specialty'].nunique())
    col3.metric("🌍 Locations", doctors_df['location'].nunique())

# Doctor Finder Page
elif page == "🔍 Find Doctor":
    st.title("🔍 Find a Doctor")
    symptom = st.text_input("Your Symptom")
    location = st.text_input("Your Location")
    if st.button("Find"):
        results = doctors_df[
            doctors_df['symptoms'].str.contains(symptom, case=False, na=False) &
            doctors_df['location'].str.contains(location, case=False, na=False)
        ]
        if not results.empty:
            st.subheader("Matching Doctors:")
            for idx, row in results.iterrows():
                if st.button(f"View Profile: {row['name']}", key=idx):
                    st.markdown(f"### 👨‍⚕️ {row['name']}")
                    st.markdown(f"**Specialty:** {row['specialty']}")
                    st.markdown(f"**Location:** {row['location']}")
                    st.markdown(f"**Treats:** {row['symptoms']}")
        else:
            st.warning("No doctors found.")

# Charts using Plotly
elif page == "📈 Stats":
    st.title("📊 Statistics")
    fig1 = px.histogram(doctors_df, x="location", title="Doctor Distribution by Location")
    fig2 = px.pie(doctors_df, names="specialty", title="Specialty Distribution")
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

# Feedback Page (Saved to CSV)
elif page == "🗣️ Feedback":
    st.title("🗣️ Leave Your Feedback")
    name = st.text_input("Name")
    comment = st.text_area("Feedback")
    if st.button("Submit Feedback"):
        new_feedback = pd.DataFrame([{"name": name, "comment": comment}])
        new_feedback.to_csv("feedback.csv", mode="a", header=False, index=False)
        st.success("Feedback saved!")

# Simulate emailing a doctor profile
elif page == "📧 Email Doctor":
    st.title("📧 Send Doctor Profile by Email")
    selected_doc = st.selectbox("Select a Doctor", doctors_df['name'])
    recipient = st.text_input("Send to (email):")
    if st.button("Send Email"):
        doc = doctors_df[doctors_df['name'] == selected_doc].iloc[0]
        # Simulate sending
        st.info(f"Email sent to **{recipient}** with profile of **{doc['name']}**, {doc['specialty']} in {doc['location']}.")
        # Note: Real email requires SMTP setup

# Logout
elif page == "🚪 Logout":
    del st.session_state.user_email
    st.success("Logged out.")