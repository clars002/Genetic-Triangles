import os
from datetime import datetime
from typing import Tuple

from PIL import Image, ImageDraw

from triangle import Triangle


class Individual_Image:
    """
    A single individual in the population, comprised of an assortment of triangles
    spanning the region defined by the image's dimensions.
    """

    def __init__(
        self,
        dimensions: Tuple[int, int] = None,
        triangles: list[Triangle] = None,
        fitness_score=None,
    ):
        if triangles == None:
            self.triangles = []
        else:
            self.triangles = triangles

        self.fitness_score = fitness_score
        self.dimensions = dimensions

    def random_populate(self, triangle_count):
        """
        Populate the image with a random assortment of triangles
        """
        for i in range(triangle_count):
            new_triangle = Triangle()
            new_triangle.random_initialize(self.dimensions)

            self.triangles.append(new_triangle)

    def render(self, save: bool = False, filename: str = None, folder: str = None):
        """
        Generate an image from this individual's assortment of trianges.
        Can be outputted to the output folder as a .png optionally.
        """
        canvas = Image.new("RGBA", self.dimensions, (255, 255, 255, 255))

        for current_triangle in self.triangles:
            triangle_overlay = Image.new("RGBA", self.dimensions)
            triangle_artist = ImageDraw.Draw(triangle_overlay, "RGBA")
            triangle_artist.polygon(current_triangle.vertices, current_triangle.color)
            canvas.alpha_composite(triangle_overlay)

        if save and filename == None:
            canvas.save(f"output/{str(id(self))}.png")
        elif save:
            datetime_str = datetime.now().strftime("%Y-%m-%d")
            os.makedirs(f"output/{datetime_str}_{folder}", exist_ok=True)
            canvas.save(f"output/{datetime_str}_{folder}/{filename}.png")
        return canvas
