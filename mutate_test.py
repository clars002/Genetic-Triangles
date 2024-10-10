# ChatGPT example for drawing triangles
import random
import time

from PIL import Image, ImageDraw

from individual import Individual_Image
from triangle import Triangle
from triangles_arbitrator import TriangleArtArbitrator

start_time = time.time()

triangle_count = 6
individual_count = 50
generation_count = 100

population = []

ref_image = Image.open("images/pika_32.png")
full_dimensions = ref_image.size

the_arbitrator = TriangleArtArbitrator(ref_image)

base = Individual_Image(full_dimensions)
base.random_populate(triangle_count)

population.append(base)

base_render = base.render()
base_render.save("Base.png")

the_arbitrator.mutate(population)

mutate_render = base.render()
mutate_render.save("Mutated.png")

end_time = time.time()
runtime = end_time - start_time
print(f"Runtime: {runtime:.4f} seconds")
