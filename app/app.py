import io
import os
import threading
import time
import zipfile

from flask import Flask, jsonify, render_template, send_file
from main import CHECK_INTERVAL_MINUTES, CHECK_INTERVAL_SECONDS, run_monitor

app = Flask(__name__)

# ── Shared scheduler state (thread-safe via lock) ────────────────────────────
_lock = threading.Lock()
_scheduler_state = {
    "last_run_ts": None,  # epoch seconds of last completed run
    "next_run_ts": None,  # epoch seconds of scheduled next run
    "last_reports": [],
    "last_issues": [],
    "run_count": 0,
    "running": False,  # True while a check is in-progress
}
# ─────────────────────────────────────────────────────────────────────────────


def _do_check():
    """Run one monitor cycle and update shared state."""
    with _lock:
        _scheduler_state["running"] = True

    try:
        reports, issues = run_monitor()
        now = time.time()
        with _lock:
            _scheduler_state["last_run_ts"] = now
            _scheduler_state["next_run_ts"] = now + CHECK_INTERVAL_SECONDS
            _scheduler_state["last_reports"] = reports
            _scheduler_state["last_issues"] = issues
            _scheduler_state["run_count"] += 1
    except Exception as exc:
        print(f"[Scheduler] ERROR: {exc}")
    finally:
        with _lock:
            _scheduler_state["running"] = False


def _scheduler_loop():
    """Background thread: run immediately, then on a fixed interval."""
    print(
        f"[Scheduler] Started — auto-checks every {CHECK_INTERVAL_MINUTES} minute(s)."
    )
    while True:
        _do_check()
        time.sleep(CHECK_INTERVAL_SECONDS)


# Start background scheduler when the Flask app boots
_bg_thread = threading.Thread(target=_scheduler_loop, daemon=True)
_bg_thread.start()


# ── Routes ────────────────────────────────────────────────────────────────────


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/run-check")
def run_check():
    """Manual on-demand check (also updates shared state)."""
    _do_check()
    with _lock:
        reports = _scheduler_state["last_reports"]
        issues = _scheduler_state["last_issues"]
    return jsonify({"reports": reports, "issues": issues})


@app.route("/scheduler-status")
def scheduler_status():
    """Lightweight endpoint polled by the dashboard every few seconds."""
    with _lock:
        state = dict(_scheduler_state)  # shallow copy is fine here
        reports = state["last_reports"]
        issues = state["last_issues"]

    now = time.time()
    next_ts = state["next_run_ts"]
    seconds_until_next = max(0, int((next_ts or 0) - now)) if next_ts else None

    return jsonify(
        {
            "running": state["running"],
            "run_count": state["run_count"],
            "last_run_ts": state["last_run_ts"],
            "next_run_ts": next_ts,
            "seconds_until_next": seconds_until_next,
            "interval_minutes": CHECK_INTERVAL_MINUTES,
            # send latest data so the dashboard can refresh without a full /run-check
            "reports": reports,
            "issues": issues,
        }
    )


@app.route("/download-logs")
def download_logs():
    log_dir = "logs"
    if not os.path.isdir(log_dir):
        return {"error": "No logs found"}, 404

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(log_dir):
            fpath = os.path.join(log_dir, fname)
            if os.path.isfile(fpath):
                zf.write(fpath, fname)
    buf.seek(0)

    return send_file(
        buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name="api_health_logs.zip",
    )


if __name__ == "__main__":
    app.run(
        debug=True, use_reloader=False
    )  # use_reloader=False prevents double thread start
