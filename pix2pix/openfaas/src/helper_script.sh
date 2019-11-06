#! /usr/bin/env bash

# Clone usecases repo and cd into pix2pix
git clone https://github.intel.com/verticals/usecases
cp -a ./usecases/tensorflow/pix2pix/infer.py ./infer.py \
&& cp -a ./usecases/tensorflow/pix2pix/scripts .

# Save a pretrained model inside model/
mkdir -p ./models
mv generator_model.h5 ./models/

# Workdir cleanup
rm -rf ./usecases/ \
requirements.txt \
helper_script.sh \
main.py
