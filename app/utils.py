import requests
from config.config_utils import load_config

config = load_config("config_file.yaml")
url = config['data_mod']
#url = "http://baby-j-data-service.herokuapp.com/api/v1/datas/" #  "http://127.0.0.1:8000/api/v1/datas/" # "http://baby-j-data-service.herokuapp.com/api/v1/datas/" # "http://data_service:8000/api/v1/datas/" #


def update_head_fcn(week, head):
    global url      
    requests.post(url+"head_update/", params={'week':week, "head":head})
    return

def update_weight_fcn(date_w, week_w, weight, height):
    global url      
    requests.post(url+"wnh_update/", params={"date":date_w, 'week':week_w, "weight":weight, "height":height})
    return

def update_feeding_fcn(date_f, time, bm_vol, formula_vol):
    global url      
    requests.post(url+"feeding_update/", params={'date':date_f, 'time':time, 'bm_vol':bm_vol, 'formula_vol':formula_vol})
    return


