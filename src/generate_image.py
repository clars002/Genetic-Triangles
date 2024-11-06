import argparse
import random
import time

from PIL import Image, ImageDraw

from individual import Individual_Image
from triangle import Triangle
from triangles_arbitrator import TriangleArtArbitrator


def process_args():
    """
    Parses arguments from the CLI.

    Returns:
        A Namespace object where attributes correspond to the
        defined/provided args.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        default="resources/images/pika_16.png",
        help="Path to the input image file.",
    )
    parser.add_argument(
        "--triangles",
        type=int,
        default=8,
        help="Number of triangles per individual image."
    )
    parser.add_argument(
        "--population",
        type=int,
        default=64,
        help="Size of the population; number of individuals."
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=50000,
        help="Maximum number of generations to run before stopping."
    )
    parser.add_argument(
        "--mutation_rate",
        type=float,
        default=.05,
        help="Portion of triangles mutated per generation on average."
    )
    parser.add_argument(
        "--crossover_rate",
        type=float,
        default=.4,
        help="Portion of parent combinations that will reproduce each generation."
    )
    return parser.parse_args()


def main():
    """
    Main driver to coordinate genetic algorithm execution
    """

    args = process_args()

    ref_image = Image.open(args.image)
    full_dimensions = ref_image.size

    the_arbitrator = TriangleArtArbitrator(ref_image)
    population = []

    # Initialize population with individual_count random individuals
    for i in range(args.population):
        new_individual = Individual_Image(full_dimensions)
        new_individual.random_populate(args.triangles)
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

    average_fitness = total_fitness / args.population

    print(f"Average fitness gen 0: {average_fitness}")
    print(f"Best fitness gen 0: {best_fitness_0}")
    best_0.save("output/Best_initial.png")

    for i in range(args.generations):
        print(f"Processing generation {i}.")
        next_generation = the_arbitrator.evolve(population, args.triangles)
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

    average_fitness = total_fitness / args.population

    print(f"Average fitness gen {args.generations}: {average_fitness}")
    print(f"Best fitness gen {args.generations}: {best_fitness_1}")
    best_1.save("output/Best_final.png")


if __name__ == "__main__":
    main()
