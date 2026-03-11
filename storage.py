import os
import json


class FileStorage:
    def __init__(self, filepath):
        self.filepath = filepath



    def load(self):
        if not os.path.exists(self.filepath):
            return {}


        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)


        return data


    def save(self, data):
        temp_path = self.filepath + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        os.replace(temp_path, self.filepath)
