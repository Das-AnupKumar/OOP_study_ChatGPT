import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# OOP Feature: Encapsulation
# Meaning:
#   Encapsulation is the concept of bundling data (attributes) and methods that operate on that data within a class,
#   while restricting access to some of the object's components from outside the class.
#   This helps protect the integrity of the data and ensures that an object manages its own state.
# Use in this code:
#   - The `ImageProcessor` class encapsulates image data (`self.image`) and methods that operate on it (`process`, `save_image`).
#   - The attributes and methods are packaged within the class, and direct access to the image is managed by methods like `process` and `save_image`.

# Base class
class ImageProcessor:
    """
    This is a base class that provides core image processing functionality.
    It encapsulates image data and provides an abstract method `process` to be overridden in derived classes.
    """

    def __init__(self, filename):
        """
        Initializes the class by loading an image using OpenCV.
        If the image cannot be loaded, an error is raised, ensuring that the object is always in a valid state.
        """
        # OpenCV API: `cv2.imread()`
        # Function: Reads an image from the specified file and returns it as a NumPy array. If the file cannot be opened,
        # it returns `None`. This function is commonly used to load images into memory for further processing.
        self.image = cv2.imread(filename)
        if self.image is None:
            raise ValueError(f'Error: Image {filename} not found!')

    # OOP Feature: Abstraction
    # Meaning:
    #   Abstraction is the concept of hiding complex implementation details and exposing only the necessary functionality to the user.
    #   This helps simplify the use of a class by providing a clear interface without exposing unnecessary complexity.
    # Use in this code:
    #   - The `process` method in `ImageProcessor` is abstract, meaning it provides a placeholder that forces subclasses to implement the actual functionality.
    #   - The base class does not define how the image will be processed; it leaves this for the derived classes to define, thus abstracting away the details.
    def process(self):
        raise ValueError(f'Subclasses should implement this!')

    def save_image(self, filename):
        """
        Saves the processed image to a specified file.
        The save functionality is encapsulated within the class, and it interacts with the image attribute.
        """
        # OpenCV API: `cv2.imwrite()`
        # Function: Writes an image to a file. The image is written in the format specified by the file extension (e.g., PNG, JPG).
        # This is used to save the processed image after applying various filters or transformations.
        cv2.imwrite(filename, self.image)

# OOP Feature: Inheritance
# Meaning:
#   Inheritance allows a new class (called a subclass or derived class) to inherit attributes and methods from another class (called a base class or parent class).
#   This promotes code reusability and hierarchical relationships between classes.
# Use in this code:
#   - The `GausianBlur` class inherits from `ImageProcessor` and reuses the constructor and save functionality from the parent class.
#   - By inheriting, `GausianBlur` gains access to the image loading and saving functionality without needing to redefine it.
#   - `GausianBlur` adds its own behavior by introducing a kernel size for Gaussian blur and overriding the `process` method.
class GausianBlur(ImageProcessor):
    """
    A derived class that implements Gaussian blur on the image.
    Inherits from the ImageProcessor class and overrides the abstract process method.
    """
    
    def __init__(self, filename, kernel):
        """
        Initializes the GaussianBlur class by calling the parent class's constructor to load the image,
        and adds an additional parameter `kernel` to define the blur intensity.
        """
        super().__init__(filename)  # Reuses the constructor of the base class to load the image
        self.kernel = kernel  # Adds a new attribute for kernel size

    # OOP Feature: Polymorphism
    # Meaning:
    #   Polymorphism allows methods with the same name to behave differently based on the object that is calling them.
    #   This can be achieved through method overriding, where a subclass provides a specific implementation of a method already defined in the parent class.
    # Use in this code:
    #   - The `process` method in the `GausianBlur` class overrides the abstract `process` method in the `ImageProcessor` class.
    #   - When `process` is called on an object of type `GausianBlur`, the specific implementation in this subclass is executed, applying a Gaussian blur to the image.
    def process(self):
        """
        Applies a Gaussian blur to the image using the kernel size provided during initialization.
        Overrides the abstract process method in the base class.
        """
        # OpenCV API: `cv2.GaussianBlur()`
        # Function: Applies a Gaussian blur to the image. This type of blur smooths the image by averaging pixel values
        # within a defined kernel size. The larger the kernel, the stronger the blur.
        self.image = cv2.GaussianBlur(self.image, (self.kernel, self.kernel), 0)

def read_image_from_directory(folder_path, filter_class, *filter_args):
    """
    This function reads images from a specified directory and processes them using a filter class derived from ImageProcessor.
    It demonstrates the flexibility of OOP by using polymorphism, allowing different filter classes to be passed in dynamically.
    
    Arguments:
    - folder_path: The directory containing the images to be processed.
    - filter_class: The class that defines how the images will be processed (e.g., GaussianBlur).
    - filter_args: Additional arguments to be passed to the filter class (e.g., kernel size for GaussianBlur).
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            file_path = os.path.join(folder_path, filename)

            try:
                # OOP Feature: Polymorphism in action
                # Here, filter_class can be any class derived from ImageProcessor.
                # This allows flexibility in using different types of image processing classes
                processor = filter_class(file_path, *filter_args)
                processor.process()  # The specific `process` method of the subclass is called
                output_folder = os.path.join(folder_path, f"processed_{filename}")
                processor.save_image(output_folder)
            except Exception as e:
                print(f"Failed to process {filename}: {e}")  # Handles errors gracefully

def browse_folder():
    """
    Opens a file dialog to allow the user to select a folder, and updates the folder_path variable with the selected path.
    """
    folder = filedialog.askdirectory()
    folder_path.set(folder)

def apply_gaussian_blur():
    """
    Applies Gaussian blur to all images in the selected folder using the kernel size specified by the user.
    This function calls read_image_from_directory and passes in the GausianBlur class to process the images.
    """
    read_image_from_directory(folder_path.get(), GausianBlur, int(kernel.get()))
    messagebox.showinfo("Success", "Gaussian blur applied to all images.")

# GUI setup using Tkinter
root = tk.Tk()
root.title("Image Processing Application")

# GUI elements for selecting folder and applying Gaussian blur
tk.Label(root, text="Select Folder:").grid(row=0, column=0, padx=10, pady=10)
folder_path = tk.StringVar()
tk.Entry(root, textvariable=folder_path, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Gaussian Blur:").grid(row=1, column=0, padx=10, pady=10)
kernel = tk.StringVar(value="5")
tk.Entry(root, textvariable=kernel, width=10).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Apply", command=apply_gaussian_blur).grid(row=1, column=2, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
