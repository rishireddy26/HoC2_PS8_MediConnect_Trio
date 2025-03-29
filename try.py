import streamlit as st
import pandas as pd
import ollama
import os
from streamlit_webrtc import webrtc_streamer

# Set up the page
st.set_page_config(page_title="Remote Healthcare Platform", layout="wide")



# User authentication (Basic session handling)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    user = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    if st.button("Login"):
        if user == "admin" and password == "123":  # Replace with actual authentication logic
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid credentials")

if not st.session_state["authenticated"]:
    login()
    st.stop()

# Sidebar navigation
menu = ["Home", "Symptom Checker", "Telemedicine", "Health Records", "Community", "Doctor Dashboard"]
choice = st.sidebar.selectbox("Navigation", menu)

# Home Page
if choice == "Home":
    st.title("Remote Healthcare Access Platform")
    st.write("Providing medical access to remote areas with low-bandwidth features.")
    st.image("image.jpeg", use_container_width=True)

# Symptom Checker Page with AI Diagnosis
elif choice == "Symptom Checker":
    st.header("🩺 AI-Powered Symptom Checker")
    symptoms = st.text_area("Enter your symptoms (comma-separated):")

    if st.button("🔍 Check Diagnosis"):
        if not symptoms.strip():
            st.warning("⚠️ Please enter symptoms before checking.")
        else:
            # Query the trained model
            prompt = f"Symptoms: {symptoms}. What is the disease and treatment?"
            response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

            # Display Results
            st.success(f"**Diagnosis & Treatment:**\n{response['message']['content']}")

# Telemedicine Page
elif choice == "Telemedicine":
    st.header("Connect with a Doctor")
    st.write("Options for Video, Audio, or Text-based consultation.")
    webrtc_streamer(key="video-call")  # Basic WebRTC video call
    st.text_input("Send a message to a doctor")
    st.button("Send")

# Health Records Page
elif choice == "Health Records":
    st.header("Manage Your Health Records")
    uploaded_file = st.file_uploader("Upload Medical Records", type=["pdf", "jpg", "png"])
    if uploaded_file:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded successfully! Saved at {file_path}")

# Community Page
elif choice == "Community":
    st.header("Community Support & Health Resources")
    st.text_area("Ask a question or share your experience")
    st.button("Post")

# Doctor Dashboard
elif choice == "Doctor Dashboard":
    st.header("Doctor Management Panel")
    st.write("Manage appointments, view patient history, and provide remote consultations.")
    patient_name = st.text_input("Enter Patient Name")
    diagnosis = st.text_area("Enter Diagnosis")
    prescription = st.text_area("Enter Prescription Details")
    if st.button("Save Record"):
        st.success("Record Saved Successfully!")
