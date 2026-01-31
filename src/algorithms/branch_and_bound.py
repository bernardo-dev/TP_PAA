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
    solution, selected_items, current_weight, current_volume = branch_and_bound(W, V, items)
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\t\tExecution time: {execution_time:.6f} seconds")
    print(f"\t\tMaximum value achievable: {solution}")
    print(f"\t\tWeight: {current_weight} / {W}")
    print(f"\t\tVolume: {current_volume} / {V}")
    print(f"\t\tSelected items (IDs): {sorted(selected_items)}")

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

    remaining = items[nivel:]

    # Bound for weight only
    bound_w = 0
    peso_rest = W - peso
    sorted_w = sorted(remaining, key=lambda x: x[2]/x[0] if x[0] > 0 else 0, reverse=True)
    for w_i, _, val_i in sorted_w:
        if w_i <= peso_rest:
            bound_w += val_i
            peso_rest -= w_i
        else:
            bound_w += (peso_rest / w_i) * val_i if w_i > 0 else 0
            break

    # Bound for volume only
    bound_v = 0
    vol_rest = V - volume
    sorted_v = sorted(remaining, key=lambda x: x[2]/x[1] if x[1] > 0 else 0, reverse=True)
    for _, vol_i, val_i in sorted_v:
        if vol_i <= vol_rest:
            bound_v += val_i
            vol_rest -= vol_i
        else:
            bound_v += (vol_rest / vol_i) * val_i if vol_i > 0 else 0
            break

    bound = lucro + min(bound_w, bound_v)
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

    for idx, item in itens_ordenados:
        w_i, vol_i, val_i = item
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

    peso_total = sum(items[idx][0] for idx in melhor_solucao)
    volume_total = sum(items[idx][1] for idx in melhor_solucao)
    return melhor_lucro, melhor_solucao, peso_total, volume_total
