DOCKER_BUILD_CMD?=docker build
DOCKER_IMAGE_TRAIN?=github_issue_classifier_train
DOCKER_IMAGE_INFER?=github_issue_classifier
DOCKER_FILE_TRAIN?=./Dockerfile.train
DOCKER_FILE_INFER?=./Dockerfile.infer
DOCKER_WS=../

all .DEFAULT:
		$(MAKE) infer train

infer: 
		$(DOCKER_BUILD_CMD)  -f $(DOCKER_FILE_INFER) -t $(DOCKER_IMAGE_INFER)  $(DOCKER_WS)

train: 
		$(DOCKER_BUILD_CMD)  -f $(DOCKER_FILE_TRAIN) -t $(DOCKER_IMAGE_TRAIN)  $(DOCKER_WS)

infer_run:
	docker run -p 5059:5059 -it $(DOCKER_IMAGE_INFER)

clean:
		docker rmi $(DOCKER_IMAGE_TRAIN)
		docker rmi $(DOCKER_IMAGE_INFER)

.PHONY: $(DEFAULT_TARGETS)

