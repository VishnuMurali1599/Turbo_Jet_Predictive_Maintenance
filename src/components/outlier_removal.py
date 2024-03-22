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
