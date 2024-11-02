import cv2
import numpy as np
import matplotlib.pyplot as plt

def stitch_mii_faces(image_path, identified_mii_blocks, block_size=(50, 50), resize_dims=(900, 500)):
    """
    Reconstructs Mii faces from identified blocks by detecting bounding boxes for contiguous blocks.
    
    :param image_path: Path to the original image.
    :param identified_mii_blocks: List of tuples with (row, col) for each block identified as a Mii.
    :param block_size: Size of each block in pixels.
    :param resize_dims: Dimensions to which the original image was resized.
    """
    # Load and resize the image
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, resize_dims)
    
    # Prepare a blank canvas for each Mii face
    faces = []

    # Group Mii blocks into clusters representing single faces
    face_groups = group_mii_blocks(identified_mii_blocks)

    for face_group in face_groups:
        # Calculate the bounding box for the current face group
        min_row = min(face_group, key=lambda x: x[0])[0]
        max_row = max(face_group, key=lambda x: x[0])[0]
        min_col = min(face_group, key=lambda x: x[1])[1]
        max_col = max(face_group, key=lambda x: x[1])[1]

        # Calculate pixel coordinates for the bounding box
        x_start = min_col * block_size[0]
        x_end = (max_col + 1) * block_size[0]
        y_start = min_row * block_size[1]
        y_end = (max_row + 1) * block_size[1]

        # Crop the face image from the resized image
        face_img = resized_image[y_start:y_end, x_start:x_end]
        
        # Append the reconstructed face
        faces.append(face_img)
    
    # Display each reconstructed face
    for i, face_img in enumerate(faces):
        plt.figure()
        plt.imshow(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(f'Mii Face {i+1}')
    plt.show()

def group_mii_blocks(mii_blocks):
    """
    Groups Mii blocks into clusters representing individual faces.
    
    :param mii_blocks: List of (row, col) tuples.
    :return: List of lists, where each sublist is a group of contiguous (row, col) tuples.
    """
    face_groups = []
    visited = set()

    def dfs(block, group):
        row, col = block
        if block in visited:
            return
        visited.add(block)
        group.append(block)

        # Check all 8 neighbors to allow flexible grouping of blocks
        neighbors = [(row + dr, col + dc) for dr in range(-1, 2) for dc in range(-1, 2) if (dr, dc) != (0, 0)]
        for neighbor in neighbors:
            if neighbor in mii_blocks and neighbor not in visited:
                dfs(neighbor, group)

    for block in mii_blocks:
        if block not in visited:
            group = []
            dfs(block, group)
            face_groups.append(group)

    return face_groups

# Example usage with the identified blocks
# # identified_mii_blocks is a list of (row, col) tuples, e.g., [(1, 5), (1, 6), (2, 5), (2, 6), ...]
# identified_mii_blocks = [
#     (1, 5), (1, 6), (2, 5), (2, 6),  # Example Mii face 1
#     (4, 3), (4, 4), (5, 3), (5, 4),  # Example Mii face 2
#     # Add more blocks here based on the actual identified blocks from your code
# ]

