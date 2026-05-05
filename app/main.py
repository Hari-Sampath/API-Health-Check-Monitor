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

    # ✅ IMPORTANT: return data for Flask
    return report, alerts_list


# OPTIONAL: keep CLI mode working
def main():
    report, alerts_list = run_monitor()

    print("\nAPI HEALTH REPORT")
    print("-" * 90)
    print(f"{'API Name':30} | {'Health':10} | {'Speed':20} | {'Validation'}")
    print("-" * 90)

    for api in report:
        print(
            f"{api['Name']:30} | {api['health']:10} | {api['speed']:20} | {api['valid']}"
        )

    print("-" * 90)

    print("\nALERTS")
    print("-" * 40)

    if not alerts_list:
        print("No alerts 🚀")
    else:
        for alert in alerts_list:
            print(alert)

    print("-" * 40)


if __name__ == "__main__":
    main()
