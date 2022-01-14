import pathlib

from fastapi import FastAPI, Request
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
from app.plot_util import plot_feeding, plot_head, plot_height, plot_weight, plot_wh

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
favicon_path = PROJECT_PATH / "static/favicon.png"


@app.get("/")
def get_home():
    return


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/weight_test")
def baby_weight():
    weight_json = get_weight()
    plot_weight(weight_json)
    return weight_json


@app.get("/height_test")
def baby_height():
    height_json = get_height()
    plot_height(height_json)
    return height_json


@app.get("/head_test")
def baby_head():
    head_json = get_head()
    plot_head(head_json)
    return head_json


@app.get("/wh_test")
def baby_wh():
    weight_json = get_weight()
    height_json = get_height()
    plot_wh(weight_json, height_json)
    return


@app.get("/feeding_test")
def baby_feeding():
    feeding_json = get_feeding()
    weight_json = get_weight()
    plot_feeding(feeding_json, weight_json)
    return


@app.get("/dashboard")
def baby_dashboard(request: Request):
    weight_json = get_weight()
    plot_weight(weight_json)
    height_json = get_height()
    plot_height(height_json)
    head_json = get_head()
    plot_head(head_json)
    plot_wh(weight_json, height_json)
    last_update_date = get_last_date()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "last_update_date": last_update_date}
    )

