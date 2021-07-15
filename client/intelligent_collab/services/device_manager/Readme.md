# Video Device Manager


The *Video Device Manager* service manages the Intelligent Collaboration virtual cameras, actions on this service can be accessed by its API.

The API is using the [FastAPI](https://fastapi.tiangolo.com/) and [uvicorn](https://www.uvicorn.org/) as ASGI server.


## Requirements

The Video Device Manager requires a pre-installed kernel module.
The [`v4l2loopback`](https://github.com/umlaeute/v4l2loopback) is a kernel module to create V4L2 loopback devices that will serve for streaming our filtered video content.

Run the following script for installing it in your system before any execution:
```
./scripts/install_virtual_camera.sh
```


## Video Device Manager API Server

- Install project's dependencies
```
poetry install
```

- Start the API server with `poetry` and `uvicorn`
```
poetry run uvicorn api:app --reload
```


## Running with `docker`

The Video Device Manager will require `privileged` in order to enable the `v4l2loopback` kernel module and then, create the virtual camera devices.

- Build the container
```
docker build -t sysstacks/icollab-vdm .
```

- Run it
```
docker run --rm \
       --privileged -v /lib/modules:/lib/modules -v /dev/:/dev:ro \
       -p 8000:8000 \
       --name icollab-vdm sysstacks/icollab-vdm
```

- Run it for development
```
docker run --rm \
       --privileged -v /lib/modules:/lib/modules -v /dev/:/dev:ro \
       -v $(pwd):/workspace \
       -p 8000:8000 \
       --name icollab-vdm sysstacks/icollab-vdm
```


## API Documentation


### List All Camera devices

```
curl -X 'GET' 'http://localhost:8000/cameras' \
  -H 'accept: application/json'
```


### Create `iccamera` device

```
curl -X 'POST' 'http://localhost:8000/cameras' \
  -H 'accept: application/json'
```


### Get `iccamera` device details

```
curl -X 'GET' 'http://localhost:8000/cameras/<camera_id>' \
  -H 'accept: application/json'
```


### Delete `iccamera` device
```
curl -X 'DELETE' 'http://localhost:8000/cameras/<camera_id>' \
  -H 'accept: application/json'
```
