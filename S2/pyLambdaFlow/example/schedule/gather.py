import json
import pickle
from time import sleep
import boto3 
from pyLambdaFlows.decorator import kernel

#Cette méthode prend une liste de tuple (score,schedule) et retourne le meilleur tuple
@kernel     
def lambda_handler(tuple_list):
    best_tuple = (0,None)
    for elem in tuple_list:
        if elem[0]>best_tuple[0]:
            best_tuple = elem
    return best_tuple
    """
    elements = [ele[0] for ele in elements]
    return max(elements)
    """