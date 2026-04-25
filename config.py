import os
import streamlit as st
import json

# Yerel çalışıyorsak dosyadan, buluttaysak Streamlit Secrets'tan oku
if os.path.exists("kimlik.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "kimlik.json"
elif "gcp_service_account" in st.secrets:
    # Bulut üzerinde servis hesabı bilgilerini geçici bir dosyaya yazma
    with open("temp_key.json", "w") as f:
        json.dump(dict(st.secrets["gcp_service_account"]), f)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_key.json"

PROJECT_ID = "smart-syllabus-agent"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"