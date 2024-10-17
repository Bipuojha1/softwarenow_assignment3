import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np

# Base Class for the Application Window
class BaseWindow:
    def __init__(self, title="AI App", size="400x400"):
        # Encapsulation: Hides the implementation details of the window setup
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)

    def run(self):
        # Method to start the Tkinter main loop
        self.root.mainloop()

# Decorator to check if an image has been loaded before processing
def check_image_loaded(func):
    def wrapper(instance, *args, **kwargs):
        if instance.image is None:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        return func(instance, *args, **kwargs)
    return wrapper

# Class for Loading and Displaying Images
class ImageLoader:
    def __init__(self):
        # Encapsulation: Image attribute is kept private
        self._image = None

    def load_image(self, filepath):
        self._image = Image.open(filepath)
        return self._image

    @property
    def image(self):
        return self._image

# Main Application Class with Multiple Inheritance from BaseWindow and ImageLoader
class ImageClassifierApp(BaseWindow, ImageLoader):
    def __init__(self):
        # Initializes both parent classes
        BaseWindow.__init__(self, "Image Classifier", "600x600")
        ImageLoader.__init__(self)
        
        self.label = tk.Label(self.root, text="Upload an image to classify", font=("Arial", 14))
        self.label.pack(pady=20)

        self.upload_btn = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        self.classify_btn = tk.Button(self.root, text="Classify Image", command=self.classify_image)
        self.classify_btn.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)
        
        # Load pre-trained MobileNetV2 model
        self.model = tf.keras.applications.MobileNetV2(weights="imagenet")
        self.image_display = None

    def upload_image(self):
        # Method overriding: Changing the behavior of upload_image in this context
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if filepath:
            self._image = self.load_image(filepath)
            self.display_image()
    
    def display_image(self):
        img_resized = self._image.resize((200, 200))
        self.image_display = ImageTk.PhotoImage(img_resized)
        self.label.config(image=self.image_display, text="")

    @check_image_loaded  # Decorator: Ensures image is loaded before classification
    def classify_image(self):
        # Convert the image to RGB in case it has an alpha channel
        img_rgb = self._image.convert("RGB")  # Convert to RGB to ensure 3 channels
        img_resized = img_rgb.resize((224, 224))  # Required size for MobileNetV2
        
        img_array = np.array(img_resized) / 255.0  # Normalize the image
        img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions to fit model input

        # Predict using the model
        predictions = self.model.predict(img_array)
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)
        
        # Display the top prediction
        top_pred = decoded_predictions[0][0]
        self.result_label.config(text=f"Prediction: {top_pred[1]}, Confidence: {top_pred[2]:.2f}")

# Running the Application
app = ImageClassifierApp()
app.run()
