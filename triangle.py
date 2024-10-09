import random
from typing import Tuple


class Triangle:
    def __init__(self, vertices=None, color=None):
        self.vertices = vertices
        self.color = color

    def random_initialize(self, bounds: Tuple[int, int]):
        self.vertices = [None] * 3
        colors = [None] * 3

        for i in range(3):
            x_coordinate = random.randint(0, bounds[0])
            y_coordinate = random.randint(0, bounds[1])
            color_value = random.randint(0, 255)

            self.vertices[i] = (x_coordinate, y_coordinate)
            colors[i] = color_value

        self.color = (colors[0], colors[1], colors[2], 128)
