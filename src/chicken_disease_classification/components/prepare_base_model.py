import os
import urllib.request as request
from zipfile import ZipFile
import torch
import torch.nn as nn
import torchvision
# import keras
from src.chicken_disease_classification import logger

from pathlib import Path
from src.chicken_disease_classification.entity.config_entity import PrepareBaseModelConfig

class PrepareBaseModel:
    def __init__(self,config:PrepareBaseModelConfig):        
        self.config= config

    def get_base_model(self):
        self.model= torchvision.models.resnet18(pretrained= True)
        self.save_model(path= self.config.base_model_path, model= self.model)

    @staticmethod
    def _prepare_full_model(model,classes,learning_rate):
        
        model_conv=model
        #Initially we drop the gradients for all model parameters. 
        for param in model.parameters():
            param.requires_grad= False

        # Parameters of newly constructed modules have requires_grad=True by default
        num_features= model_conv.fc.in_features
        model_conv.fc= nn.Linear(num_features,classes)     
        
        return model_conv
    
    def update_base_model(self):
        self.full_model= self._prepare_full_model(model= self.model,
                                                 classes= self.config.params_classes,
                                                 learning_rate= self.config.params_learning_rate) 
        self.save_model(path= self.config.updated_base_model_path, model= self.full_model)
  
    @staticmethod
    def save_model(path: Path,model):
        torch.save(model,path)

