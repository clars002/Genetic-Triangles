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
        default=24,
        help="Number of triangles per individual image.",
    )
    parser.add_argument(
        "--population",
        type=int,
        default=64,
        help="Size of the population; number of individuals.",
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=50000,
        help="Maximum number of generations to run before stopping.",
    )
    parser.add_argument(
        "--scaling_factor",
        type=int,
        default=50,
        help="Scaling factor to apply to selection; higher scaling = higher selection pressure",
    )
    parser.add_argument(
        "--mutation_rate",
        type=float,
        default=0.01,
        help="Portion of triangles mutated per generation on average.",
    )
    parser.add_argument(
        "--crossover_rate",
        type=float,
        default=0.02,
        help="Portion of parent combinations that will reproduce each generation.",
    )
    parser.add_argument(
        "--throttle",
        type=float,
        default=0,
        help="Portion of cpu time to sleep (to throttle CPU utilization)",
    )
    return parser.parse_args()


def generate_stats(population, arbitrator, args, display: bool = True):
    total_fitness = 0
    best_fitness = None
    best_0 = None

    for individual in population:
        individual_fitness = individual.fitness_score

        if individual_fitness == None:
            individual_fitness = arbitrator.assess_fitness(individual)

        total_fitness += individual_fitness

        if best_fitness == None or individual_fitness < best_fitness:
            best_fitness = individual_fitness
            best_0 = individual.render(False)

    average_fitness = total_fitness / args.population

    if display:
        print(f"Average fitness gen 0: {average_fitness}")
        print(f"Best fitness gen 0: {best_fitness}")

    return best_fitness, individual, average_fitness


def main():
    """
    Main driver to coordinate genetic algorithm execution
    """

    args = process_args()

    ref_image = Image.open(args.image)
    full_dimensions = ref_image.size

    the_arbitrator = TriangleArtArbitrator(
        ref_image, args.mutation_rate, args.crossover_rate, args.scaling_factor
    )
    population = []

    # Initialize population with individual_count random individuals
    for i in range(args.population):
        new_individual = Individual_Image(full_dimensions)
        new_individual.random_populate(args.triangles)
        population.append(new_individual)

    generate_stats(population, the_arbitrator, args)

    for i in range(args.generations):
        print(f"Processing generation {i}.")
        evolve_start = time.time()
        next_generation = the_arbitrator.evolve(population, args.triangles)
        evolve_duration = time.time() - evolve_start
        population = next_generation
        time.sleep(evolve_duration * args.throttle)

    generate_stats(population, the_arbitrator, args)


if __name__ == "__main__":
    main()
