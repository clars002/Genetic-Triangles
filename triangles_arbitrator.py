from arbitrator import Arbitrator
from PIL import Image
from individual import Individual_Image


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
