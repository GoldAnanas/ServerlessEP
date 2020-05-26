import json
import time

POPULATION_SIZE           = 100
MUTATION_RATE             = 0.1
CROSSOVER_RATE            = 0.9
TOURNAMENT_SELECTION_SIZE = 3
NUMB_OF_ELITE_SCHEDULES   = 2
NUMB_OF_GENERATION        = 70

def run():

  from data import Data
  from genetic_algorithm import GeneticAlgorithm
  from population import Population
  from utils import get_random_number

  generation_number = 0
  data = Data()
  param = []
  param.append([POPULATION_SIZE,MUTATION_RATE,CROSSOVER_RATE,TOURNAMENT_SELECTION_SIZE,0,NUMB_OF_ELITE_SCHEDULES])
  start = time.time()
  _genetic_algorithm = GeneticAlgorithm(data=data, param=param[0])
  _population = Population(size=POPULATION_SIZE, data=data)

  while _population.schedules[0]._fitness != 1.0:
    generation_number += 1
    for schedule in _population.schedules:
        schedule._fitness = schedule.calculate_fitness()
    
    _population.sort_by_fitness()
    _population = _genetic_algorithm.evolve(population=_population)
    
    for schedule in _population.schedules:
        schedule._fitness = schedule.calculate_fitness()
    
    _population.sort_by_fitness()
    print(_population.schedules[0]._fitness)
    print(_population.schedules[0].number_of_conflicts)
  end = time.time()
  print(generation_number)
  return (generation_number,end-start)
  


if __name__ == '__main__' and __package__ is None:

  with open("new_seq_30.csv","w+") as f:
      f.write("nbRun;nbGeneration;timeExec\n")
      for i in range(30):
          res_tuple = run()
          string = str(i)+";"+str(res_tuple[0])+";"+str(res_tuple[1])+"\n"
          f.write(string)
          print("###################################################")
    