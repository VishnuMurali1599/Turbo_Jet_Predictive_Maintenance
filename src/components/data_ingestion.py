from pymongo.mongo_client import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import os

from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class data_ingestion:
    
    def __init__(self,dbname:str,collectionanme:str):
        self.__password = "Vishnu8748803252"
        self.dbname = dbname
        self.collection_name = collectionanme
        self.ingestion_config=DataIngestionConfig()
        
    def RUL_calculator(self,df, df_max_cycles):
            max_cycle = df_max_cycles["cycle"]
            result_frame = df.merge(max_cycle.to_frame(name='max_cycle'), left_on='id', right_index=True)
            result_frame["RUL"] = result_frame["max_cycle"] - result_frame["cycle"]
            result_frame.drop(['max_cycle'], axis=1, inplace=True)
            return result_frame
    
    def extraction(self):
        uri = "mongodb+srv://vishnumurali835:{}@vishnumurali.gan12f1.mongodb.net/?retryWrites=true&w=majority".format(self.__password)
        # Create a new client and connect to the server
        client = MongoClient(uri)
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        database=client[self.dbname]
        collection = database[self.collection_name]
        record=collection.find()
        for i in record:
            df = pd.DataFrame(i)
            df.drop(columns = ['_id','sensor22','sensor23'],axis=1,inplace = True)
            df_rlu = df.groupby(['id'])[["id" ,"cycle"]].max()
            
            ## now the data is ingested and want to add RUL as output based on the input cycle
            df = self.RUL_calculator(df,df_rlu)
            df.drop(columns=['id'],inplace=True)
            #print(df)
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)   
            
            return(
                   self.ingestion_config.train_data_path,
                   self.ingestion_config.test_data_path
                )
        
        
    
if __name__ =="__main__":
    obj = data_ingestion("PM",'predictive')
    #obj.extraction()
    train_data,test_data=obj.extraction()
    
    data_transformation=DataTransformation()
    #train_arr,test_arr=data_transformation.initiate_data_transformation(train_data)
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
    
    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))