import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.logger import logger
import os
from sklearn.feature_selection import VarianceThreshold

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
        self.numerical_columns = []
        
    def outlier_removal(self, data:pd.DataFrame) -> pd.DataFrame:
        for i in data.columns:
            percentile75 = data[i].quantile(0.75)
            percentile25 = data[i].quantile(0.25)
            iqr = percentile75 - percentile25
            min = (percentile25 - (1.5*iqr))
            max = (percentile75 + (1.5*iqr))
            data = data[(data [i] >= min) & (data [i] <= max)]
            return data
        
    
    def get_data_transformer_object(self):
        try:
            #self.initiate_data_transformation()
            
            numerical_column = ['cycle','op1','op2','sensor2','sensor3','sensor4','sensor5',
                                'sensor6','sensor7','sensor8','sensor9','sensor11','sensor12',
                                'sensor13','sensor14','sensor15','sensor16','sensor17','sensor20',
                                'sensor21']

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")), ### imputation
                ('feature_selection',VarianceThreshold(threshold=0)), ## Feature Selection
                ("scaler",StandardScaler()) ## Feature Engineering
                ]
            )
            
            logger.info(f"Numerical columns:{numerical_column}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_column)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise (e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)  ## Calling main dataframe and forming train_data
            test_df=pd.read_csv(test_path)   ## calling main dataframe and forming test_data

            logger.info(f"Read train and test data completed")
            
            logger.info(f"Selecting new column by applying variance threshold")

            ##applying variance threshold feature selection technique()
            threshold = 0
            train_df_columns = train_df.var(axis=0)[train_df.var(axis=0) > threshold].index.tolist()
            test_df_columns = train_df.var(axis=0)[train_df.var(axis=0) > threshold].index.tolist()
            logger.info(f"From this we got the variance threshold columns ")
            logger.info(f"train columns after applying variance threshold {train_df_columns}")
            logger.info(f"train columns after applying variance threshold {test_df_columns}")
            logger.info(f"Variance threshold frequency is completed and column is selected")

            ## Whatever the columns we are getting after applying variance threshold from that we are creating new column
            train_df = train_df.loc[:,train_df_columns]
            logger.info(f"Creating new data frame after applying threshold {train_df.shape}")
            test_df = test_df.loc[:,test_df_columns]
            logger.info(f"Creating new data frame after applying threshold {test_df.shape}")
            print(train_df.shape)
            print(test_df.shape)

            ## Applying outliers function to new dataframe obtained after applying variance threshold
            train_df =self.outlier_removal(train_df)
            logger.info(f"After applying outlier removal remmaing rows is :{train_df.shape}")
            test_df = self.outlier_removal(test_df)
            logger.info(f"After applying outlier removal remmaing rows is :{test_df.shape}")
            print(train_df.shape)
            print(test_df.shape)
            
            ## here we are splliting the data into train test features after applying variance threshold freequency
            logger.info(f"Splitting the data into train and test data")
            target_column_name="RUL"
            input_feature_train_df = train_df.drop(columns=target_column_name,axis=1)
            target_feature_train_df = train_df.loc[:,[target_column_name]]
            input_feature_test_df = test_df.drop(columns=target_column_name,axis=1)
            target_feature_test_df = test_df.loc[:,[target_column_name]]
            logger.info(f"Train and test split is completed")

            print(input_feature_train_df.shape)
            print(target_feature_train_df.shape)
            print(input_feature_test_df.shape)
            print(target_feature_test_df.shape)
            print(input_feature_train_df.columns)

            #numerical_columns = input_feature_train_df.columns.tolist()
            #self.numerical_columns = input_feature_train_df.columns
            
            logger.info(f"Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()
            
            logger.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
            
            logger.info(
                "entering into input feature train_array and input _test array"
            )
            
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            logger.info(f"array data of train preprocessing data")
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            logger.info(f"array data of test preprocessing data")

            print(input_feature_train_arr.shape)
            print(target_feature_train_df.shape)
            print(input_feature_test_arr.shape)
            print(target_feature_test_df.shape)
            
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logger.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
            
        except Exception as e:
            raise (e)



        
