import os

from fastapi import FastAPI

ZMQ_PORT = int(os.environ.get("ZMQ_PORT", "5555"))
API_PORT = int(os.environ.get("API_PORT", "8000"))

app = FastAPI()
app.state.config = {}
