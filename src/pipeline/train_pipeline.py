from src.components.data_ingestion import data_ingestion

from src.components.data_transformation import DataTransformation

from src.components.model_trainer import ModelTrainer

#from src.components.model_evaluation import ModelEvaluation


import os
import sys
from src.logger import logging
#from src.exception import customexception
import pandas as pd
class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            obj = data_ingestion("PM",'predictive')
            train_data_path,test_data_path=obj.extraction()
            return train_data_path,test_data_path
        except Exception as e:
            raise (e,sys)
        
    def start_data_transformation(self,train_data_path,test_data_path):
        
        try:
            data_transformation = DataTransformation()
            train_arr,test_arr=data_transformation.initiate_data_transformation(train_data_path,test_data_path)
            return train_arr,test_arr
        except Exception as e:
            raise (e,sys)
    
    def start_model_training(self,train_arr,test_arr):
        try:
            model_trainer=ModelTrainer()
            model_trainer.initiate_model_trainer(train_arr,test_arr)
        except Exception as e:
            raise (e,sys)
                
    def start_trainig(self):
        try:
            train_data_path,test_data_path=self.start_data_ingestion()
            train_arr,test_arr=self.start_data_transformation(train_data_path,test_data_path)
            self.start_model_training(train_arr,test_arr)
        except Exception as e:
            raise (e,sys)