# effects client

The client downloads and image, sends it over zmq, to the effects_container server.

## Installation

```bash
pip install -r requirements.txt`
```

## Running

Ensure that the server is running, use the client to talk to the server.

```bash
python effects_client.py
```

This will if successful talk to the server and save the updated image to the local dir.


