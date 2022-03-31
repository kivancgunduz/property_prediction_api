import json
import os


from flask import Flask
from flask import Flask, request, jsonify

from predict.prediction import Prediction
from preprocessing.cleaning_data import Preprocessing
#from model.model import Model


app = Flask(__name__)
@app.route('/', methods=['GET'])
def welcome():
    return "Alive!"

@app.route('/predict', methods=['POST'])
def post_request():
    try:
        data = request.json
        if type(data) == dict:
            return "OK!"
        else:
            print(type(data))
            return jsonify({'error': 'Invalid input'}), 400
        
    except:
        return jsonify({'error': 'Invalid input'}), 400
"""
@app.route('/predict', methods=['GET'])
def get_predict():
    pass
"""
if __name__ == '__main__':
    app.env = 'development'
    app.run()