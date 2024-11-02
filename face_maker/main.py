import os
import cv2
import numpy as np

# Importing functions from separate files
from face_maker.mii_classification import classify_and_draw_boxes
from face_maker.mii_stitching import stitch_mii_faces

# Example usage
if __name__ == "__main__":
    image_path = "img_new.png"  # Replace with your image path
    model_path = "mii_classifier_model_6.keras"  # Ensure this path is correct
    output_path = "output_image_with_mii_boxes.png"

    # Classify and draw boxes, getting the list of identified Mii blocks
    identified_mii_blocks = classify_and_draw_boxes(image_path, model_path, output_path)
    print("Identified Mii blocks:", identified_mii_blocks)

    # Stitch faces from identified blocks
    stitch_mii_faces(image_path, identified_mii_blocks)
