from pyLambdaFlows.decorator import kernel

from data import Data
from genetic_algorithm import GeneticAlgorithm
from population import Population

@kernel
def lambda_handler(param):

    data = Data()
    _genetic_algorithm = GeneticAlgorithm(data=data, param=param)
    _population = Population(size=param[0], data=data)

    while _population.schedules[0]._fitness != 1.0:
        for schedule in _population.schedules:
            schedule._fitness = schedule.calculate_fitness()
        
        _population.sort_by_fitness()
        _population = _genetic_algorithm.evolve(population=_population)
        
        for schedule in _population.schedules:
            schedule._fitness = schedule.calculate_fitness()
        
        _population.sort_by_fitness()
        
    return _population.schedules
