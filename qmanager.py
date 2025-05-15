import pickle
import os

class QManager:
    def __init__(self):
        self.q_table = {}

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f)
        else:
            self.q_table = {}

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)