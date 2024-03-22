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
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        self.numerical_columns = []

    def outlier_removal(self, data: pd.DataFrame):
        # data = pd.DataFrame(data)
        for i in data.columns:
            percentile75 = data[i].quantile(0.75)
            percentile25 = data[i].quantile(0.25)
            iqr = percentile75 - percentile25
            min_val = (percentile25 - (1.5 * iqr))
            max_val = (percentile75 + (1.5 * iqr))
            return data[(data[i] < max_val)]

    def get_data_transformer_object(self):
        try:
            numerical_column = self.numerical_columns

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # Imputation
                    ('feature_selection', VarianceThreshold(threshold=0)),  # Feature Selection
                    ("scaler", StandardScaler())  # Feature Engineering
                ]
            )

            logger.info(f"Numerical columns:{numerical_column}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_column)
                ]
            )

            return preprocessor

        except Exception as e:
            raise Exception("An error occurred while creating the preprocessor.", e)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info("Read train and test data completed")

            logger.info("Obtaining preprocessing object")

            target_column_name = "RUL"
            numerical_columns = self.numerical_columns

            threshold = 0  # Adjust the threshold as needed
            train_columns = train_df.var(axis=0)[train_df.var(axis=0) > threshold].index.tolist()
            test_columns = test_df.var(axis=0)[test_df.var(axis=0) > threshold].index.tolist()

            self.numerical_columns.extend(train_columns)

            preprocessing_obj = self.get_data_transformer_object()

            # Part 2
            train_df = pd.read_csv(train_path, usecols=train_columns)
            test_df = pd.read_csv(test_path, usecols=test_columns)

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Ensure 'RUL' column is included in the input features
            input_feature_train_df['RUL'] = target_feature_train_df

            # Now, drop 'RUL' from the input feature dataframe
            input_feature_train_df = input_feature_train_df.drop(columns=[target_column_name], axis=1)

            logger.info("Applying preprocessing object on training dataframe and testing dataframe.")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]

            logger.info("Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return train_arr, self.data_transformation_config.preprocessor_obj_file_path

        except Exception as e:
            raise Exception("An error occurred during data transformation.", e)


# Example usage
data_transformation = DataTransformation()
train_data_path = "path/to/train.csv"
test_data_path = "path/to/test.csv"
train_arr, preprocessor_file_path = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
