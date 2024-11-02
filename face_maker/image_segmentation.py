import os
import cv2

def segment_image_into_blocks(image_path, block_size=(50, 50), resize_dims=(900, 500)):
    """
    Segments an image into blocks of size block_size (50x50 by default) after resizing to resize_dims (1100x600).

    :param image_path: Path to the image.
    :param block_size: Tuple representing the width and height of each block.
    :param resize_dims: Tuple representing the width and height to resize the image before segmentation.
    :return: Tuple containing the list of block images, number of columns, number of rows, and the resized image.
    """
    # Load the image
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    print(f"Original image path: {image_path}")
    print(f"Original image size: {w}x{h}")

    # Resize the image to the specified dimensions
    resized_image = cv2.resize(image, resize_dims)
    resized_h, resized_w, _ = resized_image.shape
    print(f"Resized image to: {resized_w}x{resized_h}")

    block_w, block_h = block_size
    segmented_images = []
    block_count = 0

    num_columns = resized_w // block_w
    num_rows = resized_h // block_h
    print(f"Number of columns: {num_columns}, Number of rows: {num_rows}")

    # Loop over the resized image and segment it into blocks of block_size
    for i in range(0, resized_h, block_h):
        row_images = []
        for j in range(0, resized_w, block_w):
            # Crop the block from the image
            block_image = resized_image[i:i + block_h, j:j + block_w]

            # Handle cases where block size exceeds image boundary
            if block_image.shape[0] != block_h or block_image.shape[1] != block_w:
                block_image = cv2.resize(block_image, block_size)

            row_images.append(block_image)
            block_count += 1

        segmented_images.append(row_images)

    print(f"Segmented the image into {block_count} blocks.")
    return segmented_images, num_columns, num_rows, resized_image