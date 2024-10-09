# ChatGPT example for drawing triangles
import random
import time

from PIL import Image, ImageDraw

from individual import Individual_Image
from triangle import Triangle
from triangles_arbitrator import TriangleArtArbitrator

start_time = time.time()

triangle_count = 32
individual_count = 16

ref_image = Image.open("images/pika_32.png")
full_dimensions = ref_image.size

the_arbitrator = TriangleArtArbitrator(ref_image)
population = []

for i in range(individual_count):
    new_individual = Individual_Image(full_dimensions)
    new_individual.random_populate(triangle_count)
    population.append(new_individual)

for individual in population:
    individual.render(True)

end_time = time.time()
print(f"Runtime: {end_time - start_time}")
