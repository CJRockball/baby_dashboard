import pathlib
from fastapi import Request, APIRouter, HTTPException, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse, RedirectResponse, HTMLResponse
from typing import Optional
import requests
from app.data_handler import (
    get_feeding,
    get_head,
    get_height,
    get_last_date,
    get_weight,
)
from app.plot_util import (
    plot_feeding,
    plot_head,
    plot_height,
    plot_prop,
    plot_weight,
    plot_wh,
)
from app.utils import update_head_fcn, update_weight_fcn, update_feeding_fcn
from os import path
import logging
import starlette.status as status

PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
TEMP_PATH = PROJECT_PATH / "templates"
STAT_PATH = PROJECT_PATH / "static"
templates = Jinja2Templates(directory=TEMP_PATH)
favicon_path = PROJECT_PATH / "static/favicon.png"

dash = APIRouter()

LOG_FILE = PROJECT_PATH / "logs/info.log"
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
)

@dash.get("/")
def get_home():
    return


@dash.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@dash.get("/weight_test")
async def baby_weight():
    weight_json = await get_weight()
    if weight_json.status_code == 200:
        plot_weight(weight_json.json())
        return weight_json.json()
    else:
        raise HTTPException(status_code=weight_json.status_code, detail="Weight data not found")



@dash.get("/height_test")
async def baby_height():
    height_json = await get_height()
    if height_json.status_code == 200:
        plot_height(height_json.json())
        return height_json.json()
    else:
        raise HTTPException(status_code=height_json.status_code, detail="Height data not found")


@dash.get("/head_test")
async def baby_head():
    head_json = await get_head()
    if head_json.status_code == 200:
        plot_head(head_json.json())
        return head_json.json()
    else:
        raise HTTPException(status_code=head_json.status_code, detail="Head data not found")



@dash.get("/wh_test")
async def baby_wh():
    weight_json = await get_weight()
    if weight_json.status_code == 200:
        height_json = await get_height()
        if height_json.status_code == 200:
            plot_wh(weight_json.json(), height_json.json())
            return
        else:
            raise HTTPException(status_code=height_json.status_code, detail="Height data not found")
    else:
        raise HTTPException(status_code=weight_json.status_code, detail="Weight data not found")



@dash.get("/feeding_test")
async def baby_feeding():
    feeding_json = await get_feeding()
    weight_json = get_weight()
    if feeding_json.status_code == 200:
        weight_json = await get_weight()
        if weight_json.status_code == 200:
            plot_feeding(feeding_json.json(), weight_json.json())
            return feeding_json.json()
        else:
            raise HTTPException(status_code=weight_json.status_code, detail="Weight data not found")
    else:
        raise HTTPException(status_code=feeding_json.status_code, detail="Feeding data not found")



@dash.get("/prop_test")
async def prop_feeding():
    feeding_json = await get_feeding()
    if feeding_json.status_code == 200:
        plot_prop(feeding_json.json())
        return
    else:
        raise HTTPException(status_code=feeding_json.status_code, detail="Feeding data not found")


@dash.get("/dashboard")
async def baby_dashboard(request: Request, response_class=HTMLResponse):
    weight_json = await get_weight()
    height_json = await get_height()
    head_json = await get_head()
    feeding_json = await get_feeding()
    
    if weight_json.status_code != 200:
        raise HTTPException(status_code=weight_json.status_code, detail="Weight data not found")
    if height_json.status_code != 200:
        raise HTTPException(status_code=height_json.status_code, detail="Height data not found")
    if head_json.status_code != 200:
        raise HTTPException(status_code=head_json.status_code, detail="head data not found")
    if feeding_json.status_code != 200:
        raise HTTPException(status_code=feeding_json.status_code, detail="Feeding data not found")

    plot_weight(weight_json.json())
    plot_height(height_json.json())    
    plot_head(head_json.json())
    plot_wh(weight_json.json(), height_json.json())
    plot_feeding(feeding_json.json(), weight_json.json())
    last_update_date = get_last_date()
    
    logging.info("Displaying dashboard")
    
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "last_update_date": last_update_date}
    )

@dash.get("/update_data")
def data_update_get(request: Request):
    return templates.TemplateResponse("data_update.html", {"request": request})




@dash.post("/update_data")
async def data_update_post(request: Request, 
                           week_h: Optional[float] = Form(None), 
                           head: Optional[float] = Form(None), 
                           date_w: Optional[str] = Form(None), 
                           week_w: Optional[float] = Form(None), 
                           weight: Optional[float] = Form(None), 
                           height: Optional[float] = Form(None), 
                           date_f: Optional[str] = Form(None), 
                           time: Optional[str] = Form(None), 
                           bm_vol: Optional[int] = Form(None), 
                           formula_vol: Optional[int] = Form(None), 
                           submit: str = Form(...),
                           response_class=HTMLResponse):
    
    input_text = ""
    if submit == "Update Head":
        update_head_fcn(week_h, head)
        input_text = "Head Updated in Database"
        logging.info("Updating head data")
        
    elif submit == "Update Weight":
        update_weight_fcn(date_w, week_w, weight, height)
        input_text = "Weight and Height Updated in Database"
        logging.info("Updating weight and height")
        
    elif submit == "Update Feeding":
        update_feeding_fcn(date_f, time, bm_vol, formula_vol)
        input_text = "Feeding Updated in Database"
        logging.info("Updating feeding data")
        
    elif submit == "Reset DB":
        requests.get(config['data_source']+str("reset_db")) #"http://baby-j-data-service.herokuapp.com/api/v1/datas/reset_db") #"http://127.0.0.1:8000/api/v1/datas/reset_db")
        input_text = "Reset DB"
        logging.info("Reset db")
    
    
    forw_url = f'/api/v1/dash/feedback/?input_text={input_text}' 
    
    return RedirectResponse(forw_url, status_code=status.HTTP_302_FOUND)

@dash.get('/feedback')
def feedback(request: Request, input_text: Optional[str], response_class=HTMLResponse): 
    
    return templates.TemplateResponse("feedback.html", {"request": request, "input_text":input_text})


