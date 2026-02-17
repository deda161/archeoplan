import matplotlib.pyplot as plt
import math
from matplotlib.patches import Rectangle
from artifacts_manager import ArtifactsManager
from matplotlib.offsetbox import AnnotationBbox
import os
from datetime import datetime

class GraphicCreator:
    def __init__(self):
        self.figs = []
        self.axes = []

    def __prepare_background(self, rows, columns, layers_count=1):

        for _ in range(layers_count):
            fig, ax = plt.subplots(figsize=(12, 9)) # in inches
            fig.patch.set_facecolor('#fafafa')
            plt.subplots_adjust(left=0.2) # for legend

            ax.set_xlim(-0.5, columns - 0.5)
            ax.set_ylim(-0.5, rows - 0.5)
            ax.set_aspect('equal')
            ax.set_facecolor('#fafafa')
            ax.axis('off')

            ax.set_xticks([])
            ax.set_yticks([])

            self.figs.append(fig)
            self.axes.append(ax)

    def __save_plot_as_file(self, file_name, layer):
        current_datetime = datetime.now()
        folder_path = f"output_{current_datetime.strftime('%Y_%m_%d__%H_%M')}"
        os.makedirs(folder_path, exist_ok=True)

        self.figs[layer].savefig(f'{folder_path}/{file_name}.png', dpi=300, bbox_inches='tight')

    def __draw_grid(self, rows, columns, squares_matrix, layer=0):
        for row in range(rows):
            for column in range(columns):
                if (squares_matrix[row][column] != -1):
                    x_coord = column
                    y_coord = rows - row - 1
                    rect = Rectangle((x_coord - 0.5, y_coord - 0.5),
                                        1, 1,
                                        facecolor='#fafafa',
                                        edgecolor='black',
                                        linewidth=1)
                    self.axes[layer].add_patch(rect)
                    # add square number as text
                    if x_coord == 0:
                        self.axes[layer].text(x_coord - 0.6, y_coord, f'{squares_matrix[row][column]}',
                                ha='center', va='center',
                                fontsize=10, color='black', alpha=0.7)
                    elif y_coord == 0 and x_coord != 0:
                        self.axes[layer].text(x_coord, y_coord - 0.55, f'{squares_matrix[row][column]}',
                                ha='center', va='center',
                                fontsize=10, color='black', alpha=0.7)
                    elif y_coord != rows - 1 and x_coord != 0:
                        continue
                    elif y_coord == rows - 1 and x_coord != 0:
                        self.axes[layer].text(x_coord, y_coord + 0.55, f'{squares_matrix[row][column]}',
                                ha='center', va='center',
                                fontsize=10, color='black', alpha=0.7)

        # TODO calculate edges
        # Calculate edge lines (cause rectangle is not perfect)
        # self.ax.plot([0-0.5, 1+0.5], [0-0.5, 0-0.5],
        #             color='black',
        #             linewidth=2.5,
        #             solid_capstyle='butt')
        # self.ax.plot([3-0.5, 3-0.5], [3-0.5, 6+0.5],
        #             color='black',
        #             linewidth=2.5,
        #             solid_capstyle='butt')


    def __prepare_layers_data(self, artifacts_raw_data) -> tuple[list, int]:
        self.artifacts = []
        layers_array = []

        for layer in artifacts_raw_data:
            layers_array.append(layer['layer'])

        return layers_array, len(layers_array)

    def make_plots(self, rows, columns, squares_matrix, artifacts_raw_data):
        layers_array, layers_count = self.__prepare_layers_data(artifacts_raw_data)
        self.__prepare_background(rows, columns, layers_count)

        for layer in range(layers_count):
            self.__draw_grid(rows, columns, squares_matrix, layer)

            self.artifacts = artifacts_raw_data[layer]['squares']

            artifacts_manager = ArtifactsManager()

            for row in range(rows):
                for column in range(columns):
                    current_square = squares_matrix[row][column]
                    if current_square != -1:
                        artifacts_square = next((d for d in self.artifacts if d['square'] == current_square), None)
                        x_min = column - 0.5
                        y_min = rows - row - 1 - 0.5
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
                                    self.axes[layer].add_artist(ab)

            # Plot name
            self.axes[layer].set_title(f'Пласт {layers_array[layer]}', fontsize=14, fontweight='bold', pad=20)

            plt.tight_layout()

            self.__save_plot_as_file(f'graph_{layers_array[layer]}', layer)

        plt.show()