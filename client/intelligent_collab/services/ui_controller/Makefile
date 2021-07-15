DOCKER_BUILD_CMD?=docker build
DOCKER_NAME?=ic-ui-controller
DOCKER_IMAGE?=ic-ui-controller
DOCKER_FILE?=./Dockerfile
DOCKER_WS=./
UI_PORT=3000
REACT_APP_MAIN_CONTROLLER_API=http://127.0.0.1:8000

all .DEFAULT:
	$(DOCKER_BUILD_CMD) -f $(DOCKER_FILE) -t $(DOCKER_IMAGE) $(DOCKER_WS)

run:
	docker run --rm -p $(UI_PORT):80 $(DOCKER_IMAGE)

start:
	cd src/ui_controller && npm install && REACT_APP_MAIN_CONTROLLER_API=$(REACT_APP_MAIN_CONTROLLER_API) npm start

clean:
	docker rmi $(DOCKER_IMAGE)

.PHONY: $(DEFAULT_TARGETS)