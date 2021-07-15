import signal

import uvicorn

import effect_service
import effect_picker

import config
from logger import logger

from config import app


def stop_effect_service_event(sig, frame):
    logger.debug("Shutting down effects service")
    effect_service.stop()


@app.on_event("startup")
async def startup():
    signal.signal(signal.SIGINT, stop_effect_service_event)


@app.get("/ping")
def ping():
    return {"status": "Ok"}


@app.get("/service")
def get_service():
    return {"effect_service": effect_service.get_status()}


@app.post("/service")
def start_service():
    return {"effect_service": effect_service.start()}


@app.delete("/service")
def stop_service():
    return {"effect_service": effect_service.stop()}


@app.get("/effect")
async def list_effects():
    return {"effects": effect_picker.list_effects()}


@app.get("/cache")
async def set_cache():
    """get cache value"""
    return {"cache": effect_picker.get_cache()}


@app.post("/cache")
async def set_cache(cache: int = 0):
    """enable disable cache, if 0 , cache is disabled."""
    return {"cache": effect_picker.set_cache(cache)}


@app.post("/effect/{effect_name}")
async def set_effect(effect_name: str):
    return {"effects": effect_picker.set_effect(effect_name)}


@app.delete("/effect")
async def unset_effect():
    effect_picker.unset_effect()
    return {"effects": ""}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.API_PORT)
