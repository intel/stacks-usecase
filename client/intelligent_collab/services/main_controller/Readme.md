## main controller

Main controller service that orchestrates the service

This service creates and manage a database of Intelligent Collaboration
services that can be read and updated through an API using `GET` and `POST`
methods.

The API is built using [FastAPI](https://fastapi.tiangolo.com/) and executed
using [uvicorn](https://www.uvicorn.org/):

```
uvicorn main:app --reload --host <desired-host-ip>
```

Following is the service schema used in the database (`title` and `alive` are
required fields):
```
{
  "title": "string",
  "summary": "string",
  "url": "string",
  "port": "string",
  "alive": boolean,
  "parameter": "string"
}
```

# API usage / documentation
Once the service is running, the API documentation is available through browser
at the selected IP, in the `docs` directory (note that the default port is 8000). For example:

```
https://10.20.30.40:8000/docs
```
the documentation describes avaliable methods and examples of request bodies.

# View available services

To get all the available services, no parameter is required and it can be achieved thorugh the following command:
```
curl -X 'GET' 'http://10.20.30.40:8000/services/' \
  -H 'accept: application/json'
```

# Register/update a service

To register a new service or update an existing one, execute the following:

```
curl -X 'POST' \
  'http://10.20.30.40:8000/services/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "service_discovery",
  "summary": "test",
  "url": "10.20.30.40",
  "port": "12345",
  "alive": true,
  "parameter": "none"
}'
