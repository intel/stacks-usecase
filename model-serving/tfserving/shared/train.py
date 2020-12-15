"""
This is a placeholder, you should replace this file
with your actual model building script.
"""
import os
import numpy as np
import tensorflow as tf

def train_my_model():
"""
Your code goes here
"""


"""
Saving your model in SavedModel.
This is an example, please adapt as needed.
"""
MODEL_DIR = "/workspace/models/"
version = 1
export_path = os.path.join(MODEL_DIR, str(version))
print('export_path = {}\n'.format(export_path))

tf.keras.models.save_model(
    model,
    export_path,
    overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None
)
