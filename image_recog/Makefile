DOCKER_BUILD_CMD?=docker build
DOCKER_NAME?=stacks_img_recog
DOCKER_IMAGE?=stacks_img_recog
DOCKER_FILE?=./Dockerfile
DOCKER_WS=./

all .DEFAULT:
	$(DOCKER_BUILD_CMD)  -f $(DOCKER_FILE) -t $(DOCKER_IMAGE)  $(DOCKER_WS)

clean:
	docker rmi $(DOCKER_IMAGE)

.PHONY: $(DEFAULT_TARGETS)
