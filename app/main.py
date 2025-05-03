# main.py

from tkinter import Tk
from image_classifier_app import ImageClassifierApp

def main():
    root = Tk()
    app = ImageClassifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# Testing as of 10/29 11:41 PM, it should be good to process all the test images I have. Of course, the model architecture is not done, but I'm on track to get 40k data samples. Hopefully the model will not be overfit. 

# 10/31 10:30 PM, making training data was painful because I have to think about the purpose this model will serve. This model just exists to identify where the faces are. I need to make another model that actually extracts out the info from this model to make new Miis. Maybe if I make the cells bigger it will be easier to identify the Miis. 

# 10/31 11:32 PM, I think I'm having a data leakage problem. My models do not work at all. They get 100% in the training data and that's it. 