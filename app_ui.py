import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("💼 Job Tracker")

# ---------------- ADD JOB ----------------
st.header("Add Job")

company = st.text_input("Company")
role = st.text_input("Role")
status = st.text_input("Status")
date = st.text_input("Applied Date")
notes = st.text_input("Notes")

if st.button("Add Job"):
    data = {
        "company": company,
        "role": role,
        "status": status,
        "applied_date": date,
        "notes": notes
    }

    response = requests.post(f"{BASE_URL}/jobs", json=data)

    if response.status_code == 200:
        st.success("Job added successfully!")
    else:
        st.error("Error adding job")

# ---------------- VIEW JOBS ----------------
st.header("All Jobs")

if st.button("Load Jobs"):
    response = requests.get(f"{BASE_URL}/jobs")

    if response.status_code == 200:
        jobs = response.json()

        for job in jobs:
            st.write(f"ID: {job['id']}")
            st.write(f"Company: {job['company']}")
            st.write(f"Role: {job['role']}")
            st.write(f"Status: {job['status']}")
            st.write(f"Date: {job['applied_date']}")
            st.write(f"Notes: {job['notes']}")
            st.write("----------------------")
    else:
        st.error("Error fetching jobs")