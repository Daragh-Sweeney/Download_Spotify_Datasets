from PIL import Image
import os

path = 'projects/images/edm_dance'
output_path = 'projects/re-images/edm_dance/'  # Note the trailing slash for the directory

def resize(width, height):
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            img = Image.open(os.path.join(path, item))
            new_image = img.resize((width, height))
            new_file_name = 'resized-' + item

            try:
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                new_image.save(os.path.join(output_path, new_file_name))
            except:
                print("An exception occurred")

resize(64, 64)