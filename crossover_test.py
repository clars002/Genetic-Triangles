# ChatGPT example for drawing triangles
import random
import time

from PIL import Image, ImageDraw

from individual import Individual_Image
from triangle import Triangle
from triangles_arbitrator import TriangleArtArbitrator

start_time = time.time()

triangle_count = 8
individual_count = 64

ref_image = Image.open("images/pika_32.png")
full_dimensions = ref_image.size

the_arbitrator = TriangleArtArbitrator(ref_image)
population = []

parent1 = Individual_Image(full_dimensions)
parent2 = Individual_Image(full_dimensions)

parent1.random_populate(triangle_count)
parent2.random_populate(triangle_count)

p1_out = parent1.render()
p2_out = parent2.render()

child = the_arbitrator.crossover(parent1, parent2, triangle_count)

c_out = child.render()

p1_out.save("p1.png")
p2_out.save("p2.png")
c_out.save("c.png")

# for i in range(individual_count):
#     new_individual = Individual_Image(full_dimensions)
#     new_individual.random_populate(triangle_count)
#     population.append(new_individual)

end_time = time.time()
runtime = end_time - start_time
print(f"Runtime: {runtime:.4f} seconds")
