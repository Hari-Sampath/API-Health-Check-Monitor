import time

import requests

result = []


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

        for attempt in range(retries + 1):
            start_time = time.time()  # starting the stop watch

            try:
                response = requests.request(method=method, url=url, timeout=timeout)

                elapsed_time = round((time.time() - start_time) * 1000)
                print(f"Success, took {elapsed_time}ms")

                result.append(
                    {
                        "api_name": api["name"],
                        "response_code": response.status_code,
                        "time": elapsed_time,
                    }
                )
                break

            except requests.exceptions.RequestException as e:
                if attempt < retries:
                    print(f"  Failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("  Completely failed after retries.")
                    result.append(
                        {
                            "api_name": api["name"],
                            "response_code": "ERROR",
                            "time": 0,
                        }
                    )

    return result
