import yaml
from alerts import generate_alerts
from network import get_status
from validator import validate


def main():

    # Load configuration
    with open("apis.yaml", "r", encoding="utf-8") as yaml_data:
        config = yaml.safe_load(yaml_data)

    # Extract settings and API list
    global_settings = config["settings"]
    api_info = config["apis"]

    # Process APIs
    responses = get_status(api_info, global_settings)
    report = validate(responses, api_info)
    issues = generate_alerts(report)

    print(report[0])
    print(report[1])
    print(report[2])
    print(issues[0])
    print(issues[1])
    print(issues[2])


if __name__ == "__main__":
    main()
