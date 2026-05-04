def validate(responses, api_info):

    report = []
    expected_time = []
    expected_status = []
    response_contains = []
    j = 0

    for api in api_info:
        expected = api["expected"]

        expected_time.append(expected["response_time_ms"])
        expected_status.append(expected["status"])
        if "response_contains" in expected:
            response_contains.append(expected["response_contains"])
        else:
            response_contains.append("No params")

    for response in responses:
        if response["time"] > expected_time[j]:
            speed = "Slower than expected"
        else:
            speed = "Expected speed"

        if expected_status[j] == response["response_code"]:
            health = "Healthy"
        else:
            health = "Faulty"

        if response_contains[j] == "No params":
            valid = "Accurate response provided"
        elif response_contains[j] in response["output"]:
            valid = "Accurate response provided"
        else:
            valid = "Inaccurate response provided"

        report.append(
            {
                "Name": response["api_name"],
                "Health": health,
                "Speed": speed,
                "Validity": valid,
            }
        )
    j += 1

    return report
