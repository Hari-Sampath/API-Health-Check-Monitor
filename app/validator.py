def validate(responses, api_info):
    report = []
    for api in api_info:
        expected = api["expected"]

        expected_time = expected["response_time_ms"]
        expected_status = expected["status"]

        for response in responses:
            if response["time"] > expected_time:
                speed = "slower than expected"
            else:
                speed = "healthy"
            if expected_status == response["response_code"]:
                health = "Healthy"
            else:
                health = "Faulty"
            valid = 1
            report.append({"health": health, "speed": speed, "valid": valid})

    return report
