# image_classifier_app.py

import os
import shutil
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from image_segmentation import segment_image_into_blocks

class ImageClassifierApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Classifier")
        self.master.geometry("800x600")

        self.segmented_images = []  # List to store the paths of segmented images
        self.selected_images = []   # List to store the selected images

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
            # Segment the image into 50x50 pixel blocks after resizing and display them
            self.segmented_images, self.num_columns, self.num_rows = segment_image_into_blocks(
                file_path,
                block_size=(50, 50),
                resize_dims=(1100, 600),
                output_dir="out/segmented_images"
            )
            self.display_images()
            self.confirm_button.config(state=NORMAL)

    def display_images(self):
        # Clear the previous images
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.selected_images = []  # Reset selected images

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

            self.image_buttons.append(image_button)

        # Update scroll region based on the new content
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def toggle_select(self, index, image_path):
        # Toggle the selection of an image and change the button size to simulate shrinking
        if index in self.selected_images:
            self.selected_images.remove(index)
            # Restore the original size of the button image (32x32)
            img = Image.open(image_path).resize((32, 32), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_buttons[index].config(image=img_tk)
            self.image_buttons[index].image = img_tk  # Keep reference
        else:
            self.selected_images.append(index)
            # Shrink the image size (20x20) to simulate the selection
            img = Image.open(image_path).resize((20, 20), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_buttons[index].config(image=img_tk)
            self.image_buttons[index].image = img_tk  # Keep reference

    def confirm_selection(self):
        selected_dir = "out/mii_images"
        not_selected_dir = "out/not_mii_images"

        # Create directories if they don't exist
        if not os.path.exists(selected_dir):
            os.makedirs(selected_dir)
        if not os.path.exists(not_selected_dir):
            os.makedirs(not_selected_dir)

        # Move selected images to "mii_images" and unselected to "not_mii_images"
        for i, image_path in enumerate(self.segmented_images):
            if i in self.selected_images:
                shutil.move(image_path, os.path.join(selected_dir, os.path.basename(image_path)))
            else:
                shutil.move(image_path, os.path.join(not_selected_dir, os.path.basename(image_path)))

        print("Images classified and moved!")
        self.label.config(text="Classification complete!")
        self.confirm_button.config(state=DISABLED)

    def on_frame_configure(self, event):
        # Update scroll region when the frame is resized
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def _on_mousewheel(self, event):
        # Scroll vertically with the mouse wheel
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
