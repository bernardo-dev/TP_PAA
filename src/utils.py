import os
from consts import LOG_DIR
import consts as c
import pandas as pd

def read_instance(instance_path):
    if not os.path.exists(instance_path):
        raise FileNotFoundError(f"Arquivo {instance_path} não encontrado")

    with open(instance_path, 'r') as file:
        lines = file.readlines()

    backpack_weight, backpack_volume = map(int, lines[0].strip().split('\t'))
    itens = []

    for line in lines[1:]:
        weight, volume, value = map(int, line.strip().split('\t'))
        itens.append([weight, volume, value])

    return backpack_weight, backpack_volume, itens


def save_logs(experiment, instance, algorithm, log_type, log, write_mode='a'):
    if experiment not in [1, 2] or not (1 <= instance <= 20):
        raise ValueError("Experimento deve ser 1 ou 2 e instance deve estar entre 1 e 20")

    base_path = os.path.join(EXPERIMENT_1_DIR if experiment == 1 else EXPERIMENT_2_DIR, LOG_DIR, algorithm)
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    file_path = os.path.join(base_path, f'{algorithm}_{log_type}_logs.txt')
    with open(file_path, write_mode) as file:
        if isinstance(log, tuple):
            file.write('\t'.join(map(str, log)) + '\n')
        else:
            file.write(f'{log}\n')

def last_instance_executed(experiment, algorithm):
    base_path = os.path.join(EXPERIMENT_1_DIR if experiment == 1 else EXPERIMENT_2_DIR, LOG_DIR, algorithm)
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    file_path = os.path.join(base_path, f'{algorithm}_{c.LAST_INSTANCE_EXECUTED}_logs.txt')
    if not os.path.exists(file_path):
        return 0

    with open(file_path, 'r') as file:
        instance = int(file.read().strip())
        return instance
    
def delete_logs(experiment, algorithm):
    base_path = os.path.join(EXPERIMENT_1_DIR if experiment == 1 else EXPERIMENT_2_DIR, LOG_DIR, algorithm)
    if os.path.exists(base_path):
        for file_name in os.listdir(base_path):
            file_path = os.path.join(base_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    

def read_results(experiment, algorithm):
    base_path = os.path.join(EXPERIMENT_1_DIR if experiment == 1 else EXPERIMENT_2_DIR, LOG_DIR, algorithm)
    if not os.path.exists(base_path):
        return [0] * 20

    file_path = os.path.join(base_path, f'{algorithm}_{c.EXECUTION_TIME}_logs.txt')
    if not os.path.exists(file_path):
        return [0] * 20
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        results = [float(line.strip().split('\t')[2]) for line in lines]

    return results

def plot_results(experiment):
    dynamic_programming_results = read_results(experiment, c.DYNAMIC_PROGRAMMING)
    branch_and_bound_results = read_results(experiment, c.BRANCH_AND_BOUND)
    # backtracking_results = read_results(experiment, c.BACKTRACKING)

    df = pd.DataFrame({
        'Instance': range(1, 21),
        'Dynamic Programming': dynamic_programming_results,
        'Branch and Bound': branch_and_bound_results,
        # 'Backtracking': backtracking_results
    })

    ax = df.plot(x='Instance', y=['Dynamic Programming', 'Branch and Bound'], kind='bar', title=f'Experimento {experiment}')
    ax.set_ylabel('Tempo de execução (s)')
    ax.set_xlabel('Instância')
    ax.legend(['Programação Dinâmica', 'Branch and Bound'])
    #Preciso criar a pasta images na raiz do projeto
    if not os.path.exists('images'):
        os.makedirs('images')
    ax.figure.savefig(f'images/experiment_{experiment}.png')
