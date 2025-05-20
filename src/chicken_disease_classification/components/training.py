import tensorflow as tf
import numpy as np
from zipfile import ZipFile
import urllib.request as request
import os
import time
from pathlib import Path
from src.chicken_disease_classification.entity.config_entity import TrainingConfig
from src.chicken_disease_classification.utils.image_preproc import resize_image
from src.chicken_disease_classification.utils.common import one_hot_encode

class Training:
    def __init__(self,config: TrainingConfig):
        self.config= config

    def get_base_model(self):
        self.model= tf.keras.models.load_model(
            self.config.updated_base_model_path
            )
        # print(f"Type of the first layer's output: {type(self.model.layers[0].output)}")
        
    def preprocess_datasets(self,dataset):
        resized_dataset= dataset.map(resize_image)
        one_hot_encoded_dataset= resized_dataset.map(one_hot_encode)
        return one_hot_encoded_dataset


    def train_valid_generator(self):
        
        validation_dataset_kwargs= dict(
            directory= self.config.training_data,
            subset="validation",
            shuffle= False,
            validation_split= 0.20,
            image_size= self.config.params_image_size[:-1],
            batch_size= self.config.params_batch_size,
            interpolation='bilinear'
        )

       
        validation_dataset= tf.keras.preprocessing.image_dataset_from_directory(**validation_dataset_kwargs)
        self.validation_dataset= self.preprocess_datasets(validation_dataset)
        
        
        if self.config.params_is_augmentation:
            train_dataset_kwargs= dict(
                directory= self.config.training_data,
                subset= 'training',
                shuffle= True,
                validation_split= 0.20,
                seed= 1442
            )
            
            train__dataset= tf.keras.preprocessing.image_dataset_from_directory(**train_dataset_kwargs)
        else:
            train__dataset= validation_dataset

        self.train_dataset= self.preprocess_datasets(train__dataset)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    def train(self, callback_list: list):
        self.steps_per_epoch= len(self.train_dataset)//self.config.params_batch_size
        self.validation_steps= len(self.validation_dataset)//self.config.params_batch_size
        
        print(tf.executing_eagerly())
        self.model.fit(
            x=self.train_dataset,
            epochs= self.config.params_epochs,
            steps_per_epoch= self.steps_per_epoch,
            validation_steps= self.validation_steps,
            validation_data= self.validation_dataset,
            callbacks= callback_list

        )

        self.save_model(
            path= self.config.trained_model_path,
            model= self.model
        )