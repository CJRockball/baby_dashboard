import pathlib
import asyncio
from fastapi import FastAPI, Request, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

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
from os import path
import logging

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
TEMP_PATH = PROJECT_PATH / "templates"
STAT_PATH = PROJECT_PATH / "static"
templates = Jinja2Templates(directory=TEMP_PATH)
favicon_path = PROJECT_PATH / "static/favicon.png"

dash = APIRouter()

#path_str = path.dirname(path.realpath(__file__))
#logger.info("relative path of static folder: %s", path_str)
#dash.mount("/static", StaticFiles(directory="static"), name="static")
#print("static path:", STAT_PATH)

@dash.get("/")
def get_home():
    return


@dash.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@dash.get("/weight_test")
async def baby_weight():
    weight_json = get_weight()
    if weight_json.status_code == 200:
        plot_weight(weight_json.json())
        return weight_json.json()
    else:
        raise HTTPException(status_code=weight_json.status_code, detail="Weight data not found")



@dash.get("/height_test")
async def baby_height():
    height_json = get_height()
    if height_json.status_code == 200:
        plot_height(height_json.json())
        return height_json.json()
    else:
        raise HTTPException(status_code=height_json.status_code, detail="Height data not found")


@dash.get("/head_test")
async def baby_head():
    head_json = get_head()
    if head_json.status_code == 200:
        plot_head(head_json.json())
        return head_json.json()
    else:
        raise HTTPException(status_code=head_json.status_code, detail="Head data not found")



@dash.get("/wh_test")
async def baby_wh():
    weight_json = get_weight()
    if weight_json.status_code == 200:
        height_json = get_height()
        if height_json.status_code == 200:
            plot_wh(weight_json.json(), height_json.json())
            return
        else:
            raise HTTPException(status_code=height_json.status_code, detail="Height data not found")
    else:
        raise HTTPException(status_code=weight_json.status_code, detail="Weight data not found")



@dash.get("/feeding_test")
async def baby_feeding():
    feeding_json = get_feeding()
    weight_json = get_weight()
    if feeding_json.status_code == 200:
        weight_json = get_weight()
        if weight_json.status_code == 200:
            plot_feeding(feeding_json.json(), weight_json.json())
            return feeding_json.json()
        else:
            raise HTTPException(status_code=weight_json.status_code, detail="Weight data not found")
    else:
        raise HTTPException(status_code=feeding_json.status_code, detail="Feeding data not found")



@dash.get("/prop_test")
async def prop_feeding():
    feeding_json = get_feeding()
    if feeding_json.status_code == 200:
        plot_prop(feeding_json.json())
        return
    else:
        raise HTTPException(status_code=feeding_json.status_code, detail="Feeding data not found")


@dash.get("/dashboard")
def baby_dashboard(request: Request, response_class=HTMLResponse):
    weight_json = get_weight()
    height_json = get_height()
    head_json = get_head()
    feeding_json = get_feeding()
    
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
    
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "last_update_date": last_update_date}
    )

