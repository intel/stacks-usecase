MAKE := $(MAKE) -e
DOCKER_BUILD_CMD = docker build

all:
	$(MAKE) train serve website

train:
	$(DOCKER_BUILD_CMD) --build-arg stage=train -f docker/Dockerfile.$(TYPE) -t $(REGISTRY)/dlrs-train-$(TYPE) .

serve:
	$(DOCKER_BUILD_CMD) --build-arg stage=serve -f docker/Dockerfile.$(TYPE) -t $(REGISTRY)/dlrs-serve-$(TYPE) .

website:
	$(DOCKER_BUILD_CMD) -f docker/Dockerfile.website -t $(REGISTRY)/dlrs-website .

.PHONY: all train serve website
