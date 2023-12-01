import sys
import os


class LoadTXT:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"default": "log.txt"}),
                "path": ("STRING", {"default": "path"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "load"

    CATEGORY = "AutoGen"

    def load(self, name, path):
        # Open the text file for reading
        file_path = os.path.join(path, name)
        try:
            with open(file_path, 'r') as file:
                # Read the entire contents of the file into a string
                file_contents = file.read()
                #print("File contents as a string:")
                #print(file_contents)
        except:
            os.makedirs(path)
            with open(file_path, 'w') as file:
                pass
            file_contents = ""
        return (file_contents,)

NODE_CLASS_MAPPINGS = {
    "LoadTXT": LoadTXT,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadTXT": "LoadTXT"
}
