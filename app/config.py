import yaml

json_data = open("apis.yaml", "r")
yaml_file = yaml.safe_load(json_data)

global_settings = yaml_file["settings"]  # global settings
api_info = yaml_file["apis"]  # list with information of apis


def get_api_detail(api_name, detail):
    for api in api_info:
        if api["name"] == api_name:
            return api[detail]


print(get_api_detail("HTTPBin GET", str(input("enter what detail you want : "))))
