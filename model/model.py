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
    def __init__(self) -> None:
        """
        A function that initialize the class.
        """
        self.df = pd.read_csv("data/raw_data.csv")
        self.model_name:str = "model.pkl"
        self.model_column_name:str = "model_columns.pkl"
        self.poly_feature_name:str = "poly_features.pkl"
        self.model_path:str = Path("./model/").joinpath(self.model_name)
        self.poly_features_model_path:str = Path("./model/").joinpath(self.poly_feature_name)
        self.model_column_path:str = Path("./model/").joinpath(self.model_column_name)
        

    def check_model_not_exist(self):
        """
        A Function that check the model file is exist or not. If not exist, create a new model file.
        """
        if not (os.path.exists(self.model_path)):
            self.train_model()
        else:
            print("Model already exist.")
    
    def manipulate_dataset(self):
        """
        A Function that manipulate the dataset.
        """
        
        raw_data: pd.DataFrame = self.df

        # Remove Unexpected rows
        raw_data.drop(raw_data[raw_data['Price'] == 'None' ].index, inplace=True)
        raw_data.drop(raw_data[raw_data['Type of property'] == 'new-real-estate-project-apartments'].index,inplace=True)
        raw_data.drop(raw_data[raw_data['Type of property'] == 'new-real-estate-project-houses'].index,inplace=True)
        raw_data.drop(['Locality'], axis=1, inplace=True)

        # Delete dublicates
        raw_data = raw_data.drop_duplicates()


        # Price 
        raw_data['Price'] = raw_data['Price'].str.replace(',','')
        raw_data['Price'] = raw_data['Price'].astype(np.int64)

        #Bedrooms
        raw_data[raw_data['Type of property'] =='flat-studio']['Bedrooms'].all = 0
        raw_data.drop(raw_data[raw_data["Bedrooms"] == "None"].index, inplace=True)
        raw_data["Bedrooms"] = raw_data['Bedrooms'].astype(int)

        # Living Area 
        raw_data.drop(raw_data[raw_data["Living area"] == "None"].index, inplace=True)
        raw_data["Living area"] = raw_data["Living area"].astype(int)

        # Building Condition
        raw_data['Building condition'].replace({
            'As new': 1,
            'Good': 2,
            'Just renovated': 3,
            'To renovate': 4,
            'To be done up': 5,
            'To restore': 6,
            'None': 2,
        }, inplace=True)
        raw_data['Building condition'] = raw_data['Building condition'].astype(int)

        # Kitchen type
        raw_data["Kitchen type"].replace({
            "Installed":2,
            "Hyper equipped":1,
            "None":0,
            "Semi equipped":3,
            "USA hyper equipped":1,
            "Not installed":0,
            "USA installed":2,
            "USA semi equipped":3,
            "USA uninstalled":0,
            }, inplace=True)
        raw_data['Kitchen type'] = raw_data['Kitchen type'].astype(int)

        # Furnished
        raw_data['Furnished'] = raw_data['Furnished'].replace('None', 0).astype(int)


        # Number of Frontage
        apt_median_value = raw_data[raw_data['Number of frontages'] != 'None']['Number of frontages'].median()
        raw_data['Number of frontages'] = raw_data['Number of frontages'].replace('None',2).astype(int)


        # Swimming Pool
        raw_data['Swimming pool'] = raw_data['Swimming pool'].replace('None', 0).astype(int)

        #Type of property
        #print(raw_data['Type of property'].unique())
        raw_data["Type of property"].replace({
            "apartment":0,
            "house":1,
            "duplex":2,
            "villa":3,
            "mixed-use-building":4,
            "exceptional-property": 5,
            "ground-floor": 6,
            "penthouse": 7,
            "loft": 8,
            "apartment-block": 9,
            "town-house": 10,
            "mansion": 11,
            "service-flat": 12,
            "castle": 13,
            "bungalow": 14,
            "triplex": 15,
            "flat-studio": 16,
            "farmhouse": 17,
            "other-property": 18,
            "kot": 19,
            "manor-house": 20,
            "chalet": 21,
            "country-cottage": 22
            }, inplace=True)
        raw_data['Type of property'] = raw_data['Type of property'].astype(int)

        # Terrace surface
        raw_data['Terrace surface'] = raw_data['Terrace surface'].replace('None', 0).astype(int)

        #Garden surface
        raw_data['Garden surface'] = raw_data['Garden surface'].replace('None', 0).astype(int)

        # surface of the plot 

        raw_data['Surface of the plot'] = raw_data['Surface of the plot'].replace('None', None)
        raw_data['Surface of the plot'] = raw_data['Surface of the plot'].fillna(raw_data['Living area'])

        raw_data['Surface of the plot'] = raw_data['Surface of the plot'].astype(int)
        # rename the column
        raw_data = raw_data.rename(columns={"Price": "price", "Bedrooms": "bedrooms",
                                "Living area": "living_area", "Kitchen type": "kitchen_type",
                                "Furnished": "furnished", "Terrace surface": "terrace_surface",
                                "Garden surface": "garden_surface", "Surface of the plot": "plot_surface",
                                "Number of frontages": "frontage", "Swimming pool": "swimming_pool",
                                "Building condition": "condition", "Type of property": "property_type",

        })

        # Save the dataset to a csv file.
        raw_data.to_csv("./data/dataset.csv", index=False)

    def train_model(self):
        """
        A Function that train the model.
        """
        df = pd.read_csv('./data/dataset.csv')
        
        y = df["price"]
        X = df.drop(["price"], axis=1)

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


model = Model()
model.train_model()
