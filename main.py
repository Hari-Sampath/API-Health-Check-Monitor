from config.loader import load_config
from network import call_api


def main():
    config = load_config("apis.yaml")

    print("Project:", config.project.get("name"))
    print("Total APIs:", len(config.apis))

    for api in config.apis:
        result = call_api(api, config.settings)

        print("\n----------------------------")
        print("API:", api.name)
        print("URL:", api.url)
        print("Response Code:", result["response_code"])
        print("Time Taken:", result["time_taken"], "ms")
        print("Error:", result["error"])


if __name__ == "__main__":
    main()
    