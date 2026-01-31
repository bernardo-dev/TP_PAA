import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(file))))
from gerador_instancias.gerar import get_experiment_data
from src.algorithms import dynamic_programming as dp
from consts import INSTANCE_BASE_PATH
from algorithms import backtracking as bt

def dynamic_programming_experiment(experiment_number, combination, instance):
    print("\tExecutando experimento de programação dinâmica...")

    # Construct the absolute path to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(file)))
    instance_path = f'{INSTANCE_BASEPATH}/experimento{experimentnumber}/combinacao{combination}{instance}.txt'
    dp.execute(instance_path)

def backtracking_experiment(experiment_number, combination, instance):
    print("\tExecutando experimento de backtracking...")

    # Construct the absolute path to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(file)))
    instance_path = f'{INSTANCE_BASEPATH}/experimento{experimentnumber}/combinacao{combination}{instance}.txt'
    bt.execute(instance_path)



def run_experiment(experiment_number):
    print(f"Iniciando Experimento {experiment_number}")
    print("-----------------------------------")

    for combination in range(1, 4):
        for instance in range(1, 11):
            W, V, n = get_experiment_data(experiment_number, combination)
            print(f"Processando instância {instance} - Combinação {combination}: W={W}, V={V}, n={n}")

            # dynamic_programming_experiment(experiment_number, combination, instance)
            backtracking_experiment(experiment_number, combination, instance)


if name == "main":
    run_experiment(1)
    run_experiment(2)
    run_experiment(3)  # Altere o número para 2 ou 3 para outros experimentos