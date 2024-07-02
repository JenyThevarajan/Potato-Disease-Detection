# -*- coding: utf-8 -*-
"""Testing_PDD_Phase2_v3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IJ6MauEowI1eClh3C7j3WQepYIKXAUJx
"""

# Install YOLOv8 (Ultralytics)
!pip install ultralytics

# Install other dependencies if needed
!pip install Pillow matplotlib

from ultralytics import YOLO
import os
import random
import matplotlib.pyplot as plt
from PIL import Image

# Load the trained model from best.pt
model_path = "/content/drive/MyDrive/runs/detect/train17/weights/best.pt"
model = YOLO(model_path)

import json

def predict_random_images(folder_path, num_images=4):
    # List all images in the folder
    image_files = os.listdir(folder_path)

    # Randomly select a subset of images
    random.shuffle(image_files)
    selected_images = image_files[:num_images]

    predictions = []

    # Set up the subplot
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    for idx, image_file in enumerate(selected_images):
        image_path = os.path.join(folder_path, image_file)

        # Load the image
        img = Image.open(image_path)

        # Perform the prediction
        results = model.predict(image_path, conf=0.10, iou=0.50)
        prediction = results[0].tojson()

        # Parse the JSON string to a dictionary
        prediction_dict = json.loads(prediction)

        # Extract only the desired fields
        filtered_predictions = [{'confidence': det['confidence'], 'class': det['name']} for det in prediction_dict]

        # Print the prediction
        print(f"Predictions for {image_file}:")
        for det in filtered_predictions:
            det['confidence'] = f"conf={det['confidence']:.2f}"  # Change confidence format
            print(f"{det['class']} ({det['confidence']})")

        # Display the image in the subplot
        ax = axs[idx // 2, idx % 2]
        ax.imshow(img)
        ax.axis('off')
        title = "\n".join([f"{det['class']} ({det['confidence']})" for det in filtered_predictions])
        ax.set_title(title)

        # Collect predictions
        predictions.append({
            'image': image_file,
            'prediction': filtered_predictions
        })

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

    return predictions

# Step 4: Call the prediction function
test_images_folder = '/content/drive/MyDrive/PDD_Phase2_V2/test/images'

# Predict randomly selected 4 images in the folder
predictions = predict_random_images(test_images_folder, num_images=4)

import os
import matplotlib.pyplot as plt
from PIL import Image
import json  # Import json for parsing

# Assuming the model is already loaded
# from ultralytics import YOLO
# model_path = "/content/drive/MyDrive/PDD_Phase2_V3/PDD_Phase2_V3.pt"
# model = YOLO(model_path)

def predict_single_image(image_path):
    # Load the image
    img = Image.open(image_path)

    # Perform the prediction
    results = model.predict(image_path, conf=0.10, iou=0.30)
    prediction = results[0].tojson()

    # Parse the JSON string to a dictionary
    prediction_dict = json.loads(prediction)

    # Extract predictions
    predictions = prediction_dict

    # Print predictions
    for det in predictions:
        class_name = det['name']  # Assuming 'name' instead of 'class'
        confidence = det['confidence']
        print(f"Class: {class_name}, Confidence: {confidence:.2f}")

    # Display the image
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# Path to the image you want to predict
image_path = '/content/drive/MyDrive/Potato_SingleLeaves/Potato___Late_blight/1100.jpg'

# Make prediction and display
predict_single_image(image_path)

