from arbitrator import Arbitrator
from PIL import Image
from individual import Individual_Image
from typing import List
import random
import itertools
from triangle import Triangle
from typing import Tuple
import numpy as np

class TriangleArtArbitrator(Arbitrator):
    def __init__(self, reference_image: Image):
        self.reference_image = reference_image

    def assess_fitness(self, individual: Individual_Image):

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

    
    def select(self, population: List[Individual_Image], selection_size):
        selection = []
        weights = []
        total_fitness = 0

        for individual in population:
            total_fitness += self.assess_fitness(individual)

        weights = [1 / (ind.fitness_score / total_fitness) for ind in population]
        normalized_weights = [w / sum(weights) for w in weights]

        np_selection = np.random.choice(population, size=selection_size, replace=False, p=normalized_weights)

        for choice in np_selection:
            selection.append(choice)

        return selection

    def crossover(self, parent1: Individual_Image, parent2: Individual_Image, number_of_triangles: int = None):
        dimensions = parent1.dimensions
        child = Individual_Image(dimensions)
        
        if number_of_triangles == None:
            number_of_triangles = len(parent1.triangles)

        cutoff = random.randint(0, number_of_triangles - 1)

        for i in range(0, cutoff):
            child.triangles.append(parent1.triangles[i])

        for i in range(cutoff, number_of_triangles):
            child.triangles.append(parent2.triangles[i])

        return child

    def mutate(self, population: List[Individual_Image], number_of_triangles: int = None, dimensions: Tuple[int, int] = None):
        if number_of_triangles == None:
            number_of_triangles = len(population[0].triangles)
        if dimensions == None:
            dimensions = population[0].dimensions

        for individual in population:
            for triangle in individual.triangles:
                check = random.random()
                if check < (1 / 16):
                    self.mutate_triangle(triangle, dimensions)

    def mutate_triangle(self, triangle: Triangle, bounds: Tuple[int, int]):
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

    def evolve(self, population: List[Individual_Image], number_of_triangles: int = None):
        initial_population_size = len(population)
        parent_combos = itertools.combinations(population, 2)
        children = []

        if number_of_triangles == None:
            number_of_triangles = len(population[0].triangles)

        for combo in parent_combos:
            if random.randint(1, 10) > 4:
                children.append(self.crossover(combo[0], combo[1], number_of_triangles))
        
        for child in children:
            population.append(child)

        self.mutate(population)
        
        new_population = self.select(population, initial_population_size)

        return new_population