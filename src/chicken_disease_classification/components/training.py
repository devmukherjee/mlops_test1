import torch
import torch.nn as nn
from torchvision.transforms import transforms
import numpy as np
from zipfile import ZipFile
import urllib.request as request
import os
import time
from pathlib import Path
from src.chicken_disease_classification.entity.config_entity import TrainingConfig
import torch.optim.lr_scheduler as lr_scheduler
from torchvision.datasets import ImageFolder
from torch.utils.data.dataloader import DataLoader
import copy
class Training:
    def __init__(self,config: TrainingConfig):
        self.config= config

    def get_base_model(self):
        self.model= torch.load(
            self.config.updated_base_model_path, weights_only= False
            )
        # print(f"Type of the first layer's output: {type(self.model.layers[0].output)}")
        
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

        self.image_datasets={x:ImageFolder(root= os.path.join(data_root,x),\
                                            transform= self.data_transforms[x])
                                                for x in ['train','val'] }
        self.image_dataloaders= {x:torch.utils.data.DataLoader(dataset= self.image_datasets[x],\
                                                        batch_size= self.config.params_batch_size, 
                                                        shuffle= (True if x=='train'else False))\
                                                        for x in ['train','val']}

        self.dataset_sizes = {x: len(self.image_datasets[x]) for x in ['train', 'val']}
        self.class_names = self.image_datasets['train'].classes
                


    def build_additional_parameters(self):
        self.criterion= nn.CrossEntropyLoss()

        # Observe that only parameters of final layer are being optimized as
        # opposed to before.
        self.optimiser_conv= torch.optim.SGD(self.model.fc.parameters(),lr=0.01,momentum=0.9)

        # Decay LR by a factor of 0.1 every 7 epochs
        self.exp_decay_lr_scheduler= lr_scheduler.StepLR(optimizer= self.optimiser_conv,step_size= 7, gamma=0.1)

    
    @staticmethod
    def save_model(path: Path, model):
        torch.save(model,path)

    @staticmethod
    def train_model(model,dataloaders,criterion,optimiser,scheduler,dataset_sizes,num_epochs= 25):
        since= time.time()

        best_model_weights= copy.deepcopy(model.state_dict())

        best_acc= 0.0

        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            for phase in ['train','val']:
                if phase=='train':
                    model.train()
                else:
                    model.eval()

                running_loss= 0.0
                running_corrects= 0.0

                #Iterate over the data
                for inputs,labels in dataloaders[phase]:
                    ##Forward pass
                    # Track history 
                    
                    # We have to first unfreeze the gradients because we will be using an 
                    # already trained model
                    with torch.set_grad_enabled(phase=='train'):
                        outputs= model(inputs)
                        _,predictions=torch.max(outputs,1)
                        loss= criterion(outputs,labels)

                        #optimise only in training phase
                        # backward +optimise
                        if(phase=='train'):
                            optimiser.zero_grad()
                            loss.backward()
                            optimiser.step()

                    #statistics:
                    running_loss+= loss.item()*inputs.size(0)
                    running_corrects+= torch.sum(predictions==labels.data)
                
                if phase=='train':
                    scheduler.step()
                
                epoch_loss= running_loss/dataset_sizes[phase]
                epoch_acc= running_corrects/dataset_sizes[phase]

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))
                
                #deepcopy the model
                if phase=='val' and epoch_acc > best_acc:
                    best_model_weights= copy.deepcopy(model.state_dict())
                    best_acc= epoch_acc
                print()

        time_elapsed= time.time() -since
        print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))

        print('Best val Acc: {:4f}'.format(best_acc))

        #load the model with best weights
        model.load_state_dict(best_model_weights)
        return model
    
    @staticmethod
    def save_model(path: Path,model):
        torch.save(model,path)

