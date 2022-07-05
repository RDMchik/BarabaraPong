import json


class JsonLoader(object):

    def load(file_path: str) -> any:
        
        with open(file_path, 'r') as file:
            data = json.load(file)

        return data