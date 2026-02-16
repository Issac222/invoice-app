import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# Your Live N8N Backend URL
WEBHOOK_URL = "https://n8n-pg0sccggco4ow0wgocsgw0g0.93.127.213.62.sslip.io/webhook/upload-invoice"

st.set_page_config(page_title="InvoiceAI Agent", layout="wide", page_icon="🧾")

# --- CUSTOM CSS (For Arabic & Design) ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    .metric-card { background-color: #f9f9f9; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .arabic-text { direction: rtl; text-align: right; font-family: 'Amiri', 'Arial', sans-serif; font-size: 18px; color: #333; }
    .stButton>button { width: 100%; border-radius: 5px; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: UPLOADER ---
with st.sidebar:
    st.title("📂 Upload Invoice")
    st.markdown("Upload your invoice (PDF or Image) to extract insights instantly.")
    uploaded_file = st.file_uploader("Choose a file...", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.success("File Ready!")
        if st.button("Analyze Invoice 🚀", type="primary"):
            with st.spinner("⏳ Sending to AI Agent... (This may take 10-20 seconds)"):
                try:
                    # PREPARE FILE FOR API
                    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    
                    # SEND TO N8N
                    response = requests.post(WEBHOOK_URL, files=files)
                    
                    if response.status_code == 200:
                        st.session_state['data'] = response.json()
                        st.success("Analysis Complete!")
                    else:
                        st.error(f"Server Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

# --- MAIN DASHBOARD ---
st.title("🧾 Invoice Intelligence Dashboard")
st.markdown("---")

if 'data' in st.session_state:
    raw_data = st.session_state['data']
    
    # Handle nested JSON if N8N returns { "analysis": { ... } }
    data = raw_data.get('analysis', raw_data)

    # 1. METRICS ROW
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Amount", f"{data.get('total_amount', 0)} {data.get('currency', 'OMR')}")
    c2.metric("📅 Date", data.get('invoice_date', 'N/A'))
    c3.metric("🏢 Merchant", data.get('company_name', 'Unknown'))
    
    # Recommendation Badge
    rec = data.get('recommendation', 'Review')
    color = "green" if "Approve" in rec else "red"
    c4.markdown(f"**Action:**")
    c4.markdown(f":{color}-background[{rec}]")

    st.divider()

    # 2. SUMMARIES ROW
    col_en, col_ar = st.columns(2)
    
    with col_en:
        st.subheader("🇬🇧 English Summary")
        st.info(data.get('summary_english', data.get('summary_en', 'No summary provided.')))
        
    with col_ar:
        st.subheader("🇴🇲 Arabic Summary")
        st.markdown(f"""
        <div class="arabic-text" style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
        {data.get('summary_arabic', data.get('summary_ar', 'لا يوجد ملخص'))}
        </div>
        """, unsafe_allow_html=True)

    # 3. DETAILS EXPANDER
    with st.expander("🔍 View Raw Data Extraction"):
        st.json(data)

else:
    # Empty State
    st.info("👈 Please upload an invoice in the sidebar to begin analysis.")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)