import matplotlib.pyplot as plt
import math
from matplotlib.patches import Rectangle
from artifacts_manager import ArtifactsManager
from matplotlib.offsetbox import AnnotationBbox

class GraphicCreator:
    def __init__(self):
        self.fig = None
        self.ax = None

    def __prepare_background(self, rows, columns):
        self.fig, self.ax = plt.subplots(figsize=(12, 9)) # in inches
        self.fig.patch.set_facecolor('#fafafa')
        plt.subplots_adjust(left=0.2) # for legend

        self.ax.set_xlim(-0.5, columns - 0.5)
        self.ax.set_ylim(-0.5, rows - 0.5)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('#fafafa')
        self.ax.axis('off')

        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def __draw_grid(self, rows, columns, squares_matrix):
        for i in range(rows):
            for j in range(columns):
                if (squares_matrix[i][j] != -1):
                    # Рисуем квадрат
                    rect = Rectangle((j - 0.5, i - 0.5),  # левый нижний угол
                                        1, 1,
                                        facecolor='#fafafa',
                                        edgecolor='black', #'#495057',
                                        linewidth=1)
                    self.ax.add_patch(rect)

        # Calculate edge lines (cause rectangle is not perfect)
        self.ax.plot([0-0.5, 1+0.5], [0-0.5, 0-0.5],
                    color='black',
                    linewidth=2.5,
                    solid_capstyle='butt')
        self.ax.plot([3-0.5, 3-0.5], [3-0.5, 6+0.5],
                    color='black',
                    linewidth=2.5,
                    solid_capstyle='butt')

        current_square_num= -1
        for x in range(columns):
            for y in range(rows):
                current_square_num += 1
                if squares_matrix[y][x] == -1:
                    continue
                if x == 0:
                    self.ax.text(x - 0.6, y, f'{squares_matrix[y][x]}',
                            ha='center', va='center',
                            fontsize=10, color='black', alpha=0.7)
                elif y == 0 and x != 0:
                    self.ax.text(x, y - 0.55, f'{squares_matrix[y][x]}',
                            ha='center', va='center',
                            fontsize=10, color='black', alpha=0.7)
                elif y != rows - 1 and x != 0:
                    continue
                elif y == rows - 1 and x != 0:
                    self.ax.text(x, y + 0.55, f'{squares_matrix[y][x]}',
                            ha='center', va='center',
                            fontsize=10, color='black', alpha=0.7)

    def __prepare_artifacts_data(self, artifacts_raw_data):
        self.artifacts = []
        if artifacts_raw_data[0]['layer'] == '80-90':
            self.artifacts = artifacts_raw_data[0]['squares']
        else:
            self.artifacts = artifacts_raw_data[1]['squares']

    def make_plots(self, rows, columns, squares_matrix, artifacts_raw_data):
        self.__prepare_background(rows, columns)
        self.__draw_grid(rows, columns, squares_matrix)
        self.__prepare_artifacts_data(artifacts_raw_data)

        artifacts_manager = ArtifactsManager()

        x_coordinate = 0
        y_coordinate = 0
        for i in range(rows):
            for j in range(columns):
                current_square = squares_matrix[i][j]
                if current_square != -1:
                    artifacts_square = next((d for d in self.artifacts if d['square'] == current_square), None)
                    x_min = x_coordinate - 0.5
                    x_max = x_coordinate + 0.5
                    y_min = y_coordinate - 0.5
                    y_max = y_coordinate + 0.5
                    if artifacts_square != None and artifacts_square['finds'] != 'no':
                        counter = 0
                        for artifact in artifacts_square['finds']:

                            if (artifact['xy'][0] < 0 or artifact['xy'][1] < 0) or (artifact['xy'][0] > 100 or artifact['xy'][1] > 100) or math.isnan(artifact['xy'][0]) or math.isnan(artifact['xy'][1]) or math.isinf(artifact['xy'][0]) or math.isinf(artifact['xy'][1]):
                                print(f"Incorrect coords: {artifact['xy']} for artifact {artifact['name']} in square {current_square}")
                                counter += 1
                                continue

                            counter += 1
                            x = (artifact['xy'][0] / 100) + x_min
                            y = (artifact['xy'][1] / 100) + y_min
                            artifact_symble = artifacts_manager.get_offset_image_of_artifact(artifact['name'])

                            if artifact_symble != None:
                                ab = AnnotationBbox(artifact_symble, (x, y), frameon=False)
                                self.ax.add_artist(ab)
                y_coordinate += 1
                if (y_coordinate == rows):
                    y_coordinate = 0
                    x_coordinate += 1

        # Plot name
        self.ax.set_title('Пласт 80-90', fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        plt.show()