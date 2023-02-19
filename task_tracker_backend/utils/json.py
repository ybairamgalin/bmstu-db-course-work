import json


def to_json(content: dict):
    return json.dumps(content, sort_keys=True, default=str)
