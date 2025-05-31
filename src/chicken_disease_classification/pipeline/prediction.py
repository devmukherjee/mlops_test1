import torch
import torch.nn as nn
from torchvision.io import decode_image
from torchvision.transforms.functional import resize
from PIL import Image
from src.chicken_disease_classification.constants import prediction_preprocessing_transform, CONFIG_FILE_PATH,PARAMS_FILE_PATH,class_names
from dataclasses import dataclass
from pathlib import Path
from src.chicken_disease_classification.utils.common import read_yaml,create_directories

@dataclass
class PredictionConfig():
    final_model_path: Path

class PredictionConfigManager():
    def __init__(self,config_file_path, params_file_path):
        self.config= read_yaml(config_file_path)
        self.params= read_yaml(params_file_path)

    def get_prediction_config(self)->PredictionConfig :
        final_model_path= Path(self.config.training.model_file_path)
        return PredictionConfig(final_model_path= final_model_path)

      
class Prediction():
    def __init__(self, config:PredictionConfig):
        self.config= config

    def predict(self,file_path):
        image_file_path= file_path
        image_pil= self.fetch_image(image_path= image_file_path)
        preprocessed_image_tensor= self.prepocess_image(pil_image=image_pil)
        model= Prediction.load_model(model_path= self.config.final_model_path)

        output= model(preprocessed_image_tensor)
        _,prediction_class_index=torch.max(output,1)
        
        final_prediction= class_names[prediction_class_index]
        return final_prediction



    @staticmethod    
    def load_model(model_path):
        model= torch.load(model_path, weights_only= False)
        return model
        # print(f"Type of the first layer's output: {type(self.model.layers[0].output)}")


    
    @staticmethod
    def fetch_image(image_path):
        image_pil= Image.open(image_path)
        return image_pil


    @staticmethod
    def prepocess_image(pil_image: Image.Image):
        return prediction_preprocessing_transform(pil_image)
    
class PredictionPipeline():
    def __init__(self):
        configuration_manager= PredictionConfigManager(config_file_path=CONFIG_FILE_PATH
                                                       ,params_file_path=PARAMS_FILE_PATH)
        prediction_config_entity= configuration_manager.get_prediction_config()

        prediction_component= Prediction(config= prediction_config_entity)

        self.prediction_component= prediction_component
    
    def predict(self,image):
        return self.prediction_component.predict(image)


        




