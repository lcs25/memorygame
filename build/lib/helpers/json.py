import json

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError as error:
        print(error)
        return {}
    except json.JSONDecodeError as error:
        print(error)
        return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)
