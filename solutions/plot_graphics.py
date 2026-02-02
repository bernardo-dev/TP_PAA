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

FULL_NAMES = {
    'DP': 'Dynamic Programming',
    'BT': 'Backtracking',
    'BB': 'Branch and Bound'
}

def plotar_grafico_dispersao(experimento, algoritmos=None):
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Iniciando plotar_grafico_dispersao: experimento={experimento}")

    arquivo_saida = combina_resultados(experimento)
    print(f"\t{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivo combinado para plotagem: {arquivo_saida}")

    if not os.path.exists(arquivo_saida):
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Arquivo de saída não encontrado: {arquivo_saida}")
        raise FileNotFoundError(f"Arquivo {arquivo_saida} não encontrado")
    
    df = pd.read_csv(arquivo_saida)
    
    if experimento == 1:
        x_col, x_label = 'Num_Itens', 'Quantidade de Itens'
    elif experimento == 2:
        x_col, x_label = 'Cap_Peso', 'Peso da Mochila'
    elif experimento == 3:
        x_col, x_label = 'Cap_Volume', 'Volume da Mochila'
    elif experimento == 4:
        x_col, x_label = 'Cap_Volume', 'Volume da Mochila'
    else:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Experimento inválido: {experimento}")
        raise ValueError("Experimento deve ser 1, 2, 3 ou 4")

    if algoritmos is None:
        algoritmos = ['DP', 'BT', 'BB']

    cores = {k: v for k, v in {'DP': '#1f77b4', 'BT': "#ffb30e", 'BB': "#df08b0"}.items() if k in algoritmos}

    plt.figure(figsize=(12, 6))
    
    for algoritmo in algoritmos:
        cor = cores[algoritmo]
        df_algo = df[df['Algoritmo'] == algoritmo]
        print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Plotando algoritmo={algoritmo} com {len(df_algo)} pontos")
        if len(df_algo) > 0:
            plt.scatter(df_algo[x_col], df_algo['Tempo_Exec(s)'], 
                       label=FULL_NAMES[algoritmo], alpha=0.6, s=50, color=cor)
        else:
            print(f"{COLOR_WARN}[WARN]{Style.RESET_ALL} Nenhum dado encontrado para algoritmo={algoritmo}")
    
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel('Tempo de Execução (s)', fontsize=12)
    plt.title(f'Experimento {experimento}: {x_label} vs Tempo de Execução')
    plt.legend(title='Algoritmo')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"graficos/experimento_{experimento}_dispersao.png")
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Finalizado plotar_grafico_dispersao: experimento={experimento}")

def plotar_grafico_boxplot(experimento, algoritmos=None):
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Iniciando plotar_grafico_boxplot: experimento={experimento}")

    arquivo_saida = combina_resultados(experimento)
    print(f"\t{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivo combinado para plotagem: {arquivo_saida}")

    if not os.path.exists(arquivo_saida):
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Arquivo de saída não encontrado: {arquivo_saida}")
        raise FileNotFoundError(f"Arquivo {arquivo_saida} não encontrado")
    
    df = pd.read_csv(arquivo_saida)
    
    if experimento == 1:
        x_label = 'Quantidade de Itens'
    elif experimento == 2:
        x_label = 'Peso da Mochila'
    elif experimento == 3:
        x_label = 'Volume da Mochila'
    elif experimento == 4:
        x_label = 'Volume da Mochila'
    else:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Experimento inválido: {experimento}")
        raise ValueError("Experimento deve ser 1, 2, 3 ou 4")

    if algoritmos is None:
        algoritmos = ['DP', 'BT', 'BB']

    cores_dict = {'DP': '#1f77b4', 'BT': "#ffb30e", 'BB': "#df08b0"}
    cores = [cores_dict[algo] for algo in algoritmos]

    plt.figure(figsize=(10, 6))
    
    # Preparar dados para o boxplot
    dados_boxplot = []
    labels = []
    
    for algoritmo in algoritmos:
        df_algo = df[df['Algoritmo'] == algoritmo]
        print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Algoritmo={algoritmo} com {len(df_algo)} dados")
        if len(df_algo) > 0:
            dados_boxplot.append(df_algo['Tempo_Exec(s)'].values)
            labels.append(FULL_NAMES[algoritmo])
        else:
            print(f"{COLOR_WARN}[WARN]{Style.RESET_ALL} Nenhum dado encontrado para algoritmo={algoritmo}")
    
    if dados_boxplot:
        bp = plt.boxplot(dados_boxplot, labels=labels, patch_artist=True, widths=0.6)
        
        # Colorir cada boxplot
        for patch, cor in zip(bp['boxes'], cores[:len(labels)]):
            patch.set_facecolor(cor)
            patch.set_alpha(0.6)
        
        plt.xlabel('Algoritmo', fontsize=12)
        plt.ylabel('Tempo de Execução (s)', fontsize=12)
        plt.title(f'Experimento {experimento}: Distribuição do Tempo de Execução por Algoritmo')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        #plt.show()
        plt.savefig(f"graficos/experimento_{experimento}_boxplot.png")
    else:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Nenhum dado disponível para plotar boxplot")
    
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Finalizado plotar_grafico_boxplot: experimento={experimento}")

def plotar_grafico_boxplot_ate_40_itens(experimento, algoritmos=None):
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Iniciando plotar_grafico_boxplot_ate_40_itens: experimento={experimento}")

    arquivo_saida = combina_resultados(experimento)
    print(f"\t{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivo combinado para plotagem: {arquivo_saida}")

    if not os.path.exists(arquivo_saida):
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Arquivo de saída não encontrado: {arquivo_saida}")
        raise FileNotFoundError(f"Arquivo {arquivo_saida} não encontrado")
    
    df = pd.read_csv(arquivo_saida)
    
    # Filtrar para linhas com até 40 itens
    df = df[df['Num_Itens'] <= 40]
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Dados filtrados para até 40 itens: {len(df)} linhas restantes")
    
    if experimento == 1:
        x_label = 'Quantidade de Itens'
    elif experimento == 2:
        x_label = 'Peso da Mochila'
    elif experimento == 3:
        x_label = 'Volume da Mochila'
    elif experimento == 4:
        x_label = 'Volume da Mochila'
    else:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Experimento inválido: {experimento}")
        raise ValueError("Experimento deve ser 1, 2, 3 ou 4")

    if algoritmos is None:
        algoritmos = ['DP', 'BT', 'BB']

    cores_dict = {'DP': '#1f77b4', 'BT': "#ffb30e", 'BB': "#df08b0"}
    cores = [cores_dict[algo] for algo in algoritmos]

    plt.figure(figsize=(10, 6))
    
    # Preparar dados para o boxplot
    dados_boxplot = []
    labels = []
    
    for algoritmo in algoritmos:
        df_algo = df[df['Algoritmo'] == algoritmo]
        print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Algoritmo={algoritmo} com {len(df_algo)} dados")
        if len(df_algo) > 0:
            dados_boxplot.append(df_algo['Tempo_Exec(s)'].values)
            labels.append(FULL_NAMES[algoritmo])
        else:
            print(f"{COLOR_WARN}[WARN]{Style.RESET_ALL} Nenhum dado encontrado para algoritmo={algoritmo}")
    
    if dados_boxplot:
        bp = plt.boxplot(dados_boxplot, labels=labels, patch_artist=True, widths=0.6)
        
        # Colorir cada boxplot
        for patch, cor in zip(bp['boxes'], cores[:len(labels)]):
            patch.set_facecolor(cor)
            patch.set_alpha(0.6)
        
        plt.xlabel('Algoritmo', fontsize=12)
        plt.ylabel('Tempo de Execução (s)', fontsize=12)
        plt.title(f'Experimento {experimento}: Distribuição do Tempo de Execução por Algoritmo (até 40 itens)')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        #plt.show()
        plt.savefig(f"graficos/experimento_{experimento}_boxplot_ate_40.png")
    else:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Nenhum dado disponível para plotar boxplot")
    
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Finalizado plotar_grafico_boxplot_ate_40_itens: experimento={experimento}")

def plotar_grafico_tamanho_vs_tempo(experimento, algoritmos=None):
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Iniciando plotar_grafico_tamanho_vs_tempo: experimento={experimento}")

    arquivo_saida = combina_resultados(experimento)
    print(f"\t{COLOR_INFO}[INFO]{Style.RESET_ALL} Arquivo combinado para plotagem: {arquivo_saida}")

    if not os.path.exists(arquivo_saida):
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Arquivo de saída não encontrado: {arquivo_saida}")
        raise FileNotFoundError(f"Arquivo {arquivo_saida} não encontrado")
    
    df = pd.read_csv(arquivo_saida)
    
    if experimento == 1:
        x_col, x_label = 'Num_Itens', 'Quantidade de Itens'
    elif experimento == 2:
        x_col, x_label = 'Cap_Peso', 'Peso da Mochila'
    elif experimento == 3:
        x_col, x_label = 'Cap_Volume', 'Volume da Mochila'
    elif experimento == 4:
        x_col, x_label = 'Num_Itens', 'Quantidade de Itens'
    else:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} Experimento inválido: {experimento}")
        raise ValueError("Experimento deve ser 1, 2, 3 ou 4")

    if algoritmos is None:
        algoritmos = ['DP', 'BT', 'BB']

    cores = {k: v for k, v in {'DP': '#1f77b4', 'BT': "#ffb30e", 'BB': "#df08b0"}.items() if k in algoritmos}

    plt.figure(figsize=(12, 6))
    
    unique_x_values = set()
    
    for algoritmo in algoritmos:
        cor = cores[algoritmo]
        df_algo = df[df['Algoritmo'] == algoritmo]
        print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Plotando algoritmo={algoritmo} com {len(df_algo)} pontos")
        if len(df_algo) > 0:
            # Agrupar por tamanho da instância e calcular média do tempo
            df_grouped = df_algo.groupby(x_col)['Tempo_Exec(s)'].mean().reset_index()
            df_grouped = df_grouped.sort_values(by=x_col)
            plt.plot(df_grouped[x_col], df_grouped['Tempo_Exec(s)'], 
                     label=FULL_NAMES[algoritmo], marker='o', color=cor, linewidth=2)
            unique_x_values.update(df_grouped[x_col].values)
        else:
            print(f"{COLOR_WARN}[WARN]{Style.RESET_ALL} Nenhum dado encontrado para algoritmo={algoritmo}")
    
    # Definir ticks do eixo x apenas para as quantidades existentes
    if unique_x_values:
        plt.xticks(sorted(unique_x_values))
    
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel('Tempo de Execução Médio (s)', fontsize=12)
    plt.title(f'Experimento {experimento}: {x_label} vs Tempo de Execução Médio')
    plt.legend(title='Algoritmo')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"graficos/experimento_{experimento}_tamanho_vs_tempo.png")
    print(f"{COLOR_INFO}[INFO]{Style.RESET_ALL} Finalizado plotar_grafico_tamanho_vs_tempo: experimento={experimento}")

def combina_csv(arquivo_saida, arquivos_para_combinar):
    diretorio = os.path.dirname(arquivo_saida)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)

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
        algoritmos = ['DP', 'BB', 'BT']
        #algoritmos = ['DP', 'BB']
        experimento = 1
        #plotar_grafico_boxplot(experimento=experimento, algoritmos=algoritmos)
        #plotar_grafico_dispersao(experimento=experimento, algoritmos=algoritmos)
        #plotar_grafico_tamanho_vs_tempo(experimento=experimento, algoritmos=algoritmos)
        plotar_grafico_boxplot_ate_40_itens(experimento=experimento, algoritmos=algoritmos)
    except Exception as e:
        print(f"{COLOR_ERROR}[ERROR]{Style.RESET_ALL} {e}")