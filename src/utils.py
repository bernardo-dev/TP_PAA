import os
import consts as c
import pandas as pd
import csv

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

def salvar_resultado(arquivo_saida, num_itens, W, V, lucro, tempo, itens_escolhidos):
    """
    Salva os dados em CSV para facilitar a geração de gráficos depois 
    """
    # Cria o diretório se não existir
    diretorio = os.path.dirname(arquivo_saida)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    existe = os.path.isfile(arquivo_saida)
    with open(arquivo_saida, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Cria cabeçalho se o arquivo não existir
        if not existe:
            writer.writerow(['Num_Itens', 'Cap_Peso', 'Cap_Volume', 'Lucro_Max', 'Tempo_Exec(s)', 'Itens_Ids'])
        
        writer.writerow([num_itens, W, V, lucro, tempo, str(itens_escolhidos)])
    