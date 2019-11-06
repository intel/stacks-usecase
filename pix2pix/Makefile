all:
	$(MAKE) train infer


train:
	docker build -t pix2pix-train -f Dockerfile .

infer:
	docker build -t pix2pix-infer -f Dockerfile.infer .
