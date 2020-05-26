from pyLambdaFlows.decorator import kernel

# Ce kernel prend en entrée une sous population créée aléatoirement et le nombre d'élites à renvoyer
# Il évalue ensuite chacun des individus (schedule)
# Enfin, il renvoie le NUMB_OF_ELITES_SCHEDULES (de base 1)

from data import Data
from population import Population   

@kernel
def lambda_handler(param):
    pop_size=param[0]
    split_var=param[4]
    
    data=Data()
    _population = Population(size=int(pop_size/split_var),data=data)
    
    for schedule in _population.schedules:
        schedule._fitness = schedule.calculate_fitness()
    
    return _population.schedules
