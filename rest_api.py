"""Simple Flask REST API to expose Nuclei scan metadata and logs.

This service is optional and starts only when ZTRAP_ENABLE_REST=1.
It reads the same DB and LOG_DIR used by `nuclei_engine`.
"""
import os
import threading
from flask import Flask, jsonify, send_file, request, abort

import nuclei_engine

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


def _check_auth():
    token = os.environ.get("ZTRAP_REST_TOKEN")
    if not token:
        return True
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer ") and auth.split(None, 1)[1] == token:
        return True
    return False


@app.route("/scans")
def list_scans():
    if not _check_auth():
        return jsonify({"error": "unauthorized"}), 401
    # Optional query params: target
    target = request.args.get("target")
    conn = nuclei_engine._get_conn()
    cur = conn.cursor()
    if target:
        cur.execute("SELECT rowid, target, ts FROM scans WHERE target=? ORDER BY ts DESC", (target,))
    else:
        cur.execute("SELECT rowid, target, ts FROM scans ORDER BY ts DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"scan_id": f"scan_{r[0]}", "target": r[1], "ts": r[2]} for r in rows])


@app.route("/scans/<scan_id>/log")
def get_log(scan_id):
    if not _check_auth():
        return jsonify({"error": "unauthorized"}), 401
    # scan_id format: scan_<number> or sync_<number>
    # try to locate matching file
    logfile = None
    for p in os.listdir(nuclei_engine.LOG_DIR):
        if p.startswith(scan_id):
            logfile = os.path.join(nuclei_engine.LOG_DIR, p)
            break
    if not logfile or not os.path.exists(logfile):
        abort(404)
    return send_file(logfile, as_attachment=False, mimetype="text/plain")


@app.route("/scans/<scan_id>/status")
def get_status(scan_id):
    statusfile = os.path.join(nuclei_engine.LOG_DIR, f"{scan_id}.status")
    if not os.path.exists(statusfile):
        return jsonify({"finished": False})
    try:
        import json
        with open(statusfile, "r") as f:
            return jsonify(json.load(f))
    except Exception:
        return jsonify({"finished": False, "error": "invalid status file"})


def _start_rest_server():
    # Bind to localhost only
    host = os.environ.get("ZTRAP_REST_HOST", "127.0.0.1")
    port = int(os.environ.get("ZTRAP_REST_PORT", "8766"))
    app.run(host=host, port=port, threaded=True)


# If enabled, start on import in a background daemon thread
if os.environ.get("ZTRAP_ENABLE_REST", "0") == "1":
    t = threading.Thread(target=_start_rest_server, daemon=True)
    t.start()
