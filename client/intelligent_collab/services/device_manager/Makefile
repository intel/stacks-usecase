DOCKER_BUILD_CMD?=docker build
DOCKER_NAME?=ic-device-manager
DOCKER_IMAGE?=ic-device-manager
DOCKER_FILE?=./Dockerfile
DOCKER_WS=./
API_PORT=8003

all .DEFAULT:
	$(DOCKER_BUILD_CMD) -f $(DOCKER_FILE) -t $(DOCKER_IMAGE) $(DOCKER_WS)

run:
	docker run --rm $(DOCKER_IMAGE)

start:
	poetry install
	cd src/device_manager && poetry run uvicorn --host 0.0.0.0 --port $(API_PORT) api:app --reload

test:
	poetry install
	poetry run pytest tests

clean:
	docker rmi $(DOCKER_IMAGE)

.PHONY: $(DEFAULT_TARGETS)