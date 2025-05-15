import os
from urllib import request
import zipfile
from src.chicken_disease_classification import logger
from src.chicken_disease_classification.utils.common import get_size
from src.chicken_disease_classification.entity.config_entity import DataIngestionConfig
from pathlib import Path

class DataIngestion:
    def __init__(self,config: DataIngestionConfig):
        self.config= config
    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            try:
                filename,headers= request.urlretrieve(
                    url= self.config.source_URL,
                    filename= self.config.local_data_file
                )
                logger.info(f"filename:{filename} downloaded with the following info  :File location: {os.path.abspath(filename)} \n {headers}")
            except Exception as e:
                logger.error(f"filename: {filename} download failed with Exception {e}")
        else:
             logger.info(f"filename {self.config.local_data_file} already exists with size: {get_size(Path(self.config.local_data_file))}")

    def extract_zip(self):
        """
        Extracts all files from a zip archive.

        Args:
            zip_file_path (str): The path to the zip file.
            extract_path (str, optional): The directory to extract the files to.
                Defaults to the current directory (".")
        """
        zip_file_path, extract_path= self.config.local_data_file,self.config.unzip_dir
        
        try:
        
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
            logger.info(f"Successfully extracted all files from '{zip_file_path}' to '{extract_path}'")
        except zipfile.BadZipFile:
            logger.error(f"Error: '{zip_file_path}' is not a valid zip file.")
        except FileNotFoundError:
            logger.error(f"Error: File not found at '{zip_file_path}'")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.debug("Exception details:", exc_info=True)  # Log detailed traceback

            


