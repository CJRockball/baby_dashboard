import httpx
import requests


def get_weight():
    w_json = requests.get("http://host.docker.internal:8000/weight")
    # w_json = requests.get("http://127.0.0.1:8000/weight")
    # w_json = httpx.get("http://127.0.0.1:8000/weight")
    return w_json.json()


def get_height():
    height_json = requests.get("http://host.docker.internal:8000/height")
    # height_json = requests.get("http://localhost:8000/height")
    # height_json = httpx.get("http://127.0.0.1:8000/height")
    return height_json.json()


def get_head():
    head_json = requests.get("http://host.docker.internal:8000/head")
    # head_json = requests.get("http://127.0.0.1:8000/head")
    # head_json = httpx.get("http://127.0.0.1:8000/head")
    return head_json.json()


def get_feeding():
    feeding_json = requests.get("http://host.docker.internal:8000/feeding")
    # feeding_json = requests.get("http://127.0.0.1:8000/feeding")
    # feeding_json = httpx.get("http://127.0.0.1:8000/feeding")
    return feeding_json.json()


def get_last_date():
    feeding_json = requests.get("http://host.docker.internal:8000/feeding")
    # feeding_json = requests.get("http://127.0.0.1:8000/feeding")
    # feeding_json = httpx.get("http://127.0.0.1:8000/feeding")
    feeding_data = feeding_json.json()
    feeding_date = list(feeding_data.get("date").values())
    last_update = feeding_date[-1]
    return last_update

