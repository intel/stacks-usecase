#!/usr/bin/env python

# Suppress warnings
from supress_warnings import *
import os
print(" ========== TF warnings are being suppressed. To unsuppress, comment out subpress_warnings  ========== ")
os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"


import argparse

import local.train as local_train
import local.infer as infer
import train
import utils.export_model


parser = argparse.ArgumentParser()
parser.add_argument("--local", action='store_true', help="Run training locally")
parser.add_argument("--local_epochs", type=int, default=10, help="local argument. How many epochs when running locally")
parser.add_argument("--local_bs", type=int, default=32, help="local argument. What batch size is used when running locally")
parser.add_argument("--local_vs", type=int, default=5, help="local argument. What validation split to use when running locally")
parser.add_argument("--local_load_model", action='store_true', help="local argument. Whether to load a model or make a new on. Default (no arg) makes a new model.")
parser.add_argument("--local_checkpoint", action='store_true', help="local argument. Loads a checkpoint if used. Default (no arg) behavior loads from 'models/unet.h5'.")
parser.add_argument("--infer", action='store_true', help="Run inference locally")
arguments = parser.parse_args()
     

def main():
    if arguments.local:
        print(" ====================== Running local training ====================== ")
        local_train.main(
        num_epochs=arguments.local_epochs, 
        batch_size=arguments.local_bs, 
        val_splits=arguments.local_vs,
        load_mod=arguments.local_load_model,
        checkpoint=arguments.local_checkpoint,
        )
    elif arguments.infer:
        print(" ====================== Running inference ====================== ")
        result = infer.main()
        return result
    else:
        print(" ====================== Run training and export ====================== ")
        train.train_unet()
        utils.export_model.main()	
    

if __name__ == '__main__':
    main()
