import os
import json
from datetime import datetime

LOG_FILE = "access_logs.json"


def log_attempt(status, details=""):
    """Records unauthorized access attempts for intelligence gathering."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "details": details,
        "ip_hint": "Logged via Streamlit Context",
    }

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r+") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except Exception:
                    data = []
                data.append(log_entry)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        else:
            with open(LOG_FILE, "w") as f:
                json.dump([log_entry], f, indent=2)
    except Exception as e:
        # Keep logging failures non-fatal and visible during development
        print(f"Logging error: {e}")
