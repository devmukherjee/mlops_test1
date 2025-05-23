# This is an empty file for module: configuration.py
from src.chicken_disease_classification.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.chicken_disease_classification.utils.common import read_yaml, create_directories
from pathlib import Path
from src.chicken_disease_classification.entity.config_entity import (DataIngestionConfig,
                                                                     PrepareBaseModelConfig,
                                                                     PrepareCallbacksConfig,
                                                                     TrainingConfig)
from ensure import ensure_annotations
import os

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

    def get_prepare_callbacks_config(self)-> PrepareCallbacksConfig :
        config= self.config.prepare_callbacks
        model_chkpt_dir= os.path.dirname(config.checkpoint_model_filepath)
        create_directories([Path(model_chkpt_dir),Path(config.tensorboard_root_log_dir)])

        prepare_callbacks_config = PrepareCallbacksConfig(
            root_directory=Path(config.root_directory),
            tensorboard_root_log_directory= Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath= Path(config.checkpoint_model_filepath)
        )
        return prepare_callbacks_config
    
    def training_config(self) -> TrainingConfig:
        training= self.config.training
        prepare_base_model= self.config.prepare_base_model
        params= self.params
        training_data= os.path.join(self.config.data_ingestion.unzip_dir,"Chicken-fecal-images")
        
        create_directories([Path(training.root_directory)])
        
        training_config= TrainingConfig(
            root_directory= Path(training.root_directory),
            trained_model_path= Path(training.model_file_path),
            updated_base_model_path= Path(prepare_base_model.updated_base_model_path),
            training_data= Path(training_data),
            params_epochs= params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )

        return training_config
