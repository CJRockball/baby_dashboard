import requests


def get_weight():
    w_json = requests.get("http://127.0.0.1:8000/weight")
    return w_json.json()

