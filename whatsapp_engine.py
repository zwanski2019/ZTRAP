import subprocess
import os
import sys
import streamlit as st

# Path to the tool within your project
WSP_PATH = "WhatsApp-OSINT"

def install_whatsapp_osint():
    """Clones and installs dependencies for the WhatsApp-OSINT tool."""
    st.info("🛰️ Initializing WhatsApp-OSINT Environment...")
    try:
        if not os.path.exists(WSP_PATH):
            subprocess.run(["git", "clone", "https://github.com/zwanski2019/WhatsApp-OSINT"], check=True)
        
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", f"{WSP_PATH}/requirements.txt"], check=True)
        st.success("✅ WhatsApp-OSINT Ready for Operation.")
        return True
    except Exception as e:
        st.error(f"❌ Setup Failed: {e}")
        return False

def run_whatsapp_scan(phone_number):
    """Runs the OSINT scan as a subprocess and captures live output."""
    # Note: Adjust the entry script name based on your repo's main file (e.g., main.py or wsp_osint.py)
    cmd = [sys.executable, f"{WSP_PATH}/main.py", "--number", phone_number]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    output_area = st.empty()
    full_log = ""
    
    for line in process.stdout:
        full_log += line
        output_area.code(full_log)
    
    process.wait()