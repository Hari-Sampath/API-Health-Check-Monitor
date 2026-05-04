from datetime import datetime

def generate_alerts(report):
    alerts = []

    for api in report:
        issues = []
        level = None

        #  CRITICAL → SYSTEM FAILURE
        if api["health"] == "Faulty":
            issues.append("API DOWN")
            level = "CRITICAL"

        #  WARNING → PERFORMANCE ISSUE
        elif "Slower" in api["speed"]:
            issues.append("SLOW")
            level = "WARNING"

        # ℹ INFO → DATA ISSUE
        if api["valid"] == "Inaccurate response provided":
            issues.append("BAD DATA")
            if not level:
                level = "INFO"

        if issues:
            alerts.append({
                "level": level,
                "api": api["Name"],
                "message": ", ".join(issues),
                "timestamp": datetime.now().isoformat()
            })

    return alerts