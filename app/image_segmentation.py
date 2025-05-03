import os
import cv2

def segment_image_into_blocks(image_path, block_size=(50, 50), resize_dims=(1100, 600), output_dir="segmented_images"):
    """
    Segments an image into blocks of size block_size (50x50 by default) after resizing to resize_dims (1100x600).

    :param image_path: Path to the image.
    :param block_size: Tuple representing the width and height of each block.
    :param resize_dims: Tuple representing the width and height to resize the image before segmentation.
    :param output_dir: Directory to save the segmented blocks.
    """
    # Load the image
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    print(f"Original image path: {image_path}")
    print(f"Original image size: {w}x{h}")

    # Resize the image to the specified dimensions (1100x600)
    resized_image = cv2.resize(image, resize_dims)
    resized_h, resized_w, _ = resized_image.shape
    print(f"Resized image to: {resized_w}x{resized_h}")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    block_w, block_h = block_size
    segmented_images = []
    block_count = 0

    num_columns = resized_w // block_w
    num_rows = resized_h // block_h
    print(f"Number of columns: {num_columns}, Number of rows: {num_rows}")

    # Loop over the resized image and segment it into blocks of 50x50 pixels
    for i in range(0, resized_h, block_h):
        for j in range(0, resized_w, block_w):
            # Crop the block from the image
            block_image = resized_image[i:i + block_h, j:j + block_w]

            # Handle cases where block size exceeds image boundary
            if block_image.shape[0] != block_h or block_image.shape[1] != block_w:
                block_image = cv2.resize(block_image, block_size)

            # Save the block image
            block_filename = os.path.join(output_dir, f"block_{block_count}.png")
            cv2.imwrite(block_filename, block_image)
            segmented_images.append(block_filename)
            block_count += 1

    print(f"Segmented and saved {block_count} blocks to {output_dir}.")
    return segmented_images, num_columns, num_rows