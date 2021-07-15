import os

API_PORT = int(os.environ.get("API_PORT", "8000"))

EFFECTS_CONTAINER_NAME = os.environ.get("EFFECTS_CONTAINER_NAME", "icollab-effects")
VIDEOPROXY_CONTAINER_NAME = os.environ.get("VIDEOPROXY_CONTAINER_NAME", "icollab-videoproxy")
DEVICE_MNGR_CONTAINER_NAME = os.environ.get("DEVICE_MNGR_CONTAINER_NAME", "icollab-devmanager")

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''