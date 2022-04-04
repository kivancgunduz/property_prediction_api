import os
import json
import pandas as pd
import jsonschema
from jsonschema import validate
import pickle

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
        self.dataframe: pd.DataFrame = pd.DataFrame()
        self.condition_dict: dict = {
            'As new': 1,
            'Good': 2,
            'Just renovated': 3,
            'To renovate': 4,
            'To be done up': 5,
            'To restore': 6,
        }
        self.kitchen_dict = {"Not installed": 0, "Semi equipped": 3, "Equipped": 2}
        self.property_type_dict = {
            "Apartment":0,
            "House":1,
        }
        

    def preprocess(self, json_input: dict) -> pd.DataFrame:
        """
        A function that preprocess the json input.
        :param json_input: A dictionary that contains the input data.
        :return: A dictionary that contains the preprocessed data.
        """
        # Check the input data.
        try:
            # Validate the input data.
            validate(json_input, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            print(e)
        else:
            # Convert the input data to dataframe.
            for key, value in json_input.items():
                for i, j in self.condition_dict.items():
                    if (value == i):
                        json_input[key] = j
                for x, y in self.kitchen_dict.items():
                    if (value == x):
                        json_input[key] = y
                for z, w in self.property_type_dict.items():
                    if (value == z):
                        json_input[key] = w

            df = pd.DataFrame(json_input, index=[0])
            df.replace(to_replace='Yes', value=1, inplace=True)
            df.replace(to_replace='No', value=0, inplace=True)
            df['living_area'] = df['living_area'].astype(int)
            df['plot_surface'] = df['surface_plot'].astype(int)
            df['bedrooms'] = df['bedrooms'].astype(int)
            df['condition'] = df['building_condition'].astype(int)
            df['property_type'] = df['property_type'].astype(int)


            model_columns = pickle.load(open('model/model_columns.pkl', 'rb'))
            df = df.reindex(columns=model_columns, fill_value=0)
            print(df)

            return df



        
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
            
    def convert_json_file(self):
        """
        A function that convert the json file to a dictionary.
        :param file_path: A string that contains the file name.
        :return: A dictionary that contains expected json schema.
        """
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(e)
            return False
    
    def check_necessery_files(self) -> bool:
        """
        A function that check the necessary files.

        :return: A boolean that indicates whether the necessary files are exist.
        """
        try:
                # Load the schema if the file is exist.
            if (os.path.exists(self.schema_path)):
                self.schema = self.convert_json_file(self.schema_path)
            else:
                print("The schema file does not exist.")
            # Load the dataset if the file is exist.
            if (os.path.exists(self.dataset_path)):
                self.dataframe = pd.read_csv(self.dataset_path)
            else:
                self.dataframe = pd.read_csv('https://raw.githubusercontent.com/kivancgunduz/challenge-regression/main/data/raw_data.csv')
                self.dataframe.to_csv(self.dataset_path, index=False)
                print("The dataset downloaded.")
            return True
        except:
            print("The necessary files are not exist.")
            return False
    
    