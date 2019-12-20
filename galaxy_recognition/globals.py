# Global variables
#
# Copyright (c) 2019 Intel Corporation
#
# Main authors:
#   * Hugo Soto <hugo.a.soto.lopez@intelcom>
#   * Hector Robles <jesus.hector.robles.gutierrez@intel.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Training directories

current_path = "/home/new_dataset/"
dataset_filename = "dataset.csv"

training_path = current_path + "images/"
training_csv_path = current_path + dataset_filename
pt_model_name = "galaxy_recognition_model.pt"

# Dataset training variables
SPLIT_RATIO = 0.05
RANDOM_SEED = 40
WORKERS = 22
BATCH = 96
NUM_EPOCHS = 5

# Hardware related for training
TRAIN_DEV = "cpu"
NUM_DEVS = 2 #  Number of CPU's for multiprocess
NUM_CLASSES = 9 #  Number of classes in dataset CSV file

# Model Optimizer variables

# Learning rate
lr = 0.4 
# Momentum Factor
momentum = 0.9
# Verbosity
verbose = True



