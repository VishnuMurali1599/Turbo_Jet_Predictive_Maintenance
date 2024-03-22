import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

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
        
    def outlier_removal(self,data:pd.DataFrame):
        #data = pd.DataFrame(data)
        for i in data:
            percentile75 = data[i].quantile(0.75)
            percentile25 = data[i].quantile(0.25)
            iqr = percentile75 - percentile25
            min = (percentile25 - (1.5*iqr))
            max = (percentile75 + (1.5*iqr))
            return data[(data [i] < max)]
    
    def get_data_transformer_object(self):
        '''
        This function si responsible for data trnasformation
        
        '''
        try:
            numerical_column = self.numerical_columns

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
        
    def initiate_data_transformation(self,data_path):

        try:
            data=pd.read_csv(data_path)

            logger.info("Read train and test data completed")

            logger.info("Obtaining preprocessing object")
            
            ## This is separate and it is not dependent on above
            
            target_column_name="RUL"
            
            X = data.drop(columns=[target_column_name],axis=1)
            y = data[[target_column_name]]


            logger.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
            preprocessing_obj = self.get_data_transformer_object()
            
            threshold = 0  # Adjust the threshold as needed
            
            ##applying variance threshold feature selection technique()
            columns = X.var(axis=0)[X.var(axis=0) > threshold].index.tolist()
            print("columns is",columns)
            
            X = data.loc[:,columns]
            
            numerical_columns = columns
            self.numerical_columns.extend(numerical_columns)
            
            X = self.outlier_removal(X)
            # Target features outlier removal
            y = self.outlier_removal(y)
            
            ## From here Fitting of the object is taking place
            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.3,random_state=100)
            
            X_train_array = preprocessing_obj.fit_transform(X_train)
            logger.info("Train dataset array feature", X_train)
            X_test_array = preprocessing_obj.transform(X_test)


            train_arr = np.hstack((X_train_array, np.array(y_train)))
            test_arr = np.hstack((X_test_array, np.array(y_test)))


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
            raise (e,sys)
