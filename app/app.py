import io
import os
import zipfile

from flask import Flask, jsonify, render_template, send_file
from main import run_monitor

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/run-check")
def run_check():
    reports, issues = run_monitor()
    return jsonify(
        {
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
    app.run(debug=True)
