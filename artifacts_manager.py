import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage
import os

class ArtifactsManager:
    def __init__(self):
        pass

    def get_offset_image_of_artifact(self, artifact) -> OffsetImage | None:
        img_path = f"symbols/{artifact}.png"
        try:
            img = plt.imread(img_path)
        except FileNotFoundError:
            return None

        return OffsetImage(img, zoom=0.4)