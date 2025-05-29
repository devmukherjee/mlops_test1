import torch
import torch.nn as nn
from torchvision.transforms import transforms
import numpy as np
# from zipfile import ZipFile
import urllib.request as request
import os
import time
from pathlib import Path
from src.chicken_disease_classification.entity.config_entity import ModelEvaluationConfig
# import torch.optim.lr_scheduler as lr_scheduler
from torchvision.datasets import ImageFolder
# from torch.utils.data.dataloader import DataLoader
import copy
from src.chicken_disease_classification import logger
from src.chicken_disease_classification.utils.common import save_json

class Evaluation:
    def __init__(self,evaluation_config: ModelEvaluationConfig):
        self.config= evaluation_config

    def load_model(self,model_path):
        self.model= torch.load(model_path,weights_only= False)

    def preprocess_data(self):
        mean= np.array([0.5,0.5,0.5])
        std= np.array([0.25,0.25,0.25])

        self.data_transforms= {
            'train': transforms.Compose([ transforms.RandomResizedCrop(224),
                                        transforms.RandomHorizontalFlip(1),
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean,std)]),
            'val':transforms.Compose([transforms.Resize(256),
                                    transforms.CenterCrop(224),
                                    transforms.ToTensor(),
                                    transforms.Normalize(mean= mean,std= std)])
        }

        data_root= self.config.training_data

        self.testing_dataset=ImageFolder(root= os.path.join(data_root,'val'),\
                                            transform= self.data_transforms['val'])
    
        self.test_image_dataloader= torch.utils.data.DataLoader(dataset= self.testing_dataset,\
                                                        batch_size= self.config.params_batch_size, 
                                                        shuffle= False)

        self.dataset_size = len(self.testing_dataset) 
        self.class_names = self.testing_dataset.classes

    def build_additional_parameters(self):
       self.criterion= nn.CrossEntropyLoss()

    @staticmethod
    def evaluation(model,criterion,dataloader,dataset_size):
        # Get model filepath
        running_loss= 0.0
        running_corrects= 0.0
        
        for inputs,labels in dataloader:
            with torch.no_grad():
                outputs= model(inputs)
                _,predictions=torch.max(outputs,1)
                loss= criterion(outputs,labels)

            #statistics:
            running_loss+= loss.item()*inputs.size(0)
            running_corrects+= torch.sum(predictions==labels.data)
        
        epoch_loss= running_loss/dataset_size
        epoch_accuracy= running_corrects/dataset_size

        logger.info(msg='Loss: {:.4f} Acc: {:.4f}'.format(epoch_loss, epoch_accuracy))

        metrics_dict= dict(loss= epoch_loss,accuracy=epoch_accuracy.item())

        return metrics_dict
    
    @staticmethod
    def save_metrics(metrics_dict,path):
        save_json(path=path,data= metrics_dict)