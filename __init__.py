import importlib
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

def get_module_list_from_directory(directory):
    directory_path = os.path.join(base_dir, directory)  # Verwende base_dir, um den vollen Pfad zum Verzeichnis zu erhalten
    files = os.listdir(directory_path)
    module_list = []

    for file in files:
        # Überprüft, ob die Datei eine .py-Datei ist und nicht __init__.py ist
        if file.endswith('.py') and file != "__init__.py":
            module_name = file[:-3]  # Entfernt .py am Ende
            module_list.append(f"{directory}.{module_name}")

    return module_list

node_list = get_module_list_from_directory("API_Nodes") + get_module_list_from_directory("Agents")



node_list += [
    "Chat",
    "TextOutput",
    "DisplayText",
    "DisplayTextAsImage",
    "Groupchat",
    "TextGeneration",
    "Conditioning",
    "Output2String",
    "LoadAPIconfig"
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module_name in node_list:
    imported_module = importlib.import_module(".{}".format(module_name), __name__)

    NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
    NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
