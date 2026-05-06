import csv
import os


def save_logs(report_list, alerts_list):

    log_dir = "logs"

    os.makedirs(log_dir, exist_ok=True)

    f1 = os.path.join(log_dir, "reports.csv")
    f2 = os.path.join(log_dir, "alerts.csv")

    if report_list:
        file_exists = os.path.isfile(f1)

        with open(f1, mode="a", newline="", encoding="utf-8") as file:
            headers = report_list[0].keys()
            writer = csv.DictWriter(file, fieldnames=headers)

            if not file_exists:
                writer.writeheader()

            writer.writerows(report_list)
            print(f"  -> Saved {len(report_list)} reports to {f1}")

    if alerts_list:
        file_exists = os.path.isfile(f2)

        with open(f2, mode="a", newline="", encoding="utf-8") as file:
            headers = alerts_list[0].keys()
            writer = csv.DictWriter(file, fieldnames=headers)

            if not file_exists:
                writer.writeheader()

            writer.writerows(alerts_list)
            print(f"  -> Saved {len(alerts_list)} alerts to {f2}")
