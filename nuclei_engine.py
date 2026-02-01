import subprocess
import shutil
import os
import streamlit as st
import threading
import time
import json
from datetime import datetime

# Paths for logs and database
LOG_DIR = "/tmp/ztrap_nuclei_logs"
NUCLEI_DB_PATH = os.environ.get("ZTRAP_NUCLEI_DB", "/tmp/ztrap_nuclei.db")

os.makedirs(LOG_DIR, exist_ok=True)

# Optional WebSocket broadcasting (disabled by default). Enable via ZTRAP_ENABLE_WS=1
WS_ENABLED = os.environ.get("ZTRAP_ENABLE_WS", "0") == "1"
WS_HOST = os.environ.get("ZTRAP_WS_HOST", "127.0.0.1")
WS_PORT = int(os.environ.get("ZTRAP_WS_PORT", "8765"))

# Placeholder for broadcast function; replaced if WS is enabled
def broadcast_message(msg):
    # default no-op to keep code testable when websockets aren't installed
    return


def is_nuclei_installed():
    """Check if nuclei is in the system PATH."""
    return shutil.which("nuclei") is not None


def install_nuclei():
    """Attempts to install Nuclei via Go and update templates.

    Returns True on success, False on failure.
    This function writes status to the Streamlit UI.
    """
    try:
        st.warning("⚙️ Nuclei not found. Starting automated installation...")
        # Step 1: Install via Go
        subprocess.run([
            "go",
            "install",
            "-v",
            "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        ], check=True)
        # Step 2: Update templates
        subprocess.run(["nuclei", "-ut"], check=True)
        st.success("✅ Nuclei and Templates installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Installation failed (subprocess error). Please ensure 'Go' is installed and configured correctly. Error: {e}")
        return False
    except FileNotFoundError as e:
        st.error(f"❌ Installation failed: 'go' not found. Install Go on your system and ensure it's on PATH. Error: {e}")
        return False
    except Exception as e:
        st.error(f"❌ Installation failed: {e}")
        return False


# -------------------------
# Scan registry / cooldown
# -------------------------

import sqlite3


def _init_db(db_path=None):
    db = db_path or NUCLEI_DB_PATH
    conn = sqlite3.connect(db)
    try:
        with conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT NOT NULL,
                    ts REAL NOT NULL
                )"""
            )
    finally:
        conn.close()


def _get_conn(db_path=None):
    db = db_path or NUCLEI_DB_PATH
    _init_db(db)
    return sqlite3.connect(db)


def check_cooldown(target, cooldown_seconds=60, max_per_hour=3, db_path=None):
    """Return (allowed: bool, reason: str)"""
    now = time.time()
    conn = _get_conn(db_path)
    try:
        cur = conn.cursor()
        # Remove very old rows (older than 24h) to keep DB small
        cutoff = now - 86400
        cur.execute("DELETE FROM scans WHERE ts < ?", (cutoff,))
        conn.commit()

        # Count occurrences in last hour for this target
        hour_ago = now - 3600
        cur.execute("SELECT count(*) FROM scans WHERE target=? AND ts>=?", (target, hour_ago))
        recent_count = cur.fetchone()[0]
        if recent_count >= max_per_hour:
            return False, f"Rate limit exceeded for target (max {max_per_hour} per hour)."

        # Check last scan overall
        cur.execute("SELECT ts FROM scans ORDER BY ts DESC LIMIT 1")
        row = cur.fetchone()
        if row and (now - row[0] < cooldown_seconds):
            return False, f"Cooldown active (wait {int(cooldown_seconds - (now - row[0]))}s)."

        return True, "OK"
    finally:
        conn.close()


def record_scan(target, db_path=None):
    conn = _get_conn(db_path)
    try:
        with conn:
            conn.execute("INSERT INTO scans (target, ts) VALUES (?, ?)", (target, time.time()))
    finally:
        conn.close()


# -------------------------
# Async scan runner
# -------------------------

def _scan_worker(scan_id, target, severity_list):
    """Internal worker. Will simulate if ZTRAP_FAKE_NUCLEI=1 is set in env."""
    # Simulation mode: write predictable logs for integration testing without real tooling
    if os.environ.get("ZTRAP_FAKE_NUCLEI", "0") == "1":
        logfile = os.path.join(LOG_DIR, f"{scan_id}.log")
        statusfile = os.path.join(LOG_DIR, f"{scan_id}.status")
        try:
            with open(logfile, "w") as lf:
                for i in range(5):
                    line = f"[SIM] finding {i} on {target}\n"
                    lf.write(line)
                    lf.flush()
                    broadcast_message(json.dumps({"scan_id": scan_id, "line": line}))
                    time.sleep(0.05)
            with open(statusfile, "w") as sf:
                json.dump({"returncode": 0, "finished": True, "ts": time.time()}, sf)
        except Exception as e:
            with open(logfile, "a") as lf:
                lf.write(f"Simulation failed: {e}\n")
            with open(statusfile, "w") as sf:
                json.dump({"returncode": -2, "finished": True, "error": str(e), "ts": time.time()}, sf)
        return

    severity = ",".join(severity_list) if isinstance(severity_list, (list, tuple)) else str(severity_list)
    cmd = ["nuclei", "-u", target, "-s", severity, "-nc"]
    logfile = os.path.join(LOG_DIR, f"{scan_id}.log")
    statusfile = os.path.join(LOG_DIR, f"{scan_id}.status")

    try:
        with open(logfile, "w") as lf:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in iter(proc.stdout.readline, ''):
                if line is None:
                    break
                lf.write(line)
                lf.flush()
                # broadcast to WebSocket clients if enabled (include scan_id so clients can filter)
                try:
                    broadcast_message(json.dumps({"scan_id": scan_id, "line": line}))
                except Exception:
                    pass
            proc.wait()
            with open(statusfile, "w") as sf:
                json.dump({"returncode": proc.returncode, "finished": True, "ts": time.time()}, sf)
    except FileNotFoundError:
        with open(logfile, "a") as lf:
            lf.write("`nuclei` binary not found. Please install Nuclei first.\n")
        with open(statusfile, "w") as sf:
            json.dump({"returncode": -1, "finished": True, "ts": time.time()}, sf)
    except Exception as e:
        with open(logfile, "a") as lf:
            lf.write(f"Scan failed: {e}\n")
        with open(statusfile, "w") as sf:
            json.dump({"returncode": -2, "finished": True, "error": str(e), "ts": time.time()}, sf)


def run_scan_async(target, severity_list):
    """Start a scan asynchronously and return a scan_id string."""
    allowed, reason = check_cooldown(target)
    if not allowed:
        st.error(reason)
        return None

    record_scan(target)
    scan_id = f"scan_{int(time.time())}"
    t = threading.Thread(target=_scan_worker, args=(scan_id, target, severity_list), daemon=True)
    t.start()
    return scan_id


def get_scan_log(scan_id, tail_lines=None):
    logfile = os.path.join(LOG_DIR, f"{scan_id}.log")
    if not os.path.exists(logfile):
        return ""
    if tail_lines is None:
        with open(logfile, "r") as f:
            return f.read()
    else:
        with open(logfile, "r") as f:
            lines = f.readlines()
            return "".join(lines[-tail_lines:])


def get_scan_status(scan_id):
    statusfile = os.path.join(LOG_DIR, f"{scan_id}.status")
    if not os.path.exists(statusfile):
        return {"finished": False}
    try:
        with open(statusfile, "r") as f:
            return json.load(f)
    except Exception:
        return {"finished": False, "error": "invalid status file"}


# Backwards compatible synchronous runner

def run_scan(target, severity_list):
    """Runs a scan synchronously (blocks). Kept for compatibility."""
    scan_id = f"sync_{int(time.time())}"
    _scan_worker(scan_id, target, severity_list)
    return scan_id


# -------------------------
# Optional WebSocket server
# -------------------------
if WS_ENABLED:
    try:
        import asyncio
        import websockets

        _ws_clients = set()

        async def _ws_handler(websocket, path):
            _ws_clients.add(websocket)
            try:
                # Keep connection alive until client disconnects
                await websocket.wait_closed()
            finally:
                _ws_clients.discard(websocket)

        async def _broadcast(msg):
            if not _ws_clients:
                return
            await asyncio.gather(*[ws.send(msg) for ws in list(_ws_clients)])

        def broadcast_message(msg):
            # schedule broadcast in the event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            try:
                asyncio.run_coroutine_threadsafe(_broadcast(msg), loop)
            except Exception:
                # if loop not running in this thread, start a loop in background
                def _start_loop():
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    start_server = websockets.serve(_ws_handler, WS_HOST, WS_PORT)
                    new_loop.run_until_complete(start_server)
                    new_loop.run_forever()

                t = threading.Thread(target=_start_loop, daemon=True)
                t.start()
                # once started, attempt broadcast again
                try:
                    asyncio.run_coroutine_threadsafe(_broadcast(msg), asyncio.get_event_loop())
                except Exception:
                    pass

        # Start the server in a background thread if not already running
        def _start_ws_server():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            start_server = websockets.serve(_ws_handler, WS_HOST, WS_PORT)
            loop.run_until_complete(start_server)
            loop.run_forever()

        ws_thread = threading.Thread(target=_start_ws_server, daemon=True)
        ws_thread.start()
    except Exception:
        # If websockets library is not available or fails to start, disable WS
        WS_ENABLED = False
        def broadcast_message(msg):
            return

