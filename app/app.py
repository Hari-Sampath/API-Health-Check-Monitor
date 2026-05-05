from flask import Flask, jsonify, render_template
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


if __name__ == "__main__":
    app.run(debug=True)
