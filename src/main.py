from datetime import datetime
from functools import lru_cache

import googlemaps
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles
from googlemaps.directions import directions
from polyline import polyline
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    G_API_KEY: SecretStr


s = Settings()

gmaps = googlemaps.Client(key=s.G_API_KEY.get_secret_value())


# Dummy datastore
items = ["Item 1", "Item 2"]

points = []


@lru_cache
def get_from_to(o, d):
    directions_result = directions(gmaps, o,
                                   d,
                                   mode="driving",
                                   departure_time=datetime.now())

    return polyline.decode(directions_result[0]["overview_polyline"]["points"])


@app.get("/poly")
def get_polyline():
    result = []
    for s, d in zip(points[:-1], points[1:]):
        result.append(get_from_to(s, d))

    return result


@app.get("/", response_class=HTMLResponse)
def get_items(request: Request):
    return templates.TemplateResponse("items.html", {"request": request, "items": items})


@app.post("/add-item")
def add_item(request: Request, item: str = Form(...)):
    items.append(item)
    return templates.TemplateResponse("partials/item.html", {"request": request, "item": item})


@app.get("/click")
def get_items(lat: float, lon: float):

    points.append((lat, lon))

    if len(points) < 2:
        return []

    return get_from_to(points[-2], points[-1])
