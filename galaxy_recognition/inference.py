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

from globals import *

import os
import sys
import pandas as pd
import numpy as np
import torch
from torchvision import transforms
from PIL import Image

model = "galaxy_recognition_model"
save_model = True
model_filename = model + ".pt"
ds_dir = current_path
image_dir = os.getcwd()
image_name = sys.argv[2]
model_dir = os.getcwd()
header = ["ID", "P_EL", "P_CW", "P_ACW", "P_EDGE", 
          "P_DK", "P_MG", "P_CS", "P_EL_DEB", "P_CS_DEB"]
transf = transforms.Compose([transforms.CenterCrop((224, 224)),
                             transforms.Resize((45, 45)),
	                     transforms.ToTensor(),
	                     transforms.Normalize(mean=[0.485, 0.456, 0.406],
	                                          std=[0.229, 0.224, 0.225])
	                   ])

model = torch.load(model_dir + "/" + model_filename) #  Load model from .pt
image = Image.open(image_dir + "/" + image_name) #  Load image
model.eval() #  Set model to inference mode

# Pre-process images
test_img = transf(image)
batch_t = torch.unsqueeze(test_img, 0)
output = model(batch_t)
# Make inference
output_id = sys.argv[1]
values = output.detach().cpu().numpy()
combined = np.column_stack((output_id, values))

# Save outputs in CSV file
if os.path.exists(model_dir + '/' + 'infer-output.csv'):
    new_row = pd.DataFrame(combined, columns=header)
    new_row["ID"] = new_row["ID"].astype(np.uint32)
    new_row.to_csv(model_dir + '/' + 'infer-output.csv', 
                   index=False, header=False, mode='a')
else:
    new_row = pd.DataFrame(combined, columns=header)
    new_row["ID"] = new_row["ID"].astype(np.uint32)
    new_row.to_csv(model_dir + '/' + 'infer-output.csv',
                   index=False, mode='a', header=header)

print(new_row)
