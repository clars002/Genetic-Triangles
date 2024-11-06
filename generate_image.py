import random
import time

from PIL import Image, ImageDraw

from individual import Individual_Image
from triangle import Triangle
from triangles_arbitrator import TriangleArtArbitrator


def main():
    triangle_count = 32
    individual_count = 64
    generation_count = 100000

    ref_image = Image.open("images/pika_32.png")
    full_dimensions = ref_image.size

    the_arbitrator = TriangleArtArbitrator(ref_image)
    population = []

    for i in range(individual_count):
        new_individual = Individual_Image(full_dimensions)
        new_individual.random_populate(triangle_count)
        population.append(new_individual)

    total_fitness = 0
    best_fitness_0 = None
    best_0 = None

    for individual in population:
        individual_fitness = the_arbitrator.assess_fitness(individual)
        total_fitness += individual_fitness
        if best_fitness_0 == None or individual_fitness < best_fitness_0:
            best_fitness_0 = individual_fitness
            best_0 = individual.render(False)

    average_fitness = total_fitness / individual_count

    print(f"Average fitness gen 0: {average_fitness}")
    print(f"Best fitness gen 0: {best_fitness_0}")
    best_0.save("Best_initial.png")

    for i in range(generation_count):
        print(f"Processing generation {i}.")
        next_generation = the_arbitrator.evolve(population, triangle_count)
        population = next_generation

    total_fitness = 0
    best_fitness_1 = None
    best_1 = None

    for individual in population:
        individual_fitness = individual.fitness_score
        total_fitness += individual_fitness
        if best_fitness_1 == None or individual_fitness < best_fitness_1:
            best_fitness_1 = individual_fitness
            best_1 = individual.render(False)

    average_fitness = total_fitness / individual_count

    print(f"Average fitness gen {generation_count}: {average_fitness}")
    print(f"Best fitness gen {generation_count}: {best_fitness_1}")
    best_1.save("Best_final.png")


if __name__ == "__main__":
    main()
