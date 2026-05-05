import yaml
from alerts import generate_alerts
from network import get_status
from validator import validate


def main():

    with open("apis.yaml", "r") as yaml_data:
        yaml_file = yaml.safe_load(yaml_data)

    global_settings = yaml_file["settings"]  # global settings
    api_info = yaml_file["apis"]  # list with information of apis

    responses = get_status(api_info, global_settings)  # sending api request and fetching response # fmt: skip
    report = validate(responses, api_info)  # checking validity of response
    issues = generate_alerts(report)
    print(issues)


if __name__ == "__main__":
    main()
