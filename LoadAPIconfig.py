import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(base_dir, 'API_Configs')
'''
def import_from_two_dirs_up(module_name):
    try:
        two_dirs_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        if two_dirs_up not in sys.path:
            sys.path.append(two_dirs_up)

        module = __import__(module_name)
        return module

    except ImportError:
        print(f"Failed to import {module_name} from {two_dirs_up}.")
        return None

your_module = import_from_two_dirs_up('folder_paths')
'''


def get_filename_list(folder_name, extension="txt"):
    try:
        # Ensure that the folder exists
        if not os.path.exists(folder_name):
            print(f"The folder {folder_name} does not exist.")
            return []

        # List all files in the folder
        all_files = os.listdir(folder_name)

        # Filter files based on the extension
        return [file for file in all_files if file.endswith(f".{extension}")]

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


class LoadAPIconfig:
    #if your_module:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "API_KEY": (get_filename_list(folder_path, "txt"), ),
                             }}
    RETURN_TYPES = ("STRING",)
    FUNCTION = "load"

    CATEGORY = "AutoGen"

    def load(self, API_Key):
        with open(os.path.join(folder_path, API_Key), 'r') as file:
            API = file.read().strip()
        return API
    #pass
NODE_CLASS_MAPPINGS = {
    "LoadAPIconfig": LoadAPIconfig,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadAPIconfig": "Load API config"
}
