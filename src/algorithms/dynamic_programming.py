import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils as ut
import consts as c
import numpy as np
import time

def execute(instance, exp_number):
    W, V, items = ut.read_instance(instance)

    start_time = time.time()
    dp_table = dynamic_programming(W, V, items)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\t\tExecution time: {execution_time:.6f} seconds")

    solution = dp_table[len(items)][W][V]
    selected_items, current_weight, current_volume = items_selected(dp_table, items, W, V)

    print(f"\t\tMaximum value achievable: {solution}")
    print(f"\t\tWeight: {current_weight} / {W}")
    print(f"\t\tWeight: {current_volume} / {V}")
    print(f"\t\tSelected items (IDs): {sorted(selected_items)}")

    ut.salvar_resultado(
        c.SOLUTIONS_DP + f'{exp_number}/{W}_{V}_{len(items)}.csv',
        len(items),
        W,
        V,
        solution,
        execution_time,
        [selected_items] 
    )

    return solution

def dynamic_programming(W, V, items):
    n = len(items)
    dp = np.zeros((n + 1, W + 1, V + 1), dtype=int)

    for i in range(1, n + 1):
        for w in range(1, W + 1):
            for v in range(1, V + 1):
                wi, vi, val_i = items[i - 1]
                if wi <= w and vi <= v:
                    dp[i][w][v] = max(dp[i - 1][w][v], dp[i - 1][w - wi][v - vi] + val_i)
                else:
                    dp[i][w][v] = dp[i - 1][w][v]

    return dp 

def items_selected(dp, items, W, V):
    n = len(items)
    w, v = W, V
    selected_items = []

    for i in range(n, 0, -1):
        if dp[i][w][v] != dp[i - 1][w][v]:
            selected_items.append(i - 1)  
            wi, vi, val_i = items[i - 1]
            w -= wi
            v -= vi

    selected_items.reverse()  
    return selected_items, W - w, V - v