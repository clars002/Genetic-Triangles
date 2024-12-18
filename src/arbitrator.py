class Arbitrator:
    """
    Abstract class which is inherited by TriangleArtArbitrator
    """

    def assess_fitness(individual):
        raise NotImplementedError("This is abstract class Arbitrator")

    def select(population):
        raise NotImplementedError("This is abstract class Arbitrator")

    def crossover(individual_1, individual_2):
        raise NotImplementedError("This is abstract class Arbitrator")

    def mutate(population):
        raise NotImplementedError("This is abstract class Arbitrator")
