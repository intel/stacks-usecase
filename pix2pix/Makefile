all:
	$(MAKE) train infer


train:
	docker build -t pix2pix-train -f Dockerfile .

run-trainer:
	docker run -it pix2pix-train

infer:
	docker build -t pix2pix-infer -f Dockerfile.infer .

run-infer:
	docker run -it pix2pix-infer
	

