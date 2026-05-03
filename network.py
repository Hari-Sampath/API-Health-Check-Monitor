import requests
import time


def call_api(api, settings):
    timeout = settings.get("timeout", 5)
    retries = settings.get("retries", 0)
    retry_delay = settings.get("retry_delay", 1)

    attempt = 0
    last_error = None

    while attempt <= retries:
        try:
            start_time = time.time()

            response = requests.request(
                method=api.method,
                url=api.url,
                headers=api.headers,
                params=api.params,
                json=api.body,
                timeout=timeout
            )

            end_time = time.time()

            response_code = response.status_code
            time_taken = int((end_time - start_time) * 1000)  # milliseconds
            output = response.text

            return {
                "response_code": response_code,
                "time_taken": time_taken,
                "output": output,
                "error": None
            }

        except Exception as e:
            last_error = str(e)
            attempt += 1

            if attempt <= retries:
                time.sleep(retry_delay)

    return {
        "response_code": None,
        "time_taken": None,
        "output": None,
        "error": last_error
    }