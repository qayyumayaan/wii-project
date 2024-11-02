import cv2
import numpy as np
from tensorflow.keras.models import load_model
from face_maker.image_segmentation import segment_image_into_blocks

def classify_and_draw_boxes(image_path, model_path='mii_classifier_model_3.keras', output_path='output_image_with_mii_boxes.png'):
    """
    Segments the input image, classifies each block using the pre-trained model, and draws red boxes around blocks classified as Mii.
    Also stores the coordinates of Mii blocks in identified_mii_blocks.

    :param image_path: Path to the input image.
    :param model_path: Path to the pre-trained Keras model.
    :param output_path: Path to save the output image with red boxes.
    :return: List of (row, col) tuples for identified Mii blocks.
    """
    # Load the pre-trained model
    model = load_model(model_path)
    print("Loaded the pre-trained model.")

    # Segment the image into blocks
    segmented_images, num_columns, num_rows, resized_image = segment_image_into_blocks(image_path, resize_dims=(900, 500))
    print("Segmented the image.")

    block_size = (50, 50)
    block_w, block_h = block_size

    # List to store identified Mii blocks
    identified_mii_blocks = []

    # Loop over each block and classify
    for row_idx, row_images in enumerate(segmented_images):
        for col_idx, block_image in enumerate(row_images):
            # Convert BGR to RGB
            block_image_rgb = cv2.cvtColor(block_image, cv2.COLOR_BGR2RGB)

            # Preprocess the block image
            block_image_preprocessed = block_image_rgb / 255.0  # Rescale pixel values
            block_image_preprocessed = np.expand_dims(block_image_preprocessed, axis=0)  # Add batch dimension

            # Predict using the model
            prediction = model.predict(block_image_preprocessed, verbose=0)
            prediction_label = 'Mii' if prediction <= 0.5 else 'Not Mii'
            print(f"Block at row {row_idx}, column {col_idx} classified as {prediction_label} with confidence {prediction[0][0]:.4f}")

            # If classified as Mii, draw a red rectangle and save block position
            if prediction <= 0.5:
                x = col_idx * block_w
                y = row_idx * block_h
                cv2.rectangle(resized_image, (x, y), (x + block_w, y + block_h), (0, 0, 255), 2)
                identified_mii_blocks.append((row_idx, col_idx))  # Save the position of Mii blocks

    # Save the output image with red boxes
    cv2.imwrite(output_path, resized_image)
    print(f"Output image saved to {output_path}")
    
    return identified_mii_blocks