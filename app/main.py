import pathlib
from typing import Optional

import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

templates = Jinja2Templates(directory="static")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
favicon_path = "favicon.ico"


@app.get("/")
def get_home():
    return


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/dashboard")
def baby_dasshboard():
    return

