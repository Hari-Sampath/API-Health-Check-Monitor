def validate(responses, api_info):

    report = []

    for response in responses:
        # find matching API config
        api = next((a for a in api_info if a["name"] == response["api_name"]), None)

        if not api:
            continue

        expected = api["expected"]

        expected_time = expected["response_time_ms"]
        expected_contains = expected.get("response_contains")

        # Speed
        speed = (
            "Slower than expected"
            if response["time"] > expected_time
            else "Expected speed"
        )

        # Health
        if response["response_code"] == "ERROR":
            health = "Faulty"
        elif 200 <= response["response_code"] < 300:
            health = "Healthy"
        else:
            health = "Faulty"

        # Valid
        output = response.get("output", "")

        if not expected_contains:
            valid = "No validation rules"
        else:
            if isinstance(output, dict):
                valid = (
                    "Accurate response provided"
                    if expected_contains in output
                    else "Inaccurate response provided"
                )
            elif isinstance(output, str):
                valid = (
                    "Accurate response provided"
                    if expected_contains.lower() in output.lower()
                    else "Inaccurate response provided"
                )
            else:
                valid = "Inaccurate response provided"

        report.append(
            {
                "Name": response["api_name"],
                "health": health,
                "speed": speed,
                "valid": valid,
            }
        )

    return report
