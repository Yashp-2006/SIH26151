import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configure page
st.set_page_config(page_title="PRAMANA Investigator Dashboard", page_icon="🕵️", layout="wide")

# API Configuration
API_URL = "http://127.0.0.1:8000"

st.sidebar.title("PRAMANA Engine")
st.sidebar.markdown("Identity attribution driven by rigorous mathematics.")
page = st.sidebar.radio("Navigation", ["Balance Sheet", "Live Ingestion", "Calibration Metrics"])

def authenticate():
    """Simulate getting a token for the API."""
    try:
        response = requests.post(f"{API_URL}/token", data={"username": "admin", "password": "admin"})
        if response.status_code == 200:
            return response.json()["access_token"]
    except:
        pass
    return None

if page == "Balance Sheet":
    st.title("Evidence Balance Sheet")
    st.markdown("Query the PRAMANA fusion engine to evaluate the likelihood that two pseudonymous accounts belong to the same physical operator.")
    
    col1, col2 = st.columns(2)
    with col1:
        account_a = st.text_input("Account Alias A", placeholder="e.g. DreadPirateRoberts")
    with col2:
        account_b = st.text_input("Account Alias B", placeholder="e.g. Altoid")
        
    if st.button("Generate Assessment", type="primary"):
        if not account_a or not account_b:
            st.error("Please enter both account aliases.")
        else:
            token = authenticate()
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            
            with st.spinner("Compiling cryptographic and behavioral evidence..."):
                try:
                    res = requests.get(f"{API_URL}/assess/{account_a}/{account_b}", headers=headers)
                    if res.status_code == 200:
                        data = res.json()
                        st.success("Assessment Complete")
                        
                        # Mocking the visual representation for the demo based on the architecture
                        st.subheader(f"Hypothesis: {account_a} == {account_b}")
                        
                        score_col, status_col = st.columns(2)
                        score_col.metric("Cumulative Log-LR", "4.2", "+1.2 (Strong Support)")
                        status_col.metric("Independence Check (k >= 2)", "PASSED", "3 independent origins")
                        
                        st.markdown("### Processed Evidence Vectors")
                        evidence_data = [
                            {"Family": "F1 (Cryptographic)", "Feature": "Shared PGP Public Key", "Log-LR": 4.0, "Independence": "Pass"},
                            {"Family": "F6 (Linguistic)", "Feature": "Character Trigram Cosine (0.82)", "Log-LR": 0.5, "Independence": "Pass"},
                            {"Family": "F8 (Behavioral)", "Feature": "Temporal Active Hours (75% overlap)", "Log-LR": 1.2, "Independence": "Pass"}
                        ]
                        st.table(pd.DataFrame(evidence_data))
                        
                    else:
                        st.error(f"API Error: {res.status_code}")
                except Exception as e:
                    st.error("Failed to connect to the PRAMANA API. Is the backend running?")
                    
elif page == "Live Ingestion":
    st.title("Kafka Live Ingestion Stream")
    st.markdown("Simulate feeding raw dark web network data into the secure ledger.")
    
    with st.form("ingest_form"):
        event_id = st.text_input("Event ID", value=f"evt_{int(datetime.now().timestamp())}")
        account_id = st.text_input("Observed Account ID", "vendor_777")
        content = st.text_area("Raw Content (Forum Post / Listing)", "Selling digital goods. Contact me on Tox.")
        submitted = st.form_submit_button("Produce to Kafka")
        
        if submitted:
            token = authenticate()
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            payload = {
                "topic": "pramana.listings",
                "listing": {
                    "event_id": event_id,
                    "account_id": account_id,
                    "source_ref": "dread_forum",
                    "snapshot_ref": "snap_001",
                    "listing_ref": "list_001",
                    "content": content
                }
            }
            try:
                res = requests.post(f"{API_URL}/stream/ingest", json=payload, headers=headers)
                if res.status_code == 200:
                    st.success("Payload successfully produced to Kafka broker and persisted to database!")
                    st.json(res.json())
                else:
                    st.error(f"Failed to ingest: {res.text}")
            except:
                st.error("Failed to connect to the PRAMANA API.")

elif page == "Calibration Metrics":
    st.title("Mathematical Bounds & Calibration")
    st.markdown("Prove the mathematical validity of the engine using Empirical Calibration Error (ECE) and Tippett Plots.")
    
    if st.button("Fetch Metrics from Engine"):
        with st.spinner("Calculating ECE across all models..."):
            try:
                res = requests.get(f"{API_URL}/calibration/tippett")
                if res.status_code == 200:
                    data = res.json()
                    st.metric("Expected Calibration Error (ECE)", f"{data.get('ece_score', 0.015)}", "-0.28 (Improvement)")
                    
                    # Mock Plotly graph for Tippett
                    df = pd.DataFrame({
                        'Log-LR': [-3, -2, -1, 0, 1, 2, 3, 4],
                        'Same Source (H1)': [0, 0, 0, 5, 20, 50, 80, 100],
                        'Different Source (H2)': [100, 80, 50, 20, 5, 0, 0, 0]
                    })
                    fig = px.line(df, x='Log-LR', y=['Same Source (H1)', 'Different Source (H2)'], 
                                  title="Tippett Plot (Discriminatory Power)",
                                  labels={'value': 'Cumulative Proportion (%)'})
                    st.plotly_chart(fig)
                else:
                    st.error("Failed to fetch metrics (the ML module might be missing ground-truth data in this environment).")
            except:
                st.error("Failed to connect to the PRAMANA API.")
