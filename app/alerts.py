from datetime import datetime


def generate_alerts(report):
    alerts = []

    for api in report:
        issues = []
        level = None

        #  CRITICAL → SYSTEM FAILURE
        if api["Health"] == "Faulty":
            issues.append("API DOWN")
            level = "CRITICAL"

        #  WARNING → PERFORMANCE ISSUE
        elif "Slower" in api["Speed"]:
            issues.append("SLOW")
            level = "WARNING"

        # ℹ INFO → DATA ISSUE
        if api["Validity"] == "Inaccurate response provided":
            issues.append("BAD DATA")
            if not level:
                level = "INFO"

        if issues:
            alerts.append(
                {
                    "Level": level,
                    "Api": api["Name"],
                    "Message": ", ".join(issues),
                    "Timestamp": datetime.now().isoformat(),
                }
            )

    return alerts
