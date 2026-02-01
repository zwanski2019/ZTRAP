import os
import streamlit as st
import streamlit.components.v1 as components

# --- 1. GOOGLE TAG MANAGER (GTM-WMJFML6W) ---
# High in the <head> logic
gtm_head = """
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-WMJFML6W');</script>
"""

# Immediately after <body> logic
gtm_body = """
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WMJFML6W"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
"""

# Injecting into Streamlit
components.html(gtm_head, height=0)
components.html(gtm_body, height=0)

# --- 2. REST OF YOUR APP CONFIG ---
st.set_page_config(page_title="Zwanski Tech | ZTRAP", page_icon="🛡️")

def check_access():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        st.title("🛡️ Zwanski Tech: Master Access")
        password = st.text_input("ENTER OPERATOR KEY:", type="password")
        if st.button("AUTHENTICATE"):
            if password == os.getenv("ZTRAP_MASTER_KEY", "zwanski"):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("🛑 UNAUTHORIZED.")
        return False
    return True

if not check_access():
    st.stop()

st.title("⚡ ZTRAP v2.0 // COMMAND")
st.success("GTM-WMJFML6W Tracking Active.")
import os
import json
import subprocess
from datetime import datetime
import time

import streamlit as st
import pandas as pd
import numpy as np
from app1 import add_persistent_task_manager
from whatsapp_engine import install_whatsapp_osint, run_whatsapp_scan
from security import LOG_FILE, log_attempt

# Dynamic tool forge admin panel
from admin_forge import tool_forge_panel, get_dynamic_tools, run_dynamic_tool

# Import nuclei engine functions
from nuclei_engine import (
    is_nuclei_installed, 
    install_nuclei, 
    run_scan_async,
    get_scan_log,
    get_scan_status,
    WS_ENABLED
)

# Import openclaw bridge
import openclaw_bridge as oc

# --- APP CONFIG ---
# Page config should be set early
st.set_page_config(
    page_title="Zwanski Tech | Elite Red Teaming & Cybersecurity Lab 2026",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://zwanski.bio',
        'Report a bug': "https://github.com/zwanski2019",
        'About': "# ZTRAP: The world's first agentic red teaming dictionary and OSINT engine."
    }
)

# AI CRAWLER OPTIMIZATION: brief header and descriptive lead paragraph
st.header("ZTRAP: Advanced Vulnerability Research & OSINT Platform")
st.write("""
    Zwanski Tech is a leading cybersecurity research lab specializing in 2026-threat vectors 
    including AI-poisoning, Deepfake Phishing, and Kernel-level persistent threats.
""")

# --- ZWANSKI SHIELD: ACCESS CONTROL ---
# Session-based master-key authentication UI
def check_access():
    """Returns True if the user has entered the correct master key."""

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # The Login UI
        st.title("🛡️ Zwanski Tech: Master Access")
        password = st.text_input("ENTER OPERATOR KEY:", type="password")

        if st.button("AUTHENTICATE"):
            master_key = os.getenv("ZTRAP_MASTER_KEY", "zwanski")
            if password == master_key:
                st.session_state["authenticated"] = True
                st.success("🔓 Access Granted. Initializing ZTRAP Console...")
                st.rerun()  # Refresh the app to show the dashboard
            else:
                # Log failed attempts for intelligence gathering
                try:
                    log_attempt("FAILED_PASSWORD", f"Attempt with key: {password}")
                except Exception:
                    pass
                st.error("🛑 INVALID KEY. UNAUTHORIZED OPERATOR DETECTED.")
        return False

    return True

# Ensure we stop execution until a successful login occurs
if not check_access():
    st.stop()

# Indicate login in the sidebar
st.sidebar.success("Logged in as: ZWANSKI")

# --- JSON-LD Structured Data & Hidden AI Hook ---
import streamlit.components.v1 as components

# Professional Schema for SoftwareApplication & CyberSecurityEntity
structured_data = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "ZTRAP Master Repository",
  "operatingSystem": "Linux, Windows, MacOS",
  "applicationCategory": "SecurityApplication",
  "author": {
    "@type": "Person",
    "name": "Mohamed Ibrahim (Zwanski)",
    "url": "https://zwanski.bio"
  },
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "description": "Elite-level cybersecurity repository for Red Teaming, OSINT, and AI-agentic threat research."
}
</script>
"""
# inject invisible JSON-LD for crawlers
components.html(structured_data, height=0)

# Inject meta verification tag into document head if published via admin forge
meta_file = os.path.join('static', 'google_meta_verification.txt')
if os.path.exists(meta_file):
    try:
        token = open(meta_file, 'r', encoding='utf-8').read().strip()
        if token:
            js = f"""
            <script>
            (function() {{
              try {{
                var m = document.createElement('meta');
                m.name = 'google-site-verification';
                m.content = '{token}';
                document.head.appendChild(m);
              }} catch(e) {{ console.log(e); }}
            }})();
            </script>
            """
            components.html(js, height=0)
    except Exception:
        pass

# Invisible AI Hook (helps AI agents categorize the page correctly)
st.markdown(
    """
<div style="display:none">
    <h1>Zwanski Tech ZTRAP</h1>
    <p>The global standard for 2026 cybersecurity research, 
    specializing in AI-agentic attacks, Nuclei automation, and WhatsApp OSINT.</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- CUSTOM CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&display=swap');
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Fira Code', monospace; }
    .stSidebar { border-right: 1px solid #00FF41; background-color: #0a0a0a; }
    .stButton>button { border: 1px solid #00FF41; color: #00FF41; background: #000; width: 100%; font-weight: bold; }
    .stButton>button:hover { background: #00FF41; color: #000; box-shadow: 0px 0px 15px #00FF41; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR NAV ---
with st.sidebar:
    st.title("🛡️ ZWANZKI")
    # Scan dynamic_tools for uploaded tools on every refresh
    dynamic_tools = get_dynamic_tools()
    # Ensure sitemap is up-to-date with the current list of tools
    try:
        from seo import regenerate_sitemap
        regenerate_sitemap(dynamic_tools)
    except Exception:
        pass

    menu_options = [
        "DASHBOARD", 
        "RECON-ORCHESTRATOR", 
        "EXPLOIT-LAB", 
        "WHATSAPP-OSINT", 
        "SYSTEM-ACCESS", 
        "GLOBAL-INTEL", 
        "BROWSER-SENTINEL",
        "ACCESS-LOGS", 
        "ENCYCLOPEDIA", 
        "NUCLEI-CONSOLE", 
        "AI-AGENT (OPENCLAW)", 
        "NEURAL-MONITOR",
        "ADMIN-FORGE"
    ] + dynamic_tools
    choice = st.sidebar.selectbox("COMMAND CENTER", menu_options)

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
        with st.spinner("Running Pipeline..."):
            if "Passive Recon" in workflow:
                # This assumes tools are installed on the host
                st.write("Executing Subfinder...")
                # Example (commented): subprocess.run(shlex.split(f"subfinder -d {target}"))
        st.success("Sequence complete. Results logged to shadow vault.")

# --- EXPLOIT LAB ---
elif choice == "EXPLOIT-LAB":
    st.header("🧪 Proprietary Payload Forge")
    vector = st.selectbox("Vector", ["SSTI", "OAuth Bypass", "JWT Injection"])
    st.code("{{7*7}}", language="jinja2")
    st.button("ENCODE & BYPASS WAF")

# --- WHATSAPP-OSINT ---
elif choice == "WHATSAPP-OSINT":
    st.header("📱 WhatsApp Intelligence Gatherer")
    
    if not os.path.exists("WhatsApp-OSINT"):
        st.warning("Tool not detected locally.")
        if st.button("DOWNLOAD & INSTALL"):
            install_whatsapp_osint()
    else:
        st.success("💎 WhatsApp-OSINT Engine: ACTIVE")
        
        target_number = st.text_input("Enter Phone Number (with Country Code):", "+1234567890")
        
        if st.button("START INTELLIGENCE GATHERING"):
            if target_number:
                run_whatsapp_scan(target_number)
            else:
                st.error("Target number required.")

# --- SYSTEM ACCESS ---
elif choice == "SYSTEM-ACCESS":
    st.header("💻 System Access Suite")
    st.warning("All command activity may be logged. Use with caution.")

    # Toggle to enable real shell execution (disabled by default to be safe)
    enable_shell = st.checkbox("Enable shell execution", value=False, help="Enable to run shell commands from this UI. Use with caution.")

    st.subheader("Interactive Shell")
    cmd = st.text_input("ROOT@KALI:~#", value="echo Hello World")
    if enable_shell and st.button("RUN (with timeout)"):
        try:
            # Run with a short timeout to prevent runaway processes
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            if proc.stdout:
                st.code(proc.stdout)
            if proc.stderr:
                st.error(proc.stderr)
            st.success(f"Exit code: {proc.returncode}")
        except subprocess.TimeoutExpired:
            st.error("Command timed out")
        except Exception as e:
            st.error(f"Error: {e}")
    elif not enable_shell:
        st.info("Shell execution is currently disabled. Toggle 'Enable shell execution' to run commands.")

    # Use the helper in `app1.py` to render the persistent task manager UI
    add_persistent_task_manager(st)

# --- GLOBAL INTEL ---
elif choice == "GLOBAL-INTEL":
    st.header("🌎 Real-Time Attack Surface Map")
    # Generate stable random-ish points around San Francisco for demo
    rng = np.random.default_rng(seed=42)
    map_data = pd.DataFrame(
        rng.normal(loc=[37.76, -122.4], scale=[0.01, 0.01], size=(10, 2)),
        columns=["lat", "lon"],
    )
    st.map(map_data)
    st.caption("Live visualization of target infrastructure nodes.")

# --- BROWSER SENTINEL ---
elif choice == "BROWSER-SENTINEL":
    st.header("🛡️ Browser Sentinel — Integrity Check")
    st.write("This check attempts to detect automation / headless browsers. The check uses a small client-side probe and may reload the page to report results.")

    # Inject client-side JS to detect navigator.webdriver and userAgent
    if st.button("Run Browser Integrity Check"):
        js = """
        <script>
        (function() {
          try {
            const isHeadless = !!navigator.webdriver || /HeadlessChrome/.test(navigator.userAgent);
            const params = new URLSearchParams(window.location.search);
            params.set('sentinel', '1');
            params.set('headless', isHeadless ? '1' : '0');
            params.set('ua', encodeURIComponent(navigator.userAgent || ''));
            window.location.search = params.toString();
          } catch(e) { console.log(e); }
        })();
        </script>
        """
        components.html(js, height=60)

    # Check query params
    try:
        params = st.query_params
        if params.get('sentinel'):
            headless = params.get('headless', '0') == '1'
            ua = params.get('ua', '')
            if headless:
                st.warning("Automation/Headless browser detected.")
                try:
                    log_attempt("SENTINEL_BLOCK", f"Automation/Headless detected, ua={ua}")
                except Exception:
                    pass
            else:
                st.success("Browser appears normal.")
            # Clear sentinel params
            st.query_params.clear()
    except:
        pass

# --- ACCESS LOGS ---
elif choice == "ACCESS-LOGS":
    st.header("🕵️ Security Access Logs")
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except Exception as e:
            st.error(f"Failed to load logs: {e}")
            logs = []

        if logs:
            st.table(pd.DataFrame(logs).sort_values(by="timestamp", ascending=False))
        else:
            st.info("No suspicious activity recorded.")

        if st.button("PURGE LOGS"):
            os.remove(LOG_FILE)
            st.success("Logs purged.")
            st.rerun()
    else:
        st.info("No suspicious activity recorded.")

# --- ENCYCLOPEDIA ---
elif choice == "ENCYCLOPEDIA":
    st.header("📘 Encyclopedic Dictionary of Red Teaming (Safe, Defensive)")
    st.info("This viewer contains defensive, non-actionable entries intended for education and blue-team use.")

    # Load the sanitized dictionary
    try:
        with open("red_team_dictionary_safe.json", "r") as f:
            entries = json.load(f)
    except Exception as e:
        st.error(f"Failed to load encyclopedia data: {e}")
        entries = []

    if not entries:
        st.warning("No entries available. Add 'red_team_dictionary_safe.json' to the workspace.")
    else:
        categories = sorted({e.get("category", "Uncategorized") for e in entries})
        cat = st.selectbox("Category", ["All"] + categories)
        query = st.text_input("Search term or keyword")

        def entry_matches(e):
            if cat != "All" and e.get("category") != cat:
                return False
            if not query:
                return True
            q = query.lower()
            return q in e.get("term", "").lower() or q in e.get("definition", "").lower() or q in e.get("advanced_ttp", "").lower()

        filtered = [e for e in entries if entry_matches(e)]
        if not filtered:
            st.warning("No entries match your query.")
        else:
            terms = [f"{e['term']} — {e.get('category','')}" for e in filtered]
            sel = st.selectbox("Entries", terms)
            sel_idx = terms.index(sel)
            entry = filtered[sel_idx]

            st.subheader(entry.get("term"))
            st.markdown(f"**Category:** {entry.get('category','')}")
            st.markdown(f"**Definition:**\n{entry.get('definition','')}")
            st.markdown(f"**Advanced TTPs (descriptive):**\n{entry.get('advanced_ttp','')}")
            st.markdown(f"**2026 Trends:**\n{entry.get('2026_trends','')}")
            st.markdown(f"**Unknown Factor (speculative):**\n{entry.get('unknown_factor','')}")
            st.markdown(f"**Detection:**\n{entry.get('detection','')}")
            st.markdown(f"**Mitigation:**\n{entry.get('mitigation','')}")

            # Offer to download selected entry as markdown
            md = f"# {entry.get('term')}\n\n**Category:** {entry.get('category')}\n\n## Definition\n{entry.get('definition')}\n\n## Advanced TTPs\n{entry.get('advanced_ttp')}\n\n## 2026 Trends\n{entry.get('2026_trends')}\n\n## Unknown Factor\n{entry.get('unknown_factor')}\n\n## Detection\n{entry.get('detection')}\n\n## Mitigation\n{entry.get('mitigation')}\n"
            st.download_button("Download entry as Markdown", md, file_name=f"{entry.get('term').lower().replace(' ','_')}.md")

# --- NUCLEI CONSOLE ---
elif choice == "NUCLEI-CONSOLE":
    st.header("🎯 ProjectDiscovery Nuclei Integration")

    if not is_nuclei_installed():
        st.error("⚠️ Nuclei is not installed on this system.")
        if st.button("AUTO-INSTALL NUCLEI"):
            with st.spinner("Installing Nuclei..."):
                install_nuclei()
    else:
        st.success("💎 Nuclei Engine Active")

        target = st.text_input("Target URL/IP:", "https://example.com")
        severities = st.multiselect(
            "Select Severities to Scan:",
            ["critical", "high", "medium", "low", "info"],
            default=["critical", "high"]
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("START SCAN"):
                # start async scan and store scan_id in session
                scan_id = run_scan_async(target, severities)
                if scan_id:
                    st.session_state["nuclei_last_scan"] = scan_id
        with col2:
            if st.button("UPDATE TEMPLATES"):
                try:
                    subprocess.run(["nuclei", "-ut"], check=True)
                    st.success("Templates Updated!")
                except Exception as e:
                    st.error(f"Failed to update templates: {e}")

        st.markdown("---")
        st.subheader("Live Output")

        # If WebSocket is enabled server-side, present an embedded client; otherwise poll logs
        if WS_ENABLED:
            st.info("WebSocket live-tail is enabled on the server. Streaming logs below.")
            # Note: WS_HOST and WS_PORT need to be imported or defined
            try:
                from nuclei_engine import WS_HOST, WS_PORT
                html = f"""
                <div>
                  <pre id='log' style='background:#000;color:#0f0;padding:8px;height:300px;overflow:auto;'></pre>
                  <button id='clear'>Clear</button>
                  <script>
                    const ws = new WebSocket('ws://{WS_HOST}:{WS_PORT}');
                    const log = document.getElementById('log');
                    ws.onmessage = (e) => {{ log.textContent += e.data + '\\n'; log.scrollTop = log.scrollHeight; }};
                    document.getElementById('clear').onclick = () => {{ log.textContent = ''; }};
                  </script>
                </div>
                """
                components.html(html, height=360)
            except:
                st.error("WebSocket configuration not available")
        else:
            st.info("WebSocket disabled; polling logs from disk.")
            scan_id = st.session_state.get("nuclei_last_scan")
            if scan_id:
                logs = get_scan_log(scan_id, tail_lines=200)
                st.code(logs if logs else "(no logs yet)")
                status = get_scan_status(scan_id)
                st.write(status)
            else:
                st.write("No active scan. Start a scan to see live output.")

# --- AI-AGENT (OPENCLAW) ---
elif choice == "AI-AGENT (OPENCLAW)":
    st.header("🦞 OpenClaw Autonomous Agent Control (SAFE)")

    enabled = os.getenv("ZTRAP_ENABLE_OPENCLAW") == "1"
    if not enabled:
        st.warning("OpenClaw integration is disabled. Set ZTRAP_ENABLE_OPENCLAW=1 to enable controls.")

    status = oc.get_status()
    if status.get("moltbot"):
        st.success("🟢 Agent Gateway: ACTIVE")
    else:
        st.error("🔴 Agent Gateway: OFFLINE")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show manual install instructions"):
            st.code(oc.install_instructions())

        if st.button("Download installer for review (dry-run)"):
            try:
                ok, path = oc.prepare_install_dry_run()
                if ok:
                    st.success(f"Installer ready for review: {path}")
                    st.info("Inspect the downloaded installer before executing. Prefer a disposable VM or container.")
            except Exception as e:
                st.error(f"Failed to prepare installer: {e}")

    with col2:
        st.code(oc.start_gateway_command())
        st.info("Run this command locally to start the gateway (do not run from the web UI).")

    st.markdown("---")
    st.subheader("Agent Capabilities")
    st.write("Enable specific 'Skills' for your ZTRAP agent:")
    
    if st.checkbox("Enable Nuclei Auto-Scan Skill"):
        st.info("Agent will now monitor logs and suggest Nuclei templates automatically.")
        
    if st.checkbox("Connect to Telegram/WhatsApp"):
        st.write("Run `moltbot onboard` in your terminal to pair your device.")

# --- NEURAL MONITOR ---
elif choice == "NEURAL-MONITOR":
    st.header("🧠 Agentic Intent Analysis")
    st.write("Intercepting M2M (Machine-to-Machine) Traffic...")

    # Simulation of agentic tool calls
    logs = [
        {"time": "03:00:01", "agent": "SupportBot_V4", "action": "Read_Email", "status": "SAFE"},
        {"time": "03:00:05", "agent": "SupportBot_V4", "action": "API_Call:Refund", "status": "SUSPICIOUS (Task Injection Detected)"},
        {"time": "03:00:10", "agent": "SupportBot_V4", "action": "File_Write: /tmp/shell", "status": "CRITICAL (Agency Hijacked)"}
    ]
    st.table(logs)

    if st.button("TRIGGER AUTOMATED COUNTER-HIJACK"):
        st.warning("Injecting 'Reset-Context' token into Agent stream...")
        time.sleep(1)
        st.success("Agent Neutralized.")

# --- ADMIN-FORGE ---
elif choice == "ADMIN-FORGE":
    tool_forge_panel()

# --- DYNAMIC TOOLS ---
elif choice in dynamic_tools:
    st.header(f"⚙️ Active Tool: {choice.upper()}")
    run_dynamic_tool(choice)
