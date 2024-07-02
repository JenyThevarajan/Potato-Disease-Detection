# -*- coding: utf-8 -*-
"""July_01_PDD_Phase2_V3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xQ9JG0fAZP5dd0u1QdmKdLDBvWyDf8Pa
"""

!pip install roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="FXakvGs1mlVg7Bnx3e4R")  # Replace "YOUR_API_KEY" with your Roboflow API key
project = rf.project("plantdiseasedetection_phase2")
version = project.version(3)  # You can specify the version number if there are multiple versions
dataset = version.download("yolov8")

# Verify GPU availability
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
if len(tf.config.experimental.list_physical_devices('GPU')) > 0:
    print("GPU is available.")
else:
    print("GPU is not available. Please check your GPU setup.")

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

!pip install ultralytics==8.0.196

from ultralytics import YOLO
from IPython.display import display, Image

HOME = "/content/drive/MyDrive"

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}

# Train the model for vehicle counting
!yolo task=detect mode=train model=yolov8n.pt data=/content/PlantDiseaseDetection_Phase2-3/data.yaml epochs=50 imgsz=416 plots=True

import shutil

# Source path
source = "/content/drive/MyDrive/runs/detect/train17/weights/best.pt"

# Destination path
destination = "/content/drive/MyDrive/PDD_Phase2_V3/PDD_Phase2_V3.pt"

# Move the file
shutil.move(source, destination)

!yolo task=detect mode=val model=/content/drive/MyDrive/PDD_Phase2_V3/PDD_Phase2_V3.pt data=/content/PlantDiseaseDetection_Phase2-3/data.yaml

!ls {HOME}/runs/detect/train17/

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train17/confusion_matrix.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train17/results.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train17/val_batch1_pred.jpg', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=detect mode=predict model=/content/drive/MyDrive/PDD_Phase2_V3/PDD_Phase2_V3.pt conf=0.25 source=/content/PlantDiseaseDetection_Phase2-3/test/images save=True

import glob
from IPython.display import Image, display

for image_path in glob.glob(f'/content/drive/MyDrive/runs/detect/predict9/1020_jpg.rf.557110ea59b6211e31a345be291a0056.jpg')[:3]:
      display(Image(filename=image_path, width=600))
      print("\n")

import shutil

# Source path of best.pt
source = "/content/drive/MyDrive/PDD_Phase2_V3/PDD_Phase2_V3.pt"

# Destination path where you want to move and rename the file
destination = "/content/drive/MyDrive/runs/detect/train17/weights/best.pt"

# Move and rename the file
shutil.move(source, destination)

project.version(dataset.version).deploy(model_type="yolov8", model_path=f"/content/drive/MyDrive/runs/detect/train17")

#Run inference on your model on a persistant, auto-scaling, cloud API

#load model
model = project.version(dataset.version).model

#choose random test set image
import os, random
test_set_loc = "/content/PlantDiseaseDetection_Phase2-3/test/images/"
random_test_image = random.choice(os.listdir(test_set_loc))
print("running inference on " + random_test_image)

pred = model.predict(test_set_loc + random_test_image, confidence=10, overlap=40).json()
pred

