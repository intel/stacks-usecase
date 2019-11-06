all:
	$(MAKE) train infer


train:
	docker run -it pix2pix-train -f Dockerfile .

infer:
	docker run -it pix2pix-infer -f Dockerfile.infer .
	

