import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

project_name= "chicken_disease_classification"
logger = logging.getLogger(__name__)

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    f"config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb"] 

for filepath in list_of_files:
    filepath= Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logger.info(f"Creating directory: {filedir}")
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, 'w') as f:
            if filename.endswith(".py"):
                f.write("# This is an empty file for module: " + filename)
            elif filename == "config.yaml":
                f.write("config:\n  key: value")
            elif filename == "dvc.yaml":
                f.write("stages:\n  stage_name:\n    cmd: python script.py")
            elif filename == "params.yaml":
                f.write("params:\n  key: value")
            elif filename == "requirements.txt":
                f.write("# Add your requirements here")
            elif filename == "setup.py":
                f.write("from setuptools import setup, find_packages\n\nsetup(name='project_name', version='0.1', packages=find_packages())")
            elif filename == "trials.ipynb":
                f.write("{\"cells\": [], \"metadata\": {}, \"nbformat\": 4, \"nbformat_minor\": 2}")
            logger.info(f"Creating file: {filepath}")

    else: logging.info(f"File already exists: {filepath}")