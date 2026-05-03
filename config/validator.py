def validate_config(raw):
    if "apis" not in raw:
        raise Exception("Missing 'apis' section in YAML")

    for api in raw["apis"]:
        if "name" not in api:
            raise Exception("API missing 'name'")
        if "url" not in api:
            raise Exception(f"API '{api.get('name', 'unknown')}' missing 'url'")
        if "expected" not in api:
            raise Exception(f"API '{api['name']}' missing 'expected'")