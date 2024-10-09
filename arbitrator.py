class Arbitrator:
    def assess_fitness(individual):
        raise NotImplementedError("This is abstract class Arbitrator")

    def select(population):
        raise NotImplementedError("This is abstract class Arbitrator")

    def crossover(individual_1, individual_2):
        raise NotImplementedError("This is abstract class Arbitrator")

    def mutate(individual):
        raise NotImplementedError("This is abstract class Arbitrator")
