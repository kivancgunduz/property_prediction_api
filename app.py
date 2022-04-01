import json
import os


from flask import Flask
from flask import Flask, request, jsonify
from sklearn import preprocessing

from predict.prediction import Prediction
from preprocessing.cleaning_data import Preprocessing


app = Flask(__name__)
app.env = 'development'
preprocessing = Preprocessing()
prediction = Prediction()

@app.route('/', methods=['GET'])
def welcome():
    if (preprocessing.check_necessery_files()):
        return jsonify({'message': 'Alive! Welcome to the prediction API.'})
    else:
        return jsonify({'message': 'Please check the files!'})

@app.route('/predict', methods=['GET'])
def post_request():
    """
    A function that will inform the user about the expected json schema.
    """
    json_schema = """
    {
        "input": {
                    "post_code": {"type": "int", "required": true, default: []},
                    "kitchen_type": {
                        "type": str,
                        "optional": True,
                        "default": ["Not installed", "Semi equipped", "Equipped"],
                        },
                    "bedroom": {"type": int, "required": True, "default": []},
                    "surface_plot": {"type": int, "optional": True, "default": []},
                    "living_area": {"type": int, "required": True, "default": []},
                    "swimming_pool": {"type": str, "optional": True, "default": ["Yes", "No"]},
                    "property_type": {
                        "type": str,
                        "required": True,
                        "default": ["APARTMENT", "HOUSE"],
                        }
                }
        }
        """
            
    return jsonify({'message': json_schema}), 200

@app.route('/predict', methods=['POST'])
def get_predict():
    """
    A function that will get the prediction from the input data.
    """
    input_data = request.get_json()
    print(input_data)
    if input_data == "" or input_data == None:
        return jsonify({"error": "No input data provided"}), 400
    else:
        predictable_df = preprocessing.preprocess(input_data)
        prediction_result = prediction.predict(predictable_df)
        return jsonify(prediction_result), 200

if __name__ == '__main__':
    app.run()