import getpass

# Hard-lock to your specific Kali username
if getpass.getuser() != "zwanski":
    st.error("UNAUTHORIZED OPERATOR DETECTED. SYSTEM LOCKING.")
    os._exit(0)
import streamlit as st
import subprocess, os, json, time, base64
from datetime import datetime
import pandas as pd
import numpy as np

elif choice == "GLOBAL-INTEL":
    st.header("🌎 Real-Time Attack Surface Map")
    # Generate mock data based on your target's IP geo-location
    map_data = pd.DataFrame(
        np.random.randn(10, 2) / [50, 50] + [37.76, -122.4], # Centered on Silicon Valley
        columns=['lat', 'lon']
    )
    st.map(map_data)
    st.caption("Live visualization of target infrastructure nodes and staging clusters.")
# --- SYSTEM CONFIGURATION ---
ST_CONFIG = {"page_title": "ZTRAP | Elite Red Team Console", "layout": "wide"}
st.set_page_config(**ST_CONFIG)

# --- ADVANCED CSS (Hacker-Elite Aesthetics) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&display=swap');
    body, .stApp { background-color: #050505; color: #00FF41; font-family: 'Fira Code', monospace; }
    .stSidebar { border-right: 1px solid #00FF41; background-color: #0a0a0a; }
    .reportview-container { background: #050505; }
    .stButton>button { border: 1px solid #00FF41; color: #00FF41; background: #000; width: 100%; font-weight: bold; }
    .stButton>button:hover { background: #00FF41; color: #000; box-shadow: 0px 0px 15px #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# --- PLUGIN LOADER (The Proprietary Logic) ---
def load_attack_plugins():
    # Imagine these are private modules you push to your private repo
    return ["CVE-2024-ExploitChain", "OAuth-Device-Code-Phish", "SSTI-DeepScan", "LogicFlaw-Hunter"]

# --- DYNAMIC EXECUTION ENGINE ---
def execute_pipeline(target, workflow_steps, h1_header):
    results = {}
    progress_bar = st.progress(0)
    
    for i, step in enumerate(workflow_steps):
        st.write(f"🚀 **Executing Stage {i+1}: {step}**")
        if step == "Passive Recon":
            # Direct Kali integration
            cmd = f"subfinder -d {target} -silent | assetfinder --subs-only | sort -u"
            out = subprocess.check_output(cmd, shell=True).decode()
            results['domains'] = out.split("\n")
        elif step == "Nuclei Scan":
            # Sophisticated Nuclei integration
            cmd = f"nuclei -u {target} -H '{h1_header}' -severity critical,high -silent"
            # Real-time capture would go here
            results['vulns'] = "Scan initiated..."
        
        progress_bar.progress((i + 1) / len(workflow_steps))
    return results

# --- MAIN UI ---
st.title("⚡ ZTRAP v2.0 // OPERATOR: ZWANZKI")
st.sidebar.image("https://img.icons8.com/nolan/128/security-shield.png", width=80)

menu = ["DASHBOARD", "RECON-ORCHESTRATOR", "EXPLOIT-LAB", "SYSTEM-ACCESS"]
choice = st.sidebar.radio("COMMANDS", menu)

if choice == "DASHBOARD":
    col1, col2, col3 = st.columns(3)
    col1.metric("Live Targets", "4.6k", "+12")
    col2.metric("Critical CVEs", "8", "+1")
    col3.metric("Bounty Earned", "$12,400", "Tier-1")
    
    st.subheader("Recent Intelligence Stream")
    st.info("Target: Twilio Staging // Found: OAuth Device Flow Exposure // Severity: HIGH")

elif choice == "RECON-ORCHESTRATOR":
    target = st.text_input("BASE DOMAIN", "paypal.com")
    header = st.text_input("IDENTIFIER", "X-PP-BB: HackerOne-zwanski")
    workflow = st.multiselect("TOOLCHAIN", ["Passive Recon", "Port Discovery", "HTTP Probing", "Nuclei Scan"])
    
    if st.button("INITIATE GLOBAL ATTACK SURFACE MAPPING"):
        data = execute_pipeline(target, workflow, header)
        st.write(data)

elif choice == "EXPLOIT-LAB":
    st.header("Proprietary Payload Forge")
    st.selectbox("Attack Vector", load_attack_plugins())
    st.text_area("Payload Buffer", "{{7*7}}", height=200)
    st.button("ENCODE & BYPASS WAF")

elif choice == "SYSTEM-ACCESS":
    st.header("Direct Kali Shell (Restricted)")
    st.warning("All commands are logged to internal audit.")
    cmd = st.text_input("ROOT@KALI:~#")
    if st.button("RUN"):
        out = subprocess.check_output(cmd, shell=True).decode()
        st.code(out)
