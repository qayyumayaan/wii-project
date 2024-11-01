# image_classifier_app.py

import os
import shutil
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from image_segmentation import segment_image_into_blocks
import uuid

class ImageClassifierApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Classifier")
        self.master.geometry("800x600")

        self.segmented_images = []  # List to store the paths of segmented images
        self.selected_images = []   # List to store the selected images
        self.saved_selection = []   # List to store the saved selection indexes
        self.image_buttons = []     # List to store image buttons

        self.label = Label(master, text="Upload an image to begin")
        self.label.pack()

        self.upload_button = Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.confirm_button = Button(master, text="Confirm Selection", command=self.confirm_selection, state=DISABLED)
        self.confirm_button.pack()

        self.canvas_frame = Frame(master)
        self.canvas_frame.pack(fill=BOTH, expand=True)

        # Scrollable Canvas
        self.canvas = Canvas(self.canvas_frame)
        self.scrollbar_y = Scrollbar(self.canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar_x = Scrollbar(self.canvas_frame, orient=HORIZONTAL, command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # A frame inside the canvas to hold the images
        self.scrollable_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind the canvas scrolling event
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def upload_image(self):
        # Open a file dialog to upload an image
        file_path = filedialog.askopenfilename(title="Select an image")

        if file_path:
            # Clear previous segmented images from disk
            self.clear_segmented_images()

            # Segment the image into 50x50 pixel blocks after resizing and display them
            self.segmented_images, self.num_columns, self.num_rows = segment_image_into_blocks(
                file_path,
                block_size=(50, 50),
                resize_dims=(900, 500),
                output_dir="out/segmented_images"
            )
            self.display_images()
            self.confirm_button.config(state=NORMAL)

    def clear_segmented_images(self):
        output_dir = "out/segmented_images"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    def display_images(self):
        # Clear the previous images
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.selected_images = self.saved_selection.copy()  # Load saved selection
        self.image_buttons = []

        for i, image_path in enumerate(self.segmented_images):
            # Open each segmented image
            img = Image.open(image_path)
            img = img.resize((32, 32), Image.Resampling.LANCZOS)  # Resize to 32x32 for display
            img_tk = ImageTk.PhotoImage(img)

            # Create a button for each image
            image_button = Button(
                self.scrollable_frame,
                image=img_tk,
                command=lambda i=i, image_path=image_path: self.toggle_select(i, image_path)
            )
            image_button.image = img_tk  # Keep reference
            image_button.grid(
                row=i // self.num_columns,
                column=i % self.num_columns,
                padx=2,
                pady=2
            )  # Grid layout with dynamic columns

            # Apply saved selection appearance
            if i in self.saved_selection:
                self.shrink_image(image_button, image_path)

            self.image_buttons.append(image_button)

        # Update scroll region based on the new content
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def toggle_select(self, index, image_path):
        # Toggle the selection of an image and change the button size to simulate shrinking
        if index in self.selected_images:
            self.selected_images.remove(index)
            self.restore_image(self.image_buttons[index], image_path)
        else:
            self.selected_images.append(index)
            self.shrink_image(self.image_buttons[index], image_path)

    def shrink_image(self, button, image_path):
        # Shrink the image size (20x20) to simulate the selection
        img = Image.open(image_path).resize((20, 20), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        button.config(image=img_tk)
        button.image = img_tk  # Keep reference

    def restore_image(self, button, image_path):
        # Restore the original size of the button image (32x32)
        img = Image.open(image_path).resize((32, 32), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        button.config(image=img_tk)
        button.image = img_tk  # Keep reference

    def confirm_selection(self):
        selected_dir = "out/mii_images"
        not_selected_dir = "out/not_mii_images"

        # Save current selection
        self.saved_selection = self.selected_images.copy()

        # Create directories if they don't exist
        os.makedirs(selected_dir, exist_ok=True)
        os.makedirs(not_selected_dir, exist_ok=True)

        # Move selected images to "mii_images" and unselected to "not_mii_images"
        for i, image_path in enumerate(self.segmented_images):
            dest_dir = selected_dir if i in self.selected_images else not_selected_dir
            basename = os.path.basename(image_path)
            name, ext = os.path.splitext(basename)
            unique_id = uuid.uuid4().hex  # Generate a unique hexadecimal string
            new_filename = f"{name}_{unique_id}{ext}"
            dest_path = os.path.join(dest_dir, new_filename)

            shutil.move(image_path, dest_path)

        print("Images classified and moved!")
        self.label.config(text="Classification complete!")
        self.confirm_button.config(state=DISABLED)

        # Clear memory references and reset variables
        self.clear_memory()

    def clear_memory(self):
        # Destroy all widgets in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Reset image lists
        self.segmented_images = []
        self.image_buttons = []

        # Clear the canvas
        self.canvas.delete("all")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        # Force garbage collection
        import gc
        gc.collect()

    def on_frame_configure(self, event):
        # Update scroll region when the frame is resized
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def _on_mousewheel(self, event):
        # Scroll vertically with the mouse wheel
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
