import network
import storage
import validator
import yaml

with open("apis.yaml", "r") as yaml_data:
    yaml_file = yaml.safe_load(yaml_data)

global_settings = yaml_file["settings"]  # global settings
api_info = yaml_file["apis"]  # list with information of apis

responses = network.get_status(
    api_info, global_settings
)  # sending api request and fetching response

report = validator.validate(responses, api_info)  # checking validity of response
