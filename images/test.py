import json
from screenshot_utils import screenshot_dimensions

with open("dictionary.json", 'r') as json_file:
    data = json.load(json_file)

for entry in data:
    name = entry
    print(name + screenshot_dimensions(name, (9, 9)))