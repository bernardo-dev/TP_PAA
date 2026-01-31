import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as ut
import consts as c
import heapq
import time

def execute(instance, exp_number):
    W, V, items = ut.read_instance(instance)

    start_time = time.time()
    solution, selected_items = branch_and_bound(W, V, items)
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\t\tExecution time: {execution_time:.6f} seconds")
    print(f"\t\tMaximum value achievable: {solution}")

    ut.salvar_resultado(
        c.SOLUTIONS_BB + f'{exp_number}/{W}_{V}_{len(items)}.csv',
        len(items),
        W,
        V,
        solution,
        execution_time,
        [selected_items]
    )

    return solution

def calcular_bound(nivel, lucro, peso, volume, items, W, V):
    if peso > W or volume > V:
        return -float('inf')

    bound = float(lucro)
    peso_restante = W - peso
    volume_restante = V - volume

    itens_restantes = sorted(
        items[nivel:],
        key=lambda x: x[2] / (x[0] + x[1]) if (x[0] + x[1]) > 0 else 0,
        reverse=True
    )

    for w_i, vol_i, val_i in itens_restantes:
        if w_i <= peso_restante and vol_i <= volume_restante:
            bound += val_i
            peso_restante -= w_i
            volume_restante -= vol_i
        else:
            fracao_peso = peso_restante / w_i if w_i > 0 else float('inf')
            fracao_volume = volume_restante / vol_i if vol_i > 0 else float('inf')
            fracao = min(fracao_peso, fracao_volume, 1.0)
            if fracao > 0:
                bound += fracao * val_i
            break

    return bound

def greedy_solution(items, W, V):
    itens_ordenados = sorted(
        enumerate(items),
        key=lambda x: x[1][2] / (x[1][0] + x[1][1]) if (x[1][0] + x[1][1]) > 0 else 0,
        reverse=True
    )

    peso_atual = 0
    volume_atual = 0
    lucro_total = 0
    selecionados = []

    for idx, (w_i, vol_i, val_i) in itens_ordenados:
        if peso_atual + w_i <= W and volume_atual + vol_i <= V:
            selecionados.append(idx)
            peso_atual += w_i
            volume_atual += vol_i
            lucro_total += val_i

    return lucro_total, sorted(selecionados)

def branch_and_bound(W, V, items):
    melhor_lucro, melhor_solucao = greedy_solution(items, W, V)

    heap = []
    bound_raiz = calcular_bound(0, 0, 0, 0, items, W, V)
    heapq.heappush(heap, (-bound_raiz, 0, 0, 0, 0, []))

    while heap:
        neg_bound, nivel, lucro, peso, volume, selecionados = heapq.heappop(heap)
        bound = -neg_bound

        if bound <= melhor_lucro:
            continue

        if nivel >= len(items):
            if lucro > melhor_lucro:
                melhor_lucro = lucro
                melhor_solucao = selecionados[:]
            continue

        w_i, vol_i, val_i = items[nivel]

        # Incluir item
        novo_peso = peso + w_i
        novo_volume = volume + vol_i
        if novo_peso <= W and novo_volume <= V:
            novo_lucro = lucro + val_i
            nova_solucao = selecionados + [nivel]

            if novo_lucro > melhor_lucro:
                melhor_lucro = novo_lucro
                melhor_solucao = nova_solucao[:]

            bound_com = calcular_bound(nivel + 1, novo_lucro, novo_peso, novo_volume, items, W, V)
            if bound_com > melhor_lucro:
                heapq.heappush(heap, (-bound_com, nivel + 1, novo_lucro, novo_peso, novo_volume, nova_solucao))

        # Não incluir item
        bound_sem = calcular_bound(nivel + 1, lucro, peso, volume, items, W, V)
        if bound_sem > melhor_lucro:
            heapq.heappush(heap, (-bound_sem, nivel + 1, lucro, peso, volume, selecionados[:]))

    return melhor_lucro, melhor_solucao
