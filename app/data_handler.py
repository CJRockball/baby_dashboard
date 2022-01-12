import requests


def get_weight():
    w_json = requests.get("http://127.0.0.1:8000/weight")
    return w_json.json()


def get_height():
    height_json = requests.get("http://127.0.0.1:8000/height")
    return height_json.json()


def get_head():
    head_json = requests.get("http://127.0.0.1:8000/head")
    return head_json.json()
