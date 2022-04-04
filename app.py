import json
import os


from flask import Flask
from flask import Flask, request, jsonify, Blueprint
from sklearn import preprocessing

from predict.prediction import Prediction
from preprocessing.cleaning_data import Preprocessing


app = Flask(__name__)
#app.env = 'development'

blueprint = Blueprint('api', __name__)

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
    return jsonify({'message': preprocessing.convert_json_file()}), 200

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
        return jsonify({"Prediction": prediction_result }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port)