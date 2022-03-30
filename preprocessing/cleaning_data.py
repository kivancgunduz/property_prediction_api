

class Preprocessing:
    """
    A class that operate all preprocessing operations before the prediction operations
    """

    def __init__(self) -> None:
        """
        A function that defines construction varaibles.

        """
        self.model_dict = model_dict = {
            "Living area": {'type': int,'optional':False,'default': []},
            "Bedroom": {'type': int, 'optional': False, 'default': []},
            "Province": {
                'type': str,
                'optional': False,
                'default': [
                    'Brussels', 'Oost-vlaanderen', 'Vlaams-brabant', 'Luik', 'Namen',
                    'Luxemburg', 'West-vlaanderen', 'Antwerpen', 'Henegouwen',
                    'Waals-brabant', 'Limburg']},
            "Property Type": {'type': str, 'optional': False, 'default': ['Apartment','House']},
            "Property Subtype": {
                'type': str,
                'optional': True,
                'default': [
                    'Apartment', 'Town-house', 'House', 'Villa', 'Penthouse',
                    'Mansion', 'Studio', 'Exceptional property', 'Kot', 'Duplex',
                    'Triplex', 'Ground floor', 'Bungalow', 'Loft', 'Chalet',
                    'Service flat', 'Castle', 'Farmhouse', 'Country house',
                    'Manor house', 'Other properties']
                },
            "Surface of the plot": {'type': int, 'optional': True, 'default': []},
            "HasGarden": {'type': str, 'optional': True, 'default': ['Yes','No']},
            "Garden surface": {'type': int, 'optional': True, 'default': []},
            "Kitchen Type": {
                'type': str,
                'optional': True,
                'default': ['Equipped', 'Semi-equipped', 'Not installed']},
            "Swimming pool": {'type': str, 'optional': True, 'default': ['Yes','No']},
            "Furnished": {'type': str, 'optional': True, 'default': ['Yes','No']},
            "HasFireplace": {'type': str, 'optional': True, 'default': ['Yes','No']},
            "HasTerrace": {'type': str, 'optional': True, 'default': ['Yes','No']},
            "Terrace surface": {'type': int, 'optional': True, 'default': []},
            "Number of frontages": {'type': int, 'optional': True, 'default': []},
            "Building condition": {'type': str, 'optional': True, 'default': ['As new','Good','To renovate']}
    }
    

    def preprocess(self, json_input: dict):
        """
        A Function that check entry input and then validate it.
        Param:: json_input: A dictionary
        Param:: self
        """

        for feauture in self.model_dict.keys():
            if not self.model_dict[feauture]['optional']:
                if feauture not in json_input.keys():
                    raise ValueError(f'The feauture {feauture} is missing!')

        valid_data = json_input.copy()
        for feature, value in json_input.items():
            if feature not in self.model_dict.keys():
                raise ValueError(f'{feature} is not a valid entry')
            if type(value) != self.model_dict[feature]['type']:
                raise ValueError(f'{feature}:{value} of {type(value)} should be {self.model_dict[feature]["type"]}')
            if self.model_dict[feature]['type'] == str and len(self.model_dict[feature]['default'])>0:
                if value not in self.model_dict[feature]['default']:
                    raise ValueError(f'Possible entries for {feature} are {self.model_dict[feature]["default"]}')
                else:
                    #convert data
                    valid_data[f"{feature}_{value}"] = 1
                    del valid_data[feature]

        return [valid_data]
        

    

