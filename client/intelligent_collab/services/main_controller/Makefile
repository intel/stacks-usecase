DOCKER_BUILD_CMD?=docker build
DOCKER_NAME?=icollab-main-service
DOCKER_IMAGE?=icollab-main-service
DOCKER_FILE?=./Dockerfile
DOCKER_WS=./

all .DEFAULT:
	$(DOCKER_BUILD_CMD) -f $(DOCKER_FILE) -t $(DOCKER_IMAGE) $(DOCKER_WS)

run:
	docker run --rm -p 8000:8000 $(DOCKER_IMAGE)
clean:
	docker rmi $(DOCKER_IMAGE)

.PHONY: $(DEFAULT_TARGETS)
