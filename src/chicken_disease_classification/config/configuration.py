# This is an empty file for module: configuration.py
from src.chicken_disease_classification.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.chicken_disease_classification.utils.common import read_yaml, create_directories
from pathlib import Path
from src.chicken_disease_classification.entity.config_entity import DataIngestionConfig,PrepareBaseModelConfig
from ensure import ensure_annotations

class ConfigurationManager:
    def __init__(self,
                config_file_path,
                params_file_path):
        self.config= read_yaml(config_file_path)
        self.params= read_yaml(params_file_path)
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
    
    @ensure_annotations
    def get_prepare_base_model_config(self)-> PrepareBaseModelConfig: 
        config= self.config.prepare_base_model

        create_directories([config.root_directory])

        prepare_base_model_config= PrepareBaseModelConfig(
            root_dir= Path(config.root_directory),
            base_model_path= Path(config.base_model_path),
            updated_base_model_path= Path(config.updated_base_model_path),
            params_image_size= self.params.IMAGE_SIZE,
            params_learning_rate= self.params.LEARNING_RATE,
            params_include_top= self.params.INCLUDE_TOP,
            params_weights= self.params.WEIGHTS,
            params_classes= self.params.CLASSES
        )

        return prepare_base_model_config
