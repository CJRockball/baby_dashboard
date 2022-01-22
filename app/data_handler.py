import httpx
import requests
import os


CAST_SERVICE_HOST_URL = 'http://host.docker.internal:8002'
url = os.environ.get('DATA_SERVICE_HOST_URL') or CAST_SERVICE_HOST_URL
adr = "http://baby-j-data-service.herokuapp.com/api/v1/datas/" #"http://127.0.0.1:8000/api/v1/datas/" #"http://data_service:8000/api/v1/datas/" #  

def get_weight():
    # w_json = requests.get("http://host.docker.internal:8000/weight")
    #w_json = requests.get("http://127.0.0.1:8000/weight")
    w_json = httpx.get(adr + "weight")
    return w_json


def get_height():
    # height_json = requests.get("http://host.docker.internal:8000/height")
    # height_json = requests.get("http://localhost:8000/height")
    height_json = httpx.get(adr + "height")
    return height_json


def get_head():
    # head_json = requests.get("http://host.docker.internal:8000/head")
    # head_json = requests.get("http://127.0.0.1:8000/head")
    head_json = httpx.get(adr + "head")
    return head_json


def get_feeding():
    # feeding_json = requests.get("http://host.docker.internal:8000/feeding")
    # feeding_json = requests.get("http://127.0.0.1:8000/feeding")
    feeding_json = httpx.get(adr + "feeding")
    return feeding_json


def get_last_date():
    # feeding_json = requests.get("http://host.docker.internal:8000/feeding")
    # feeding_json = requests.get("http://127.0.0.1:8000/feeding")
    feeding_json = httpx.get(adr + "feeding")
    feeding_data = feeding_json.json()
    feeding_date = list(feeding_data.get("date").values())
    last_update = feeding_date[-1]
    return last_update

