import importlib
import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))

def install_package():
    # Navigate to the NodeGPT directory
    os.chdir(base_dir)

    # Run the install.bat file
    subprocess.run('install.bat', shell=True)

    venv_activate = ".\\venv\\Scripts\\activate"
    requirements_install = "pip install -r requirements.txt"

    subprocess.run(f"{venv_activate} && {requirements_install}", shell=True)#, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def update_repository(repo_path):
    try:
        # Navigate to the repository directory
        os.chdir(repo_path)

        # Execute 'git pull' command
        result = subprocess.run(['git', 'pull'], check=True)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())

    except Exception as e:
        print(f"An error occurred while updating the repository: {e}")
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