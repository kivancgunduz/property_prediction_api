import os
import json
import jsonschema
from jsonschema import validate

class Preprocessing:
    """
    A class that operate all preprocessing operations before the prediction operations.
    """

    def __init__(self) -> None:
        """
        A function that initialize the class.
        """
        self.schema: dict = {}
        self.schema_path: str = 'data/schema.json'
        self.dataset_path: str = 'data/dataset.csv'
        
    
    

    def preprocess(self, json_input: dict):
        """
        A function that preprocess the json input.

        :param json_input: A dictionary that contains the input data.
        :return: A dictionary that contains the preprocessed data.
        """
        # Load the schema if the file is exist.
        if (os.path.exists(self.schema_path)):
            self.schema = self.convert_json_file(self.schema_path)
        else:
            print("The schema file does not exist.")
        
        # Validate the input data.

        
    @staticmethod
    def save_json_file(json_input: dict, file_name: str):
        """
        A function that save the json file.

        :param json_input: A dictionary that contains the input data.
        :param file_name: A string that contains the file name.
        :return: A dictionary that contains the preprocessed data.
        """
        try:
            with open(file_name, 'w+') as f:
                json.dump(json_input, f)
                return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def convert_json_file(file_path: str):
        """
        A function that convert the json file to a dictionary.

        :param file_path: A string that contains the file name.
        :return: A dictionary that contains expected json schema.
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(e)
            return False
        

    

