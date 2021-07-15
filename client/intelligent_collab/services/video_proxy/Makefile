DOCKER_BUILD_CMD?=docker build
DOCKER_NAME?=ic-video-proxy
DOCKER_IMAGE?=ic-video-proxy
DOCKER_FILE?=./Dockerfile
DOCKER_WS=./
API_PORT=8002
ZMQ_PORT=5555

all .DEFAULT:
	$(DOCKER_BUILD_CMD) -f $(DOCKER_FILE) -t $(DOCKER_IMAGE) $(DOCKER_WS)

run:
	docker run --rm -p $(ZMQ_PORT):5555 $(DOCKER_IMAGE)

start:
	poetry install
	cd src/video_proxy && poetry run uvicorn --host 0.0.0.0 --port $(API_PORT) api:app --reload

test:
	poetry install
	poetry run pytest tests

clean:
	docker rmi $(DOCKER_IMAGE)

.PHONY: $(DEFAULT_TARGETS)
