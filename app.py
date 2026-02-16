import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# Your Live N8N URL
WEBHOOK_URL = "https://n8n-pg0sccggco4ow0wgocsgw0g0.93.127.213.62.sslip.io/webhook/upload-invoice"

st.set_page_config(page_title="Debug Invoice App", layout="wide")

st.title("🛠️ Debug Mode: Invoice App")
st.markdown(f"**Target URL:** `{WEBHOOK_URL}`")

uploaded_file = st.file_uploader("Upload Invoice (PDF/Image)", type=['pdf', 'png', 'jpg'])

if uploaded_file:
    if st.button("Test Connection"):
        with st.spinner("Sending to n8n..."):
            try:
                # 1. Prepare File
                files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
                
                # 2. Send Request
                response = requests.post(WEBHOOK_URL, files=files)
                
                # 3. SHOW RAW DEBUG INFO
                st.subheader("📡 Server Response Info")
                st.write(f"**Status Code:** `{response.status_code}`")
                
                st.subheader("📝 Raw Text Received")
                st.text(response.text)
                
                # 4. Attempt to Parse JSON
                st.subheader("🧩 JSON Parsing Result")
                try:
                    data = response.json()
                    st.success("✅ Success! JSON is valid.")
                    st.json(data)
                except json.JSONDecodeError:
                    st.error("❌ Failed to parse JSON. The server returned text (html or error), not data.")
            
            except Exception as e:
                st.error(f"❌ Application Crash: {e}")