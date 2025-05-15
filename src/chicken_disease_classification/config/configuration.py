# This is an empty file for module: configuration.py
from src.chicken_disease_classification.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.chicken_disease_classification.utils.common import read_yaml, create_directories

from src.chicken_disease_classification.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__(self):
        self.config_file_path= CONFIG_FILE_PATH
        self.params_file_path= PARAMS_FILE_PATH

        self.config= read_yaml(CONFIG_FILE_PATH)
        self.params= read_yaml(PARAMS_FILE_PATH)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_configuration(self) -> DataIngestionConfig:
        config= self.config.data_ingestion

        create_directories([config.root_directory])

        data_ingestion_config= DataIngestionConfig(root_directory= config.root_directory \
                                                   , source_URL= config.source_URL \
                                                   , local_data_file= config.local_data_file\
                                                   ,unzip_dir= config.unzip_dir
                                                    )
        return data_ingestion_config
