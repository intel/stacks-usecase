#! /usr/bin/env bash

# Clone usecases repo and cd into pix2pix
git clone https://github.com/intel/stacks-usecase.git
cp -a ./stacks-usecase/pix2pix/infer.py ./infer.py \
&& cp -a ./stacks-usecase/pix2pix/scripts .

# Save a pretrained model inside model/
mkdir -p ./models
mv generator_model.h5 ./models/

# Workdir cleanup
rm -rf ./stacks-usecase/ \
requirements.txt \
helper_script.sh \
main.py
