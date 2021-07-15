import signal
from fastapi import Query
import uvicorn
from pydantic import BaseModel
from typing import Optional

import video_service
import video_settings

import config
from logger import logger

from config import app


class VideoSource(BaseModel):
    source: str
    pix_fmt: Optional[str] = None
    res: Optional[str] = None

def stop_video_service_event(sig, frame):
    logger.debug("Shutting down video proxy service")
    video_service.stop()


@app.on_event("startup")
async def startup():
    signal.signal(signal.SIGINT, stop_video_service_event)


@app.get("/ping")
def ping():
    return {"status": "Ok"}


@app.get("/service")
def get_service():
    return {"video_service": video_service.get_status()}


@app.post("/service")
def start_service():
    return {"video_service": video_service.start()}


@app.delete("/service")
def stop_service():
    return {"video_service": video_service.stop()}


@app.get("/stream_type")
async def get_direction():
    return {"stream_type": video_settings.get_stream_direction()}


@app.post("/video_source")
async def set_video_source(video_source: VideoSource):
    return {"video_source": video_settings.set_source(video_source.dict())}


@app.delete("/video_source")
async def unset_video_source():
    video_settings.unset_source()
    return {"video_source": ""}


@app.get("/video_source")
async def get_video_source():
    return {"video_source": video_settings.get_current_source()}


@app.post("/virtual_device/{virtual_device}")
async def set_virtual_device(virtual_device: int):
    return {"virtual_device": video_settings.set_virtual_device(virtual_device)}


@app.get("/virtual_device")
async def get_virtual_device():
    return {"virtual_device": video_settings.get_current_virtual_device()}


@app.delete("/virtual_device")
async def unset_virtual_device():
    video_settings.unset_virtual_device()
    return {"virtual_device": ""}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.API_PORT)
