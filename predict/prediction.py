import pickle
from flask import jsonify
import joblib
import pandas as pd


class Prediction:
    """
    A class that generate the prediction from model.
    """
    def __init__(self) -> None:
        """
        A function that initialize the class.
        """
        pass
    
    def predict(self, ready_df: pd.DataFrame) -> dict:
        try:
            model = joblib.load(open('./model/model.pkl', 'rb'))
            prediction_price = int(model.predict(ready_df)[0])
        except Exception as e:
            print(e)
            return "Error"
        else:
            return prediction_price
