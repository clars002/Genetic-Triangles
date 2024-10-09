# ChatGPT example for drawing triangles
import random
import time

from PIL import Image, ImageDraw

from individual import Individual_Image
from triangle import Triangle
from triangles_arbitrator import TriangleArtArbitrator

start_time = time.time()

triangle_count = 32

ref_image = Image.open("images/pika_32.png")
full_dimensions = ref_image.size

the_arbitrator = TriangleArtArbitrator(ref_image)

my_individual = Individual_Image(full_dimensions)

for i in range(triangle_count):
    new_triangle = Triangle()
    new_triangle.random_initialize(full_dimensions)

    my_individual.triangles.append(new_triangle)


print(f"Ref vs Individual: {the_arbitrator.assess_fitness(my_individual)}")

my_individual.render(True)

end_time = time.time()

print(f"Runtime: {end_time - start_time}")
