from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
import os

mandatory_sheet_names_bel = ['квадрат', 'пласт', 'артэфакт', 'поўнач', 'захад']

class DataParser:
    def __init__(self, file_path):

        self.file_path = file_path
        self.raw_data = {}
        self.processed_data = []
        self.squares_matrix = []
        self.matrix_rows = 0
        self.matrix_cols = 0

    def read_data_from_file(self) -> bool:
        '''
        Read data from Excel file

        :return: True if successful
        :rtype: bool
        '''
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")

            if not self.file_path.lower().endswith(('.xlsx', '.xls')):
                raise ValueError(f"Not Excel format")

            excel_file = pd.ExcelFile(self.file_path, engine='openpyxl')
            sheet_names = excel_file.sheet_names

            for sheet_name in sheet_names:
                raw_data = pd.read_excel(self.file_path,
                                  sheet_name=sheet_name,
                                  engine='openpyxl',
                                  dtype=str)

                self.raw_data[sheet_name] = raw_data
            return True

        except FileNotFoundError as no_file_error:
            return False
        except Exception as error:
            return False

    def prepare_data(self) -> bool:
        '''
        Parse data from file and prepare it for further use.
        Shoold be called after read_data_from_file

        :return: True if successful
        :rtype: bool
        '''
        if not self.raw_data:
            # Excel file is not read yet
            return False

        # Empty previous processed data
        self.processed_data = []

        # Work with each sheet
        for sheet_name, df in self.raw_data.items():

            # If sheet is about configuration of squares, than proceed it separately
            if sheet_name == 'Раскоп':
                self.__parse_squares_configuration(df)
                continue

            # Normalize column names
            df.columns = [str(col).strip().lower() for col in df.columns]

            # Check mandatory columns
            missing_columns = [col for col in mandatory_sheet_names_bel if col not in df.columns]
            if missing_columns:
                # TODO
                continue

            # Group data by layers
            layers = df['пласт'].unique()

            for layer in layers:
                if pd.isna(layer):
                    continue

                layer_str = str(layer).strip()
                layer_data = df[df['пласт'] == layer] # Filter by layer
                squares_dict = {}

                for _, row in layer_data.iterrows():
                    try:
                        square_num_str = str(row['квадрат']).strip()
                        if not square_num_str:
                            continue

                        # Convert square number string to int
                        try:
                            square_num = int(float(square_num_str))
                        except:
                            # TODO
                            square_num = square_num_str

                        # Get artifact coordinates, where y is North, x is West
                        y_str = str(row['поўнач']).strip()
                        x_str = str(row['захад']).strip()

                        # Convert coordinates to float
                        # If coords convertion fails, use default values - 50 (center of square)
                        try:
                            x = float(x_str) if x_str else 50
                        except:
                            x = 50

                        try:
                            y = float(y_str) if y_str else 50
                        except:
                            y = 50

                        # Normalize artifact name
                        artifavt_name = str(row['артэфакт']).strip() if pd.notna(row['артэфакт']) else 'none'
                        self.__convert_artifact_name(artifavt_name)

                        find_record = {
                            'name': artifavt_name,
                            'xy': (x, y)
                        }

                        # Add all other columns if they are not empty
                        for col in df.columns:
                            if col not in mandatory_sheet_names_bel and pd.notna(row[col]):
                                find_record[col] = str(row[col]).strip()

                        # Add artifact to corresponding square
                        if square_num not in squares_dict:
                            squares_dict[square_num] = {
                                'square': square_num,
                                'finds': []
                            }

                        squares_dict[square_num]['finds'].append(find_record)

                    except Exception as error:
                        continue

                # Make record for layer
                if squares_dict:
                    layer_record = {
                        'layer': layer_str,
                        'squares': list(squares_dict.values())
                    }

                    # Add sheet name
                    layer_record['sheet'] = sheet_name
                    self.processed_data.append(layer_record)

        return True

    def __parse_squares_configuration(self, data) -> None:
        matrix = data.values
        self.matrix_rows = len(matrix)
        self.matrix_cols = len(matrix[0])

        for row in range(0, self.matrix_rows):
            for col in range(0, self.matrix_cols):
                if pd.isna(matrix[row][col]):
                    matrix[row][col] = -1
                else:
                    matrix[row][col] = int(float(matrix[row][col]))

        self.squares_matrix = matrix.tolist()

    def get_processed_data(self) -> List[Dict[str, Any]]:
        return self.processed_data

    def get_squares_matrix(self) -> List[List[int]]:
        return self.squares_matrix

    def get_squares_matrix_size(self) -> Tuple[int, int]:
        return self.matrix_rows, self.matrix_cols

    def __convert_artifact_name(self, name) -> str:
        if name == 'костка':
            name = 'bone'
        elif name == 'кераміка':
            name = 'ceramic'
        elif name == 'фаланга':
            name = 'phalanx'
        elif name == 'фр. чэрапу':
            name = 'scull'
        elif name == 'арэх лясны':
            name = 'spine'
        elif name == 'вугаль':
            name = 'wing'
        elif name == 'гліна':
            name = 'glue'
        elif name == 'зуб':
            name = 'tooth'
        elif name == 'камень':
            name = 'stone'
        elif name == 'капраліт':
            name = 'coprolite'
        elif name == 'bone_product':
            name = 'bone_prod'
        elif name == 'к-ка перапаленая':
            name = 'bone_burnt'
        elif name == 'крамянёвы выраб':
            name = 'flint_prod'
        elif name == 'крэмень дэбітаж':
            name = 'flint_debit'
        elif name == 'луска рыбная':
            name = 'fish_scales'
        elif name == 'пляма вуг.':
            name = 'stain_carbone'
        elif name == 'пляма лускі':
            name = 'stain_fish_2'
        elif name == 'пляма попел.':
            name = 'stain_ash'
        elif name == 'пляма пясчаная':
            name = 'stain_sand'
        elif name == 'пляма рак.':
            name = 'stain_cancer'
        elif name == 'пляма рыбн.':
            name = 'stain_fish'
        elif name == 'ракавінка скарлупка':
            name = 'shell'
        elif name == 'рыбная костка':
            name = 'fish_bone'
        elif name == 'чылім ядро':
            name = 'kernel'
        else:
            name = 'none'