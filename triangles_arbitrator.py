from arbitrator import Arbitrator
from PIL import Image
from individual import Individual_Image
from typing import List
import random
import itertools

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
            if individual.fitness_score != None:
                total_fitness += individual.fitness_score
            else:
                total_fitness += self.assess_fitness(individual)

        for individual in population:
            weights.append(1 / (individual.fitness_score / total_fitness)) # invert because higher fitness_score = less fit

        selection = random.choices(population, weights, k=selection_size)

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
        
        new_population = self.select(population, initial_population_size)

        return new_population