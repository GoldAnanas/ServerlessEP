import pyLambdaFlows
import time
import pandas as pd
import json
from MapToMap import MapToMapOp
from time import time

POPULATION_SIZE           = 100
MUTATION_RATE             = 0.1
CROSSOVER_RATE            = 0.9
TOURNAMENT_SELECTION_SIZE = 3
NUMB_OF_ELITE_SCHEDULES   = 2
SPLIT_VAR                 =4
NUMB_OF_GENERATION        = 70

def run():
    time1=time()

    param = pyLambdaFlows.Source()
    param.files.append("./population.py")
    param.files.append("./schedule.py")
    param.files.append("./domain.py")
    param.files.append("./utils.py")
    param.files.append("./data.py")
    param.files.append("./genetic_algorithm.py")


    b = pyLambdaFlows.op.Map(param, ["./Eval_Kernel.py", "./population.py", "./schedule.py", "./domain.py", "./utils.py", "./data.py", "./genetic_algorithm.py"]) # dependances size=4 : [[0], [1], [2], [3]]

    c = MapToMapOp([b, param], ["./Rate_and_Generate_Kernel.py", "./population.py", "./schedule.py", "./domain.py", "./utils.py", "./data.py", "./genetic_algorithm.py"]) # dependances size=4 : [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

    d = MapToMapOp([c, param], ["./Rate_and_Generate_Kernel.py", "./population.py", "./schedule.py", "./domain.py", "./utils.py", "./data.py", "./genetic_algorithm.py"]) #dependances size=4 : [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

    e = MapToMapOp([d, param], ["./Rate_and_Generate_Kernel.py", "./population.py", "./schedule.py", "./domain.py", "./utils.py", "./data.py", "./genetic_algorithm.py"]) #dependances size=4 : [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

    f = MapToMapOp([e, param], ["./Rate_and_Generate_Kernel.py", "./population.py", "./schedule.py", "./domain.py", "./utils.py", "./data.py", "./genetic_algorithm.py"]) #dependances size=4 : [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

    param_list = []

    for acc in range (SPLIT_VAR):
        param_list.append([POPULATION_SIZE,MUTATION_RATE,CROSSOVER_RATE,TOURNAMENT_SELECTION_SIZE,SPLIT_VAR,NUMB_OF_ELITE_SCHEDULES,NUMB_OF_GENERATION])

    with pyLambdaFlows.Session(credentials_csv="./accessKeys.csv") as sess:
        f.compile(purge=False)
        result = f.eval(feed_dict={param:param_list})
    time2=time()
    print(result)
    res_list=[]
    for i in range (SPLIT_VAR):
        for s in range(NUMB_OF_ELITE_SCHEDULES):
            print(result[i][s]._fitness)
            res_list.append(result[i][s])            

    """
    # Pour visionner amélioration
    print(result[0][0])
    print("--> fitness : "+ str(result[0][0]._fitness))
    print(result[0][1])
    print("--> fitness : "+ str(result[0][1]._fitness))
    """

    print("time : {}".format(time2-time1))
    res = sorted(res_list,key = lambda schedule: schedule._fitness,reverse=True)
    print("First schedule: {} with fitness = {}".format(res[0],res[0]._fitness))
    final_res = (res[0]._fitness,(time2-time1))
    return final_res

if __name__ == "__main__":

    
    '''
    with open("parallel_100.csv","w+") as f:
        for i in range(30):
            res_tuple = run()
            string = str(i)+";"+str(res_tuple[0])+";"+str(res_tuple[1])+"\n"
            f.write(string)
    '''
    run()
      