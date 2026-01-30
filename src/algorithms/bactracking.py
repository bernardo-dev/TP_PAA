import time
import csv
import os

class Item:
    def __init__(self, id, peso, volume, valor):
        self.id = id
        self.peso = peso
        self.volume = volume
        self.valor = valor

def ler_arquivo(caminho_arquivo):
    itens = []
    try:
        with open(caminho_arquivo, 'r') as f:
            # Lê primeira linha
            linha1 = f.readline().split()
            W_max = int(linha1[0])
            V_max = int(linha1[1])
            
            # Lê os itens
            for i, linha in enumerate(f):
                dados = linha.split()
                if len(dados) >= 3:
                    # Peso, Volume, Valor 
                    itens.append(Item(i+1, int(dados[0]), int(dados[1]), int(dados[2])))
        return W_max, V_max, itens
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None, None, []

def backtracking_solver(itens, capacidade_w, capacidade_v, n):
    """
    Função recursiva de Backtracking
    Retorna: (melhor_valor, lista_de_itens_escolhidos)
    """
    # Caso base: sem itens ou capacidades esgotadas
    if n == 0 or (capacidade_w == 0 and capacidade_v == 0):
        return 0, []

    item_atual = itens[n-1]

    # restrição: item não cabe (por peso ou volume)
    if item_atual.peso > capacidade_w or item_atual.volume > capacidade_v:
        return backtracking_solver(itens, capacidade_w, capacidade_v, n-1)

    else:
        # Incluir o item (Soma valor, subtrai capacidades)
        val_com, itens_com = backtracking_solver(
            itens, 
            capacidade_w - item_atual.peso, 
            capacidade_v - item_atual.volume, 
            n-1
        )
        val_com += item_atual.valor

        # Não incluir o item
        val_sem, itens_sem = backtracking_solver(itens, capacidade_w, capacidade_v, n-1)

        # Decisão: Retorna o que der maior valor
        if val_com > val_sem:
            return val_com, itens_com + [item_atual.id]
        else:
            return val_sem, itens_sem

def salvar_resultado(arquivo_saida, num_itens, W, V, lucro, tempo, itens_escolhidos):
    """
    Salva os dados em CSV para facilitar a geração de gráficos depois 
    """
    existe = os.path.isfile(arquivo_saida)
    with open(arquivo_saida, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Cria cabeçalho se o arquivo não existir
        if not existe:
            writer.writerow(['Num_Itens', 'Cap_Peso', 'Cap_Volume', 'Lucro_Max', 'Tempo_Exec(s)', 'Itens_Ids'])
        
        writer.writerow([num_itens, W, V, lucro, tempo, str(itens_escolhidos)])

def main():
    arquivo_entrada = 'teste_grande.txt'
    arquivo_resultados = 'resultados_backtracking.csv'
    
    print(f"--- Processando {arquivo_entrada} ---")
    W_max, V_max, itens = ler_arquivo(arquivo_entrada)
    
    if W_max is None: return

    # Início da medição de tempo
    inicio = time.time()
    
    # Backtracking
    # len(itens) como índice inicial (de trás para frente)
    lucro_max, itens_escolhidos = backtracking_solver(itens, W_max, V_max, len(itens))
    
    fim = time.time()
    tempo_execucao = fim - inicio
    
    # Exibe resultados
    print(f"Lucro Máximo: {lucro_max}")
    print(f"Itens escolhidos (IDs): {sorted(itens_escolhidos)}")
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")
    
    # Salva para o relatório
    salvar_resultado(arquivo_resultados, len(itens), W_max, V_max, lucro_max, tempo_execucao, sorted(itens_escolhidos))
    print(f"Dados salvos em '{arquivo_resultados}' para análise futura.")

if __name__ == "__main__":
    main()