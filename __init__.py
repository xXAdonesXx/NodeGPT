import importlib
import os
import subprocess
import json


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

def install_package():
    # Navigate to the NodeGPT directory
    os.chdir(base_dir)

    # Run the install.bat file
    subprocess.run('install.bat', shell=True)

    venv_activate = ".\\venv\\Scripts\\activate"
    requirements_install = "pip install -r requirements.txt"

    subprocess.run(f"{venv_activate} && {requirements_install}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def read_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def update_repository(repo_path):
    try:
        # Navigate to the repository directory
        os.chdir(repo_path)

        # Execute 'git pull' command
        result = subprocess.run(['git', 'pull'], check=True)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())

    except Exception as e:
        print(f"An error occurred while updating the repository: {e}")

auto_update_path = os.path.join(base_dir, 'AutoUpdate.json')
print(auto_update_path)
config = read_config(auto_update_path)
auto_update = config.get('AutoUpdate', False)



if auto_update:
    try:
        update_repository(base_dir)
        print("NodeGPT updated")
    except Exception as e:
        print(f"An error occurred during installation: {e}")
    try:
        install_package()
        print("Requirements updated")
    except Exception as e:
        print(f"An error occurred during installation: {e}")


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
    "LoadAPIconfig",
    "LoadTXT",
    "llava"
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module_name in node_list:
    imported_module = importlib.import_module(".{}".format(module_name), __name__)

    NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
    NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
