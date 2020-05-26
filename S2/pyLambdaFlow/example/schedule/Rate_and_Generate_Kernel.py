import json
import pickle
from time import sleep,time
import boto3 
from pyLambdaFlows.decorator import kernel

# Takes a population list
# Generate new population from the best elites of all the subpopulation
# Evaluate the new population created and sends it

from data import Data
from population import Population
from genetic_algorithm import GeneticAlgorithm

@kernel 
def lambda_handler(list_elites_schedules,param):
    all_elites = []

    for schedules_list in list_elites_schedules:
        for schedule in schedules_list:
            all_elites.append(schedule)  

    sorted_list = sorted(all_elites, key= lambda schedule: schedule._fitness, reverse=True)
    
    """
    print(len(sorted_list))
    for i in range (len(sorted_list)):
        print(sorted_list[i]._fitness)
    """

    data = Data()
    newPop = Population(size=param[0][0],data=data, schedules=sorted_list)

    """
    print(len(newPop.schedules))
    for i in range (len(newPop.schedules)):
        print(newPop.schedules[i]._fitness)
    """

    algo = GeneticAlgorithm(data=data,param=param[0]) 
      
    for _ in range(param[0][6]):
        if(newPop.schedules[0]._fitness!=1.0):
            newPop = algo.evolve(population=newPop)
            
            for schedule in newPop.schedules:
                schedule._fitness=schedule.calculate_fitness()
            newPop.sort_by_fitness()
    
    elites=[]
    for i in range(param[0][5]): #param[0][5]==NUMB_OF_ELITES
        elites.append(newPop.schedules[i])
    
    return elites
    