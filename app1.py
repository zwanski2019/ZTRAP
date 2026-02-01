"""app1.py

Utility helper for ZTRAP. The old file contained a top-level UI snippet which caused
syntax errors when analyzed as a standalone module. This module provides a helper
function `add_persistent_task_manager` that can be imported by `app.py` if desired.
"""

import os
import json
import subprocess
from datetime import datetime


def add_persistent_task_manager(st, default_name="pay_pal_background_scan", default_cmd="sleep 60 && echo done > /tmp/job_done.txt"):
    """Renders a persistent task manager UI within a Streamlit app.

    Parameters:
    - st: the streamlit module passed in by the caller (usually `streamlit as st`).
    - default_name: default job label
    - default_cmd: default background command
    """
    st.subheader("Persistent Task Manager")
    task_name = st.text_input("Job Label", default_name)
    bg_cmd = st.text_area("Command to Background", default_cmd)
    if st.button("DETACH & EXECUTE"):
        try:
            p = subprocess.Popen(bg_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            registry = "/tmp/ztrap_tasks.json"
            tasks = []
            if os.path.exists(registry):
                try:
                    with open(registry, "r") as f:
                        tasks = json.load(f)
                except Exception:
                    tasks = []
            tasks.append({"name": task_name, "cmd": bg_cmd, "pid": p.pid, "started": datetime.utcnow().isoformat()})
            with open(registry, "w") as f:
                json.dump(tasks, f)
            st.success(f"Job '{task_name}' started (pid: {p.pid}). Check /tmp/ztrap_tasks.json for registry.")
        except Exception as e:
            st.error(f"Failed to start job: {e}")
