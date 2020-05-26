import pyLambdaFlows
import time
import pandas as pd
import json
from MapToMap import MapToMapOp
from time import time

POPULATION_SIZE           = 40
MUTATION_RATE             = 0.1
CROSSOVER_RATE            = 0.9
TOURNAMENT_SELECTION_SIZE = 3
NUMB_OF_ELITE_SCHEDULES   = 2
SPLIT_VAR                 = 1
def run():
    # First kernel will create first generation and split it into sub_population, and send those to the second kernel
    # Secondly, lambda_kernel_eval will take a sub_pop, evaluate it and then return the elite in it
    # Third kernel takes those result and create new pop mutating from the previous one

    time1=time()

    # This is the first loop


    param = pyLambdaFlows.Source()
    param.files.append("./population.py")
    param.files.append("./schedule.py")
    param.files.append("./domain.py")
    param.files.append("./utils.py")
    param.files.append("./data.py")
    param.files.append("./genetic_algorithm.py")
        

    b = pyLambdaFlows.op.Map(param, ["./Sequential_Kernel.py", "./population.py", "./schedule.py", "./domain.py", "./utils.py", "./data.py", "./genetic_algorithm.py"]) # dependances size=4 : [[0], [1], [2], [3]]

    param_list = []

    for _ in range (SPLIT_VAR):
        param_list.append([POPULATION_SIZE,MUTATION_RATE,CROSSOVER_RATE,TOURNAMENT_SELECTION_SIZE,SPLIT_VAR,NUMB_OF_ELITE_SCHEDULES])

    with pyLambdaFlows.Session(credentials_csv="./accessKeys.csv") as sess:
        b.compile(purge=False)
        result = b.eval(feed_dict={param:param_list})
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
    final_res = (result[0]._fitness,(time2-time1))
    return final_res

if __name__ == "__main__":
    '''
    with open("seq_aws_30.csv","w+") as f:
        for i in range(30):
            res_tuple = run()
            string = str(i)+";"+str(res_tuple[0])+";"+str(res_tuple[1])+"\n"
            f.write(string)
    '''
    run()