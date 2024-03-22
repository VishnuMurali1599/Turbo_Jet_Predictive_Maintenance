import sys
import pandas as pd
from src.utils import load_object
import os
from pymongo.mongo_client import MongoClient

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join('artifacts','proprocessor.pkl')
            print("Before Loading")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise (e,sys)



class CustomData:
    def __init__(  self,
        cycle: float,
        op1: float,
        op2: float,
        sensor2:float,
        sensor3: float,
        sensor4:float,
        sensor5: float,
        sensor6:float,
        sensor7: float,
        sensor8:float,
        sensor9: float,
        sensor10:float,
        sensor11: float,
        sensor12: float,
        sensor13:float,
        sensor14: float,
        sensor15:float,
        sensor16: float,
        sensor17:float,
        sensor20: float,
        sensor21:float):

        self.cycle = cycle

        self.op1 = op1
        
        self.op2 = op2

        self.sensor2 = sensor2

        self.sensor3 = sensor3

        self.sensor4 = sensor4

        self.sensor5 = sensor5

        self.sensor6 = sensor6
        
        self.sensor7 = sensor7

        self.sensor8 = sensor8

        self.sensor9 = sensor9

        self.sensor10 = sensor10

        self.sensor11 = sensor11

        self.sensor12 = sensor12

        self.sensor13 = sensor13
        
        self.sensor14 = sensor14

        self.sensor15 = sensor15

        self.sensor16 = sensor16

        self.sensor17 = sensor17
        
        self.sensor20 = sensor20

        self.sensor21 = sensor21


    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "cycle": [self.cycle],
                "op1": [self.op1],
                "op2": [self.op2],
                "sensor2": [self.sensor2],
                "sensor3": [self.sensor3],
                "sensor4": [self.sensor4],
                "sensor5": [self.sensor5],
                "sensor6": [self.sensor6],
                "sensor7": [self.sensor7],
                "sensor8": [self.sensor8],
                "sensor9": [self.sensor9],
                "sensor10": [self.sensor10],
                "sensor11": [self.sensor11],
                "sensor12": [self.sensor12],
                "sensor13": [self.sensor13],
                "sensor14": [self.sensor14],
                "sensor15": [self.sensor15],
                "sensor16": [self.sensor16],
                "sensor17": [self.sensor17],
                "sensor20": [self.sensor20],
                "sensor21": [self.sensor21]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise (e, sys)
