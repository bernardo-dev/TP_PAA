import sys
import time
import os
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as ut
import consts as c

def execute (instance_path, exp_number):
    W_max, V_max, itens = ut.read_instance(instance_path)
    
    if W_max is None:
        print(f"Erro ao processar {instance_path}, pulando...\n")
        return

    print(f"\tCapacidade W: {W_max}, Capacidade V: {V_max}, Número de Itens: {len(itens)}")

    inicio = time.time()
    
    lucro_max, itens_escolhidos = backtracking_solver(itens, W_max, V_max, len(itens))
    
    fim = time.time()
    tempo_execucao = fim - inicio

    print(f"\t\tLucro Máximo: {lucro_max}")
    print(f"\t\tItens escolhidos (IDs): {sorted(itens_escolhidos)}")
    print(f"\t\tTempo de execução: {tempo_execucao:.6f} segundos")
    
    ut.salvar_resultado(
        c.SOLUTIONS_BT + f'{exp_number}/{W_max}_{V_max}_{len(itens)}.csv',
        len(itens),
        W_max,
        V_max,
        lucro_max,
        tempo_execucao,
        sorted(itens_escolhidos)
    )

def backtracking_solver(itens, capacidade_w, capacidade_v, n):
    """
    Função recursiva de Backtracking
    Retorna: (melhor_valor, lista_de_itens_escolhidos)
    0 = peso
    1 = volume
    2 = valor
    """
    # Caso base: sem itens ou capacidades esgotadas
    if n == 0 or (capacidade_w == 0 and capacidade_v == 0):
        return 0, []

    item_atual = itens[n-1]

    # restrição: item não cabe (por peso ou volume)
    if item_atual[0] > capacidade_w or item_atual[1] > capacidade_v:
        return backtracking_solver(itens, capacidade_w, capacidade_v, n-1)

    else:
        # Incluir o item (Soma valor, subtrai capacidades)
        val_com, itens_com = backtracking_solver(
            itens, 
            capacidade_w - item_atual[0], 
            capacidade_v - item_atual[1], 
            n-1
        )
        val_com += item_atual[2]

        # Não incluir o item
        val_sem, itens_sem = backtracking_solver(itens, capacidade_w, capacidade_v, n-1)

        # Decisão: Retorna o que der maior valor
        if val_com > val_sem:
            return val_com, itens_com + [n-1]
        else:
            return val_sem, itens_sem