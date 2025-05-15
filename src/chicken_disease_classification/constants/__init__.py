# This is an empty file for module: __init__.py
from pathlib import Path
import os

def get_current_file_directory():
    """Gets the directory of the current Python script."""
    return os.path.dirname(os.path.abspath(__file__))

root= os.getcwd()

# CONFIG_FILE_PATH= Path("./../config/config.yaml")
# PARAMS_FILE_PATH= Path("./../params.yaml")

CONFIG_FILE_PATH= Path(os.path.join(root,"config/config.yaml"))
PARAMS_FILE_PATH= Path(os.path.join(root,"params.yaml"))