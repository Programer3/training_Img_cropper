import os
from PIL import Image
import numpy as np

def crop_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    
    # Crop the image into four parts
    top_left = image.crop((0, 0, 512, 512))
    top_right = image.crop((width - 512, 0, width, 512))
    bottom_left = image.crop((0, height - 512, 512, height))
    bottom_right = image.crop((width - 512, height - 512, width, height))
    
    return top_left, top_right, bottom_left, bottom_right

# Ask the user for the output file name
output_name = input("Enter the name for the output files: ")
if not output_name:
    output_name = "output"

# Specify the folder containing the images
folder_path = 'C:/Users/amank/Downloads/grids_Is-Holm'

# Create the 'cropped' folder if it doesn't exist
output_folder = os.path.join(os.path.dirname(__file__), 'cropped')
os.makedirs(output_folder, exist_ok=True)

# Iterate over the images in the folder
images_done = 0
file_number = 1
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(folder_path, filename)
        
        # Crop the image
        crops = crop_image(image_path)
        
        # Save the cropped parts
        for crop in crops:
            # Generate the output file name
            output_file_name = f"{output_name} ({file_number}).png"
            crop_path = os.path.join(output_folder, output_file_name)
            crop.save(crop_path)
            file_number += 1
        
        images_done += 1
        print(f"images_done: {images_done}")