import json


def load_config():
    with open("AJ_MAS/config.json", "r") as f:
        return json.load(f)


config = load_config()
