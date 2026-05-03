import time

import requests
import yaml

with open("apis.yaml", "r") as yaml_data:
    yaml_file = yaml.safe_load(yaml_data)

global_settings = yaml_file["settings"]  # global settings
api_config = yaml_file["apis"]  # list with information of apis

i = 0


def get_status(api_config, global_settings):
    for api in api_config:
        url = api["url"]
        method = api["method"]
        header = api["headers"]
        params = api["params"]
        body = api["body"]

        timeout = global_settings["timeout"]
        retries = global_settings["retries"]
        retry_delay = global_settings["retry_delay"]
        default_method = global_settings["default_method"]

        result = []

        for attempt in range(retries + 1):

            start_time = time.time()  # starting the stop watch

            try:
                output = requests.get(url)

            result.append(
                {"response_time": start_time, "response_code": code, "output": output}
            )


get_status(api_config, global_settings)
