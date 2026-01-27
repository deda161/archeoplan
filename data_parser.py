import pandas as pd
import numpy as np

class DataParser:
    def __init__(self, file_path):

        self.file_path = file_path
        self.raw_data = {}
        self.processed_data = {}
        self.squares_matrix = []