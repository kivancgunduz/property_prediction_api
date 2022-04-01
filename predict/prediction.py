import pickle
from flask import jsonify
import pandas as pd


class Prediction:
    """

    """
    def __init__(self) -> None:
        pass
    
    def predict(self, ready_df: pd.DataFrame) -> dict:
        try:
            model = pickle.load(open('./model/model.pkl', 'rb'))
            prediction_price = int(model.predict(self.df)[0])
        except Exception as e:
            print(e)
            return jsonify({'error': e}), 500
        else:
            return jsonify({'message': 'The price is: {}'.format(prediction_price)})
