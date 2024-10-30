# main.py

from tkinter import Tk
from image_classifier_app import ImageClassifierApp

def main():
    root = Tk()
    app = ImageClassifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
