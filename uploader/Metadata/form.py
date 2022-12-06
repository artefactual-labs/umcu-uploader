import json


class FormData:
    def __init__ (self, filepath=None, form=None):
        self.filepath = filepath
        self.form = form

    def load(self):
         # Load form from JSON if applicable
        try:
            with open(self.filepath, 'r') as data:
                self.form = json.load(data)
        except FileNotFoundError:
            return 'Form could not be loaded', self.form
    def save(self, form):
         # Save form from JSON if applicable
        try:
            with open(self.filepath, 'w') as data:
                self.form = json.dump(form, data)
        except FileNotFoundError:
            return 'Form could not be saved', self.form