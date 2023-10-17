import json
import sys
sys.path.append("x:\\programme\\python\\lib\\site-packages")

from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
class DisplayTextAsImage:
    def __init__(self):
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("TEXT",),
            },
            "hidden": {},
        }

    RETURN_TYPES = ()
    FUNCTION = "display_text_as_image"

    OUTPUT_NODE = True

    CATEGORY = "AutoGen"

    def display_text_as_image(self, text):

        text = text['LOG']

        # Check if the first key of the dictionary is a string representation of a list
        if isinstance(list(text.keys())[0], str):
            # Convert the string representation to an actual list
            content_list_str = list(text.keys())[0]
            content_list = json.loads(content_list_str)
        else:
            raise ValueError("Unexpected format of 'text'")

        # Extract the content from each dictionary in the list
        all_contents = [item['content'] for item in content_list if 'content' in item]

        # Get the last content from the list (or None if the list is empty)
        last_content = all_contents[-1] if all_contents else None
        print(last_content)

        # Generate image from the text
        img = Image.new('RGB', (300, 50), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.load_default()  # Using default font, can be replaced with custom font if needed
        d.text((10, 10), last_content, font=fnt, fill=(0, 0, 0))

        # Save the image
        self.output_dir = "X:\Anton\Pictures\Text2Image\Programme\ComfyUI\ComfyUI\ComfyUI\output"
        filename_prefix = "ComfyUI"
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, img.width,
            img.height)  # Assuming folder_paths.get_save_image_path is defined elsewhere

        file = f"{filename}_{counter:05}_.png"
        img.save(os.path.join(full_output_folder, file), compress_level=4)

        return {"ui": {"images": [{"filename": file, "subfolder": subfolder, "type": self.type}]}}

class folder_paths:
    @staticmethod
    def get_output_directory():
        return "/mnt/data/"

    @staticmethod
    def get_save_image_path(prefix, dir, width, height):
        # Simplified logic for demonstration, should be replaced with actual logic
        return (dir, prefix, 1, "", prefix)


NODE_CLASS_MAPPINGS = {
    "DisplayTextAsImage": DisplayTextAsImage,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "DisplayTextAsImage": "DisplayTextAsImage"
}