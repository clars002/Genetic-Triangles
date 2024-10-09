from triangle import Triangle
from PIL import Image, ImageDraw
from typing import Tuple


class Individual_Image:
    def __init__(
        self,
        dimensions: Tuple[int, int] = None,
        triangles: list[Triangle] = [],
        fitness_score=None,
    ):
        self.triangles = triangles
        self.fitness_score = fitness_score
        self.dimensions = dimensions

    def render(
        self, save: bool = False
    ):  # TODO: Are the opacities non-uniform for some reason?
        canvas = Image.new("RGBA", self.dimensions, (255, 255, 255, 255))

        for current_triangle in self.triangles:
            triangle_overlay = Image.new("RGBA", self.dimensions)
            triangle_artist = ImageDraw.Draw(triangle_overlay, "RGBA")
            triangle_artist.polygon(current_triangle.vertices, current_triangle.color)
            canvas.alpha_composite(triangle_overlay)

        if save:
            canvas.save(f"{str(id(self))}.png")
        return canvas
