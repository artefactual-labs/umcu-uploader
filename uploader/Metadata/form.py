import json


class FormData:
    def __init__ (self, filepath=None, form=None):
        self.filepath = filepath
        self.form = form

    def load(self):
         # Read form from JSON if applicable
        try:
            with open(self.filepath, 'r') as data:
                self.form = json.load(data)
        except FileNotFoundError:
            return 'Form could not be loaded', self.form
    def save(self):
         # Read form from JSON if applicable
        try:
            with open(self.filepath, 'w') as data:
                self.form = json.dumps(data)
        except FileNotFoundError:
            return 'Form could not be saved', self.form