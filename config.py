import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
venv_site_packages = os.path.join(base_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(venv_site_packages)
