import network
import storage
import validator
import yaml
import alerts


def print_report(report):
    print("\nAPI HEALTH REPORT")
    print("-" * 90)
    print(f"{'API Name':30} | {'Health':10} | {'Speed':20} | {'Validation'}")
    print("-" * 90)

    for api in report:
        print(f"{api['Name']:30} | {api['health']:10} | {api['speed']:20} | {api['valid']}")

    print("-" * 90)


def print_summary(report):
    total = len(report)
    healthy = sum(1 for r in report if r["health"] == "Healthy")
    faulty = total - healthy
    slow = sum(1 for r in report if "Slower" in r["speed"])

    print("\nSUMMARY")
    print("-" * 40)
    print(f"Total APIs   : {total}")
    print(f"Healthy      : {healthy}")
    print(f"Faulty       : {faulty}")
    print(f"Slow APIs    : {slow}")
    print("-" * 40)


def print_alerts(alerts_list):
    print("\nALERTS")
    print("-" * 40)

    if not alerts_list:
        print("No alerts 🚀")
    else:
        for alert in alerts_list:
            print(alert)

    print("-" * 40)


def main():
    with open("apis.yaml", "r") as yaml_data:
        yaml_file = yaml.safe_load(yaml_data)

    global_settings = yaml_file["settings"]
    api_info = yaml_file["apis"]

    responses = network.get_status(api_info, global_settings)

    report = validator.validate(responses, api_info)
    alerts_list = alerts.generate_alerts(report)

    # structured output
    print_report(report)
    print_summary(report)
    print_alerts(alerts_list)


if __name__ == "__main__":
    main()