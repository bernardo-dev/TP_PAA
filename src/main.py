import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gerador_instancias.gerar import get_experiment_data
from .algorithms import dynamic_programming as dp
from .algorithms import branch_and_bound as bb
from consts import INSTANCE_BASE_PATH
from algorithms import backtracking as bt

def dynamic_programming_experiment(experiment_number, combination, instance):
    print("\tExecutando experimento de programação dinâmica...")

    instance_path = f'{INSTANCE_BASE_PATH}/experimento_{experiment_number}/combinacao{combination}_{instance}.txt'
    dp.execute(instance_path, experiment_number)

def branch_and_bound_experiment(experiment_number, combination, instance):
    print("\tExecutando experimento de branch and bound...")

    instance_path = f'{INSTANCE_BASE_PATH}/experimento_{experiment_number}/combinacao{combination}_{instance}.txt'
    bb.execute(instance_path)

def backtracking_experiment():
    print("\tExecutando experimento de backtracking...")

def run_experiment(experiment_number):
    print("-----------------------------------")
    print(f"Iniciando Experimento {experiment_number}")
    print("-----------------------------------")


    for combination in range(1, 2):
        for instance in range(1, 2):
            W, V, n = get_experiment_data(experiment_number, combination)
            print(f"Processando instância {instance} - Combinação {combination}: W={W}, V={V}, n={n}")

            #dynamic_programming_experiment(experiment_number, combination, instance)
            branch_and_bound_experiment(experiment_number, combination, instance)
            # backtracking_experiment()
   

if __name__ == "__main__":
    run_experiment(1)
    #run_experiment(2)
    #run_experiment(3) 