from fastapi import FastAPI
from app import main
from fastapi.staticfiles import StaticFiles
import pathlib

PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
TEMP_PATH = PROJECT_PATH / "templates"
STAT_PATH = PROJECT_PATH / "static"


app = FastAPI()
app.mount("/static", StaticFiles(directory=STAT_PATH), name="static")
app.include_router(main.dash, prefix='/api/v1/dash', tags=['dash'])
