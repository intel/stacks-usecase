## Fast image recognition

A simple image recognition REST API using [Efficient Net](https://github.com/lukemelas/EfficientNet-PyTorch).

Build the application by running `make` in `usecases/image_recog` directory, a docker image named `stacks_img_recog` would be built

To run the server:

```bash
›$ docker run -d -p 5059:5059 stacks_img_recog
```

Once the docker instance is up, on the client, you can run these:

Basic info about the API:

```bash

›$ curl -i   'http://localhost:5059/usage'
```

```bash
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 224
Server: Werkzeug/0.14.1 Python/3.7.3
Date: Fri, 09 Aug 2019 02:33:52 GMT

{
  "info": {
    "usage": {
      "client": "curl -i  -X POST -F img=@data/cat.jpg 'http://localhost:5059/recog'",
      "server": "docker run -d -p 5059:5059 stacks_img_recog"
    },
    "what": "image recognition api"
  }
}
```

Classify the sample image in the `data` directory:

![cat](./data/cat.jpg)

photo credit: Kerri Lee Smith <a href=http://www.flickr.com/photos/77654186@N07/48470874687>Ellie Belly Ladybug</a> via <a href=http://photopin.com>photopin</a> <a href=https://creativecommons.org/licenses/by-nc-sa/2.0/>(license)</a>

```bash
›$ curl -i  -X POST -F img=@data/cat.jpg 'http://localhost:5059/recog'
```

output:

```bash
HTTP/1.1 100 Continue
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 61
Server: Werkzeug/0.14.1 Python/3.7.3
Date: Fri, 09 Aug 2019 02:33:58 GMT

{
  "class": "Egyptian cat",
  "prob": 0.2503426969051361
}

```
