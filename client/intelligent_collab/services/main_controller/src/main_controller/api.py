from typing import Optional, List

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests

import config
from logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True, connect_args={'check_same_thread': False},)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class VideoSource(BaseModel):
    source: str
    pix_fmt: Optional[str] = None
    res: Optional[str] = None

class Service(BaseModel):
    name: str
    ip: str = ""
    port: int = 8000
    alive: Optional[bool] = False

    class Config:
        orm_mode = True

class ServiceUpdate(BaseModel):
    name: str
    ip: Optional[str]
    port: Optional[int]
    alive: Optional[bool]

class DBService(Base):
    '''
    Database model to store serivices:
    id: Identifier of the record
    name: Name of the service/container
    ip: IP assigned to the container
    port: Port where the API is listening
    alive: If the container is alive
    '''
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    ip = Column(String(50))
    port = Column(Integer)
    alive = Column(Boolean)

Base.metadata.create_all(bind=engine)


def get_service(db: Session, name: str):
    return db.query(DBService).where(DBService.name == name).first()


def get_services(db: Session):
    return db.query(DBService).all()


def register_service(db: Session, service):
    db_service = DBService(**service.dict())
    service_found = db.query(DBService).where(DBService.name == db_service.name).first()
    if service_found:
        # Service already exists
        if db_service.ip:
            service_found.ip = db_service.ip
        if db_service.port:
            service_found.port = db_service.port
        if service_found.alive != db_service.alive:
            service_found.alive = db_service.alive
        db.commit()
        return db_service
    db.add(db_service)
    db.commit()
    return db_service


@app.post('/services/', response_model=Service)
def register_service_view(service: Service, db: Session = Depends(get_db)):
    db_service = register_service(db, service)
    return db_service


@app.get('/services/', response_model=List[Service])
def get_all_available_services_view(db: Session = Depends(get_db)):
    return get_services(db)


@app.get("/services/{name}")
def get_service_by_name(name: str, db: Session = Depends(get_db)):
    return get_service(db, name)


@app.get('/')
async def index():
    return {'message': 'Main controller Service'}


@app.get('/healthcheck')
async def healthcheck(db: Session = Depends(get_db)):
    status_code = 200
    status = {}
    status[config.EFFECTS_CONTAINER_NAME] = "Not Ok"
    status[config.VIDEOPROXY_CONTAINER_NAME] = "Not Ok"
    status[config.DEVICE_MNGR_CONTAINER_NAME] = "Not Ok"
    effect_svc = get_service(db, config.EFFECTS_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/ping"
        response = requests.get(url)
        if response.status_code == 200:
            status[config.EFFECTS_CONTAINER_NAME] = "Ok"
            service = ServiceUpdate(name=config.EFFECTS_CONTAINER_NAME, alive=True)
        else:
            status_code = 400
            service = ServiceUpdate(name=config.EFFECTS_CONTAINER_NAME, alive=False)
        register_service(db, service)

    video_svc = get_service(db, config.VIDEOPROXY_CONTAINER_NAME)
    if video_svc:
        url = f"http://{video_svc.ip}:{video_svc.port}/ping"
        response = requests.get(url)
        if response.status_code == 200:
            status[config.VIDEOPROXY_CONTAINER_NAME] = "Ok"
            service = ServiceUpdate(name=config.VIDEOPROXY_CONTAINER_NAME, alive=True)
        else:
            status_code = 400
            service = ServiceUpdate(name=config.VIDEOPROXY_CONTAINER_NAME, alive=False)
        register_service(db, service)

    device_svc = get_service(db, config.DEVICE_MNGR_CONTAINER_NAME)
    if device_svc:
        url = f"http://{device_svc.ip}:{device_svc.port}/ping"
        response = requests.get(url)
        if response.status_code == 200:
            status[config.DEVICE_MNGR_CONTAINER_NAME] = "Ok"
            service = ServiceUpdate(name=config.DEVICE_MNGR_CONTAINER_NAME, alive=True)
        else:
            status_code = 400
            service = ServiceUpdate(name=config.DEVICE_MNGR_CONTAINER_NAME, alive=False)
        register_service(db, service)

    return JSONResponse(
        status_code=status_code,
        content=status,
    )


@app.get('/config/')
async def get_services_config(db: Session = Depends(get_db)):
    configs = {}
    effect_svc = get_service(db, config.EFFECTS_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/service"
        response = requests.get(url)
        effect_config = {
            "config": response.json(),
            "status_code": 200
        }
        if response.status_code != 200:
            effect_config["status_code"] = response.status_code
        url = f"http://{effect_svc.ip}:{effect_svc.port}/effect"
        response = requests.get(url)
        effect_config["config"].update(response.json())
        if response.status_code != 200:
            effect_config["status_code"] = response.status_code
        url = f"http://{effect_svc.ip}:{effect_svc.port}/cache"
        response = requests.get(url)
        effect_config["config"].update(response.json())
        if response.status_code != 200:
            effect_config["status_code"] = response.status_code
    else:
        effect_config = {
            "config": "Not found. Service not registered",
            "status_code": 400
        }
    video_svc = get_service(db, config.VIDEOPROXY_CONTAINER_NAME)
    if video_svc:
        url = f"http://{video_svc.ip}:{video_svc.port}/service"
        response = requests.get(url)
        video_config = {
            "config": response.json(),
            "status_code": response.status_code
        }
        if response.status_code != 200:
            video_config["status_code"] = response.status_code
        url = f"http://{video_svc.ip}:{video_svc.port}/stream_type"
        response = requests.get(url)
        video_config["config"].update(response.json())
        if response.status_code != 200:
            video_config["status_code"] = response.status_code
        url = f"http://{video_svc.ip}:{video_svc.port}/video_source"
        response = requests.get(url)
        video_config["config"].update(response.json())
        if response.status_code != 200:
            video_config["status_code"] = response.status_code
        url = f"http://{video_svc.ip}:{video_svc.port}/virtual_device"
        response = requests.get(url)
        video_config["config"].update(response.json())
        if response.status_code != 200:
            video_config["status_code"] = response.status_code
    else:
        video_config = {
            "config": "Not found. Service not registered",
            "status_code": 400
        }
    device_svc = get_service(db, config.DEVICE_MNGR_CONTAINER_NAME)
    if device_svc:
        url = f"http://{device_svc.ip}:{device_svc.port}/cameras"
        response = requests.get(url)
        device_config = {
            "config": {"webcams": response.json()},
            "status_code": response.status_code
        }
    else:
        device_config = {
            "config": "Not found. Service not registered",
            "status_code": 400
        }
    configs[config.EFFECTS_CONTAINER_NAME] = effect_config
    configs[config.VIDEOPROXY_CONTAINER_NAME] = video_config
    configs[config.DEVICE_MNGR_CONTAINER_NAME] = device_config
    return JSONResponse(
        status_code=200,
        content=configs,
    )


@app.post('/video')
async def start_video(db: Session = Depends(get_db)):
    status_code = 200
    status = {}
    effect_svc = get_service(db, config.EFFECTS_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/service"
        response = requests.post(url)
        status_code = response.status_code
        if status_code != 200:
            status["error"] = response.json()
        else:
            status["server"] = response.json()
    else:
        status_code = 400
        status["error"] = "Effect service not registered"

    if status_code == 200:
        video_svc = get_service(db, config.VIDEOPROXY_CONTAINER_NAME)
        if video_svc:
            url = f"http://{video_svc.ip}:{video_svc.port}/service"
            response = requests.post(url)
            if status_code != 200:
                status["error"] = response.json()
            else:
                status["client"] = response.json()
        else:
            status_code = 400
            status["error"] = "Video proxy service not registered"
    
    return JSONResponse(
        status_code=status_code,
        content=status,
    )


@app.delete('/video')
async def stop_video(db: Session = Depends(get_db)):
    status_code = 200
    status = {}
    effect_svc = get_service(db, config.EFFECTS_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/service"
        response = requests.delete(url)
        status_code = response.status_code
        if status_code != 200:
            status["error"] = response.json()
        else:
            status["server"] = response.json()
    else:
        status_code = 400
        status["error"] = "Effect service not registered"

    if status_code == 200:
        video_svc = get_service(db, config.VIDEOPROXY_CONTAINER_NAME)
        if video_svc:
            url = f"http://{video_svc.ip}:{video_svc.port}/service"
            response = requests.delete(url)
            if status_code != 200:
                status["error"] = response.json()
            else:
                status["client"] = response.json()
        else:
            status_code = 400
            status["error"] = "Video proxy service not registered"
    
    return JSONResponse(
        status_code=status_code,
        content=status,
    )

@app.post('/iccam')
async def create_iccam(db: Session = Depends(get_db)):
    status_code=200
    status = {}
    effect_svc = get_service(db, config.DEVICE_MNGR_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/cameras"
        response = requests.post(url)
        status_code = response.status_code
        if status_code != 200:
            status["error"] = response.json()
        else:
            status["iccam_id"] = response.json()["device_id"]
    else:
        status_code = 400
        status["error"] = "Device Manager service not registered"
    
    if status_code == 200:
        video_svc = get_service(db, config.VIDEOPROXY_CONTAINER_NAME)
        if video_svc:
            url = f"http://{video_svc.ip}:{video_svc.port}/virtual_device/{status['iccam_id']}"
            response = requests.post(url)
            if status_code != 200:
                status["error"] = response.json()
        else:
            status_code = 400
            status["error"] = "Video proxy service not registered"
    
    return JSONResponse(
        status_code=status_code,
        content=status,
    )


@app.delete('/iccam')
async def delete_iccam(db: Session = Depends(get_db)):
    status_code=200
    status = {}
    effect_svc = get_service(db, config.DEVICE_MNGR_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/cameras"
        response = requests.delete(url)
        status_code = response.status_code
        if status_code != 200:
            status["error"] = response.json()
    else:
        status_code = 400
        status["error"] = "Device Manager service not registered"
    
    return JSONResponse(
        status_code=status_code,
        content=status,
    )


@app.get("/cache")
async def get_cache(db: Session = Depends(get_db)):
    effect_svc = get_service(db, config.EFFECTS_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/cache"
        response = requests.get(url)
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    return JSONResponse(
        status_code=400,
        content="Effect service not registered",
    )


@app.post("/cache")
async def set_cache(cache: int = 0, db: Session = Depends(get_db)):
    effect_svc = get_service(db, config.EFFECTS_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/cache?cache={cache}"
        response = requests.post(url)
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    return JSONResponse(
        status_code=400,
        content="Effect service not registered",
    )


@app.post('/effect/{effect_name}')
async def set_effect(effect_name: str, db: Session = Depends(get_db)):
    effect_svc = get_service(db, config.EFFECTS_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/effect/{effect_name}"
        response = requests.post(url)
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    return JSONResponse(
        status_code=400,
        content="Effect service not registered",
    )


@app.delete('/effect')
async def remove_effect(db: Session = Depends(get_db)):
    effect_svc = get_service(db, config.EFFECTS_CONTAINER_NAME)
    if effect_svc:
        url = f"http://{effect_svc.ip}:{effect_svc.port}/effect"
        response = requests.delete(url)
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    return JSONResponse(
        status_code=400,
        content="Effect service not registered",
    )


@app.post('/video_source')
async def set_video_source(video_source: VideoSource, db: Session = Depends(get_db)):
    video_svc = get_service(db, config.VIDEOPROXY_CONTAINER_NAME)
    if video_svc:
        url = f"http://{video_svc.ip}:{video_svc.port}/video_source"
        response = requests.post(url, json=video_source.dict())
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    return JSONResponse(
        status_code=400,
        content="Video proxy service not registered",
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.API_PORT)
