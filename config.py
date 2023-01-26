"""
Author: João Victor David de Oliveira (j.victordavid2@gmail.com)
config.py (c) 2023
Desc: description
Created:  2023-01-26T18:16:43.524Z
Modified: 2023-01-26T18:40:58.331Z
"""

import json


class ConfigBasic:
    def __init__(self, file: str, baseData = None):
        self.file = file
        self.data = {}
        self.baseData = baseData

    def load(self):
        try:
            with open(self.file, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            if self.baseData is not None:
                config = self.baseData
                with open(self.file, 'w') as f:
                    json.dump(self.baseData, f)
            else:
                raise FileNotFoundError
        self.data = config
        return config

    def save(self, config: dict = None):
        saveData = config if config else self.data
        with open(self.file, 'w') as f:
            json.dump(saveData, f)
        return True


class Config(ConfigBasic):
    def __init__(self, file: str, baseData = None):
        super().__init__(file, baseData)
        self.load()

    def get(self, key: str):
        return self.data[key]

    def set(self, key: str, value):
        self.data[key] = value
        self.save()
        return True

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key: str, value):
        return self.set(key, value)
