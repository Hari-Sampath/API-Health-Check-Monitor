import alerts
import network
import storage
import validator
import yaml


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


if __name__ == "__main__":
    main()
