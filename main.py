import yaml

json_data = open("apis.yaml", "r")
yaml_file = yaml.safe_load(json_data)
api_info = yaml_file["apis"]  # list with information of apis

names = [api["name"] for api in api_info]

print(names)
