import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys
from colorama import init, Fore, Style

init(autoreset=True)

COLOR_INFO = Fore.CYAN + Style.BRIGHT
COLOR_ERROR = Fore.RED + Style.BRIGHT
COLOR_WARN = Fore.YELLOW + Style.BRIGHT

SOLUTIONS_DP = 'dp/exp'
SOLUTIONS_BB = 'bb/exp'
SOLUTIONS_BT = 'bt/exp'

def plotar_grafico_dispersao(experimento):
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Iniciando plotar_grafico_dispersao: experimento={experimento}")

    arquivo_saida = combina_resultados(experimento)
    print(f"\t{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivo combinado para plotagem: {arquivo_saida}")

    if not os.path.exists(arquivo_saida):
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Arquivo de saída não encontrado: {arquivo_saida}")
        raise FileNotFoundError(f"Arquivo {arquivo_saida} não encontrado")
    
    df = pd.read_csv(arquivo_saida)
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Dados carregados: {len(df)} linhas")
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Colunas: {df.columns.tolist()}")
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Algoritmos únicos: {df['Algoritmo'].unique().tolist()}")
    
    if experimento == 1:
        x_col, x_label = 'Num_Itens', 'Quantidade de Itens'
    elif experimento == 2:
        x_col, x_label = 'Cap_Peso', 'Peso da Mochila'
    elif experimento == 3:
        x_col, x_label = 'Cap_Volume', 'Volume da Mochila'
    else:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Experimento inválido: {experimento}")
        raise ValueError("Experimento deve ser 1, 2 ou 3")

    plt.figure(figsize=(12, 6))
    
    cores = {'DP': '#1f77b4', 'BT': "#ffb30e", 'BB': "#df08b0"}
    
    for algoritmo, cor in cores.items():
        df_algo = df[df['Algoritmo'] == algoritmo]
        print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Plotando algoritmo={algoritmo} com {len(df_algo)} pontos")
        if len(df_algo) > 0:
            plt.scatter(df_algo[x_col], df_algo['Tempo_Exec(s)'], 
                       label=algoritmo, alpha=0.6, s=50, color=cor)
        else:
            print(f"{COLOR_WARN}[WARN]{Style.RESET_ALL} Nenhum dado encontrado para algoritmo={algoritmo}")
    
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel('Tempo de Execução (s)', fontsize=12)
    plt.title(f'Experimento {experimento}: {x_label} vs Tempo de Execução')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Finalizado plotar_grafico_dispersao: experimento={experimento}")

def combina_csv(arquivo_saida, arquivos_para_combinar):
    diretorio = os.path.dirname(arquivo_saida)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Diretório criado: {diretorio}")

    with open(arquivo_saida, 'w', newline='') as csvfile_out:
        writer = csv.writer(csvfile_out)
        writer.writerow(['Algoritmo', 'Num_Itens', 'Cap_Peso', 'Cap_Volume', 'Lucro_Max', 'Tempo_Exec(s)', 'Itens_Ids'])
        print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivo CSV criado: {arquivo_saida}")
        
        print(f"\t{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivos para combinar: {arquivos_para_combinar}")

        for arquivo in arquivos_para_combinar:
            if not os.path.exists(arquivo):
                print(f"{COLOR_WARN}[WARN]{Style.RESET_ALL} Arquivo não encontrado para combinar: {arquivo}")
                continue
            
            with open(arquivo, 'r') as csvfile_in:
                print(f"\t{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivo pronto para combinar: {arquivo}")
                reader = csv.reader(csvfile_in)
                next(reader)  # Pula o cabeçalho
                
                algoritmo = ''
                if 'dp' in arquivo:
                    algoritmo = 'DP'
                elif 'bb' in arquivo:
                    algoritmo = 'BB'
                elif 'bt' in arquivo:
                    algoritmo = 'BT'
                
                for row in reader:
                    writer.writerow([algoritmo] + row)

def combina_resultados(experimento):
    arquivos_para_combinar = []
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Iniciando combina_resultados: experimento={experimento}")
    
    for algo in [SOLUTIONS_BB, SOLUTIONS_BT, SOLUTIONS_DP]:
        
        dir_exp = algo + f'{experimento}/'

        if os.path.exists(dir_exp):
            print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Diretório encontrado: {dir_exp}")
            for arquivo in os.listdir(dir_exp):
                if arquivo.endswith('.csv'):
                    arquivos_para_combinar.append(os.path.join(dir_exp, arquivo))
        else:
            print(f"{COLOR_WARN}[WARN]{Style.RESET_ALL} Diretório não encontrado: {dir_exp}")

    arquivo_saida = os.path.join(os.path.dirname(__file__), f'combined_exp{experimento}.csv')
    combina_csv(arquivo_saida, arquivos_para_combinar)
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivo combinado gerado: {arquivo_saida}")
    return arquivo_saida

if __name__ == "__main__":
    try:
        plotar_grafico_dispersao(1)
    except Exception as e:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} {e}")