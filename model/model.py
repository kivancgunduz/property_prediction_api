import os
from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

import joblib


class Model():
    """
    A class that manage the model. 
    """
    def _init_(self) -> None:
        self.df: pd.DataFrame = pd.read_csv('./data/raw_data.csv')

    def check_dataset_file(self):
        """
        A Function that check the dataset file.
        """
        pass
    def create_model_file(self):
        """
        A Function that create a model file.
        """
        df = self.df
        y = df["Price"]
        X = df.drop(["Price"], axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2, random_state=0)
        scaler = StandardScaler()
        scaler.fit(X_train)
        features_scal = scaler.transform(X_train)


        regressor = LinearRegression()
        regressor.fit(X_train, y_train)
        print(regressor.score(X_train, y_train))


        predict = regressor.predict(X_train)
        print(regressor.score(X_test, y_test))

        joblib.dump(regressor, "model/model.pkl")

        model_columns = list(X.columns)

        joblib.dump(model_columns, "model/model_columns.pkl")
        print(X.columns)
    def manipulate_dataset(self):
        """
        A Function that manipulate the dataset.
        """
        pass
    
    def train_model(self):
        """
        A Function that train the model.
        """
        pass

    

    def check_performance(self):
        """
        A Function that check the performance of the model.
        """
        pass