# This is an empty file for module: __init__.py
import os
import logging

import sys

logging_str= "%(asctime)s - %(levelname)s - %(message)s"
log_dir= os.path.join(os.getcwd(), "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok= True)
    logging.info(f"Creating directory: {log_dir}")

log_file_path= os.path.join(log_dir, "running_logs.log")

logging.basicConfig(
    level= logging.INFO,
    format= logging_str,
    handlers= [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(filename= log_file_path, mode= "a+")
    ]
) 

logger= logging.getLogger("chicken_disease_classification_logger")