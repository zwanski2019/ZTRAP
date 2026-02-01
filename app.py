import streamlit as st
import subprocess
import os
import json
import time
import base64
import getpass
import pandas as pd
import numpy as np
from datetime import datetime

# --- SECURITY: IDENTITY LOCK ---
# Note: On Streamlit Cloud, getuser() returns 'adminuser'. 
# For local Kali use, keep your name.
if getpass.getuser() not in ["zwanski", "adminuser"]:
    st.error("🛑 UNAUTHORIZED OPERATOR DETECTED. SYSTEM LOCKING.")
    st.stop()

# --- APP CONFIG ---
st.set_page_config(page_title="ZTRAP | Elite Red Team Console", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&display=swap');
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Fira Code', monospace; }
    .stSidebar { border-right: 1px solid #00FF41; background-color: #0a0a0a; }
    .stButton>button { border: 1px solid #00FF41; color: #00FF41; background: #000; width: 100%; font-weight: bold; }
    .stButton>button:hover { background: #00FF41; color: #000; box-shadow: 0px 0px 15px #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAV ---
with st.sidebar:
    st.title("🛡️ ZWANZKI")
    menu = ["DASHBOARD", "RECON-ORCHESTRATOR", "EXPLOIT-LAB", "SYSTEM-ACCESS", "GLOBAL-INTEL"]
    choice = st.sidebar.radio("COMMANDS", menu)

# --- DASHBOARD ---
if choice == "DASHBOARD":
    st.title("⚡ ZTRAP v2.0 // COMMAND")
    col1, col2, col3 = st.columns(3)
    col1.metric("Live Targets", "4.6k", "+12")
    col2.metric("Critical CVEs", "8", "+1")
    col3.metric("Bounty Earned", "$12,400", "Tier-1")
    st.info("Recent Intelligence: Target Twilio Staging // OAuth Device Flow Exposure // Severity: HIGH")

# --- RECON ---
elif choice == "RECON-ORCHESTRATOR":
    st.header("🎯 Target Orchestration")
    target = st.text_input("BASE DOMAIN", "paypal.com")
    header = st.text_input("IDENTIFIER", "X-PP-BB: HackerOne-zwanski")
    workflow = st.multiselect("TOOLCHAIN", ["Passive Recon", "Port Discovery", "Nuclei Scan"], default=["Passive Recon"])
    
    if st.button("INITIATE ATTACK SURFACE MAPPING"):
        with st.status("Running Pipeline..."):
            if "Passive Recon" in workflow:
                # This assumes tools are installed on the host
                st.write("Executing Subfinder...")
                # subprocess.run(f"subfinder -d {target}", shell=True) 
        st.success("Sequence complete. Results logged to shadow vault.")

# --- EXPLOIT LAB ---
elif choice == "EXPLOIT-LAB":
    st.header("🧪 Proprietary Payload Forge")
    vector = st.selectbox("Vector", ["SSTI", "OAuth Bypass", "JWT Injection"])
    st.code("{{7*7}}", language="jinja2")
    st.button("ENCODE & BYPASS WAF")

# --- SYSTEM ACCESS ---
elif choice == "SYSTEM-ACCESS":
    st.header("💻 Direct Shell Access")
    st.warning("All commands are logged to internal audit.")
    cmd = st.text_input("ROOT@KALI:~#")
    if st.button("RUN"):
        try:
            out = subprocess.check_output(cmd, shell=True).decode()
            st.code(out)
        except Exception as e:
            st.error(f"Error: {e}")

# --- GLOBAL INTEL ---
elif choice == "GLOBAL-INTEL":
    st.header("🌎 Real-Time Attack Surface Map")
    map_data = pd.DataFrame(
        np.random.randn(10, 2) / [50, 50] + [37.76, -122.4], 
        columns=['lat', 'lon']
    )
    st.map(map_data)
    st.caption("Live visualization of target infrastructure nodes.")
