import pandas as pd

from src.config.config import Configuration

class InputModule:
    def __init__(self):
        self.config = Configuration()

    def read_input_file(self):
        # TO DO: optimize loaded columns
        input_data = pd.read_csv(self.config.DATASET_DIR)
        return input_data