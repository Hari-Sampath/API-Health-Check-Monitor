import time

import alerts
import network
import storage
import validator
import yaml

CHECK_INTERVAL_MINUTES = 60
CHECK_INTERVAL_SECONDS = CHECK_INTERVAL_MINUTES * 60


def run_monitor():
    with open("apis.yaml", "r") as yaml_data:
        yaml_file = yaml.safe_load(yaml_data)

    global_settings = yaml_file["settings"]
    api_info = yaml_file["apis"]

    responses = network.get_status(api_info, global_settings)
    report = validator.validate(responses, api_info)
    alerts_list = alerts.generate_alerts(report)

    return report, alerts_list


def main():
    report, alerts_list = run_monitor()
    storage.save_logs(report, alerts_list)
    return report, alerts_list


def run_scheduler():
    print(f"[Scheduler] Starting — checks every {CHECK_INTERVAL_MINUTES} minute(s).")
    while True:
        try:
            print(f"[Scheduler] Running check at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            report, alerts_list = main()
            ok_count = sum(
                1
                for r in report
                if "healthy" in str(r.get("health", "")).lower()
                or str(r.get("health", "")) == "200"
            )
            print(
                f"[Scheduler] Done — {len(report)} APIs checked, "
                f"{ok_count} healthy, {len(alerts_list)} alert(s)."
            )
        except Exception as exc:
            print(f"[Scheduler] ERROR during check: {exc}")

        print(
            f"[Scheduler] Next check in {CHECK_INTERVAL_MINUTES} minute(s) "
            f"(at {time.strftime('%H:%M:%S', time.localtime(time.time() + CHECK_INTERVAL_SECONDS))})."
        )
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    import sys

    if "--scheduler" in sys.argv:
        run_scheduler()
    else:
        main()
