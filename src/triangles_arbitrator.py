import copy
import itertools
import random
import time
from typing import List, Tuple

import numpy as np
from PIL import Image

from arbitrator import Arbitrator
from individual import Individual_Image
from triangle import Triangle


class TriangleArtArbitrator(Arbitrator):
    """
    'Arbitrator' for the triangle class; performs individual and population
    operations (assessing fitness, selection, crossover, mutation)
    """

    def __init__(
        self,
        reference_image: Image,
        mutation_rate: float = 0.05,
        crossover_rate: float = 0.4,
        scaling_factor: int = 1,
    ):
        self.reference_image = reference_image
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.scaling_factor = scaling_factor

        self._generation = 0

    def assess_fitness(self, individual: Individual_Image):
        """
        Compares each pixel from the reference image with each pixel from the individual
        to assess that individual's fitness
        """

        score = 0

        comparison = individual.render()

        for row in range(individual.dimensions[1]):
            for column in range(individual.dimensions[0]):

                reference_pixel = self.reference_image.getpixel((column, row))
                comparison_pixel = comparison.getpixel((column, row))

                for i in range(len(reference_pixel)):
                    score += abs(reference_pixel[i] - comparison_pixel[i])

        individual.fitness_score = score
        return score

    def select(
        self,
        population: List[Individual_Image],
        selection_size,
        output_best: bool = True,
    ):
        """
        Use weighted random selection to generate the next generation's population of
        individuals from the passed population
        """
        selection = []
        weights = []
        total_fitness = 0

        for individual in population:
            total_fitness += self.assess_fitness(individual)

        # Invert the weight because higher fitness_score = less fit individual
        weights = [
            ((1 / (ind.fitness_score / total_fitness)) ** self.scaling_factor)
            for ind in population
        ]
        normalized_weights = [w / sum(weights) for w in weights]

        # Randomly select the next population (do not allow for replacement)
        np_selection = np.random.choice(
            population, size=selection_size, replace=True, p=normalized_weights
        )

        for choice in np_selection:
            selection.append(choice)

        # Calculate most fit individual in the new population:
        best_score = None
        best_individual = None
        total_fitness = 0

        for individual in selection:
            individual_score = individual.fitness_score
            total_fitness += individual_score
            if best_score == None or individual_score < best_score:
                best_score = individual_score
                best_individual = individual

        average_fitness = total_fitness / selection_size

        if output_best:
            # Output the best individual of the new population to the output folder
            filename = f"gen_{self._generation}"
            foldername = id(self)
            best_individual.render(True, filename, foldername)
            print(f"Best fitness: {best_score}")
            print(f"Average fitness: {average_fitness}")

        return selection

    def crossover(
        self,
        parent1: Individual_Image,
        parent2: Individual_Image,
        number_of_triangles: int = None,
    ):
        """
        Perform crossover between two parents and return the child.
        Currently only one type of crossover, based on the first type in
        the lecture 8 notes.
        """
        dimensions = parent1.dimensions
        child = Individual_Image(dimensions)

        if number_of_triangles == None:
            number_of_triangles = len(parent1.triangles)

        cutoff = random.randint(0, number_of_triangles - 1)

        for i in range(0, cutoff):
            triangle_copy = copy.deepcopy(parent1.triangles[i])
            child.triangles.append(triangle_copy)

        for j in range(cutoff, number_of_triangles):
            triangle_copy = copy.deepcopy(parent2.triangles[j])
            child.triangles.append(triangle_copy)

        return child

    def mutate(
        self,
        population: List[Individual_Image],
        number_of_triangles: int = None,
        dimensions: Tuple[int, int] = None,
    ):
        """
        Apply mutation randomly to the entire population.
        """
        if number_of_triangles == None:
            number_of_triangles = len(population[0].triangles)
        if dimensions == None:
            dimensions = population[0].dimensions

        for individual in population:
            for triangle in individual.triangles:
                check = random.random()
                if check < self.mutation_rate:
                    self.mutate_triangle(triangle, dimensions)

    def mutate_triangle(self, triangle: Triangle, bounds: Tuple[int, int]):
        """
        Apply a random mutation to the passed triangle. Can affect shape
        (the position of each vertex), and/or color (each R, G, and B value).
        """
        for i in range(3):
            check = random.random()
            if check < 0.5:
                new_x_position = random.randint(0, bounds[0])
                new_y_position = random.randint(0, bounds[1])
                triangle.vertices[i] = (new_x_position, new_y_position)

        new_colors = [None] * 4
        for i in range(3):
            check = random.random()
            if check < 0.5:
                new_color_value = random.randint(0, 255)
                new_colors[i] = new_color_value
            else:
                new_colors[i] = triangle.color[i]

        new_colors_tuple = (new_colors[0], new_colors[1], new_colors[2], 128)

        triangle.color = new_colors_tuple

        return

    def evolve(
        self, population: List[Individual_Image], number_of_triangles: int = None
    ):
        """
        Apply the genetic algorithm for one generation.
        """
        initial_population_size = len(population)
        parent_combos = itertools.combinations(population, 2)
        children = []

        # If the number of triangles per image is not passed explicitly, discern it:
        if number_of_triangles == None:
            number_of_triangles = len(population[0].triangles)

        # Out of all the possible combinations of parents, 40% will bear children:
        for combo in parent_combos:
            if random.random() < self.crossover_rate:
                children.append(self.crossover(combo[0], combo[1], number_of_triangles))

        for child in children:
            population.append(child)

        # Mutate the current pool of individuals, including parents and children
        self.mutate(population)

        # Select the new population out of all parents and children in the current pool
        new_population = self.select(population, initial_population_size)

        self._generation += 1
        return new_population
