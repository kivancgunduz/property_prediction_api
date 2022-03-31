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

    def create_model_file(self):
        """
        A Function that create a model file.
        """
        pass

    def check_performance(self):
        """
        A Function that check the performance of the model.
        """
        pass