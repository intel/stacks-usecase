#!/usr/bin/env python3
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


import os
import time
import copy
import sys
import numpy as np 
import pandas as pd 

import torch
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.sampler import SubsetRandomSampler
import torchvision
from torchvision import transforms, datasets, models
from skimage import io, transform
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler

from PIL import Image

# Global variables file globals.py
from globals import *

# Data Loader
class LoadGalaxy(Dataset):
    def __init__(self, root_dir, file_path, transform=None):
        self.data = pd.read_csv(file_path)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        obj_id = self.data.iloc[index, 0]
        obj_filename = os.path.join(self.root_dir, str(obj_id)) + ".jpg"
        image = Image.open(obj_filename)
        labels = self.data.iloc[index, 1:].values

        if self.transform:
            item = {'image': self.transform(image), 'labels': labels, 'id': obj_id}
        else:
            item = {'image': image, 'labels': labels, 'id': obj_id}
        return item

# Transform dataset for training
# Specify transforms using torchvision.transforms as transforms library
transform = transforms.Compose([
                                transforms.CenterCrop((224, 224)),
                                transforms.Resize((45, 45)),
                                transforms.RandomHorizontalFlip(p=0.5),
                                transforms.RandomRotation(degrees=(0,360)),
                                transforms.RandomVerticalFlip(p=0.5),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                     std=[0.229, 0.224, 0.225])
                                   ])


training_dataset = LoadGalaxy(training_path, training_csv_path, transform=transform)
size = len(training_dataset)
indx = list(range(size))
split = int(np.floor(SPLIT_RATIO * size))
np.random.seed(RANDOM_SEED)
np.random.shuffle(indx)

train_indx = indx[split:]
eval_indx = indx[:split]

training_sampler = SubsetRandomSampler(train_indx)
evaluation_sampler = SubsetRandomSampler(eval_indx)

training_dataloader = DataLoader(training_dataset, batch_size=BATCH, num_workers=WORKERS, sampler=training_sampler)

evaluation_dataloader = DataLoader(training_dataset, batch_size=BATCH, num_workers=WORKERS, sampler=evaluation_sampler)
 
# Prepare model to train and create neural network
device = torch.device(TRAIN_DEV)
model = models.resnet50(num_classes=NUM_CLASSES)
model = nn.DataParallel(model, device_ids=range(NUM_DEVS))

model.to(device)

criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum)
scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, 'min', verbose=True)

# Train model

def training():
    model.train()
    losses = []
    epoch_start = time.time()
    for i, batch in enumerate(training_dataloader):
        inputs, labels = batch['image'], batch['labels'].float().view(-1, NUM_CLASSES)
        inputs, labels = inputs.to(device), labels.to(device)


        # Set to zero the gradients
        optimizer.zero_grad()
        
        # compute output
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Record loss in RMSE
        losses.append(loss.item())
        loss = torch.sqrt(loss)
        
        #Backprop SGD step
        loss.backward()
        optimizer.step()

    epoch_loss = np.sqrt(sum(losses) / len(losses))
    epoch_time = time.time() - epoch_start
    
    return epoch_loss

# Evaluation

def evaluation():
    model.eval()
    losses = []
    epoch_start = time.time()
    for i, batch in enumerate(evaluation_dataloader):
        inputs, labels = batch['image'], batch['labels'].float().view(-1, NUM_CLASSES)
        inputs, labels = inputs.to(device), labels.to(device)

        # Compute output
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Record loss in RMSE
        losses.append(loss.item())
        loss = torch.sqrt(loss)

    epoch_loss = np.sqrt(sum(losses) / len(losses))
    epoch_time = time.time() - epoch_start

    return epoch_loss

train_losses = []
eval_losses = []
for epoch in range(NUM_EPOCHS):
    train_loss = training()
    eval_loss   = evaluation()
    scheduler.step(eval_loss)

    train_losses.append(train_loss)
    eval_losses.append(eval_loss)

# Save Trained Model
torch.save(model, pt_model_name)
