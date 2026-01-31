import utils as ut
import consts as c
import numpy as np
import time

def execute(instance):
    W, V, items = ut.read_instance(instance)
    
    start_time = time.time()
    solution = dynamic_programming(W, V, items)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.6f} seconds")

    log_tuple = (W, len(items), execution_time)

    # ut.save_logs(instance, c.DYNAMIC_PROGRAMMING, c.EXECUTION_TIME, log_tuple)
    # ut.save_logs(instance, c.DYNAMIC_PROGRAMMING, c.SOLUTION_VALUE, solution)
    # ut.save_logs(instance, c.DYNAMIC_PROGRAMMING, c.LAST_INSTANCE_EXECUTED, instance, 'w')

    return solution

def dynamic_programming(W, V, items):
    
    n = len(items)
    dp = np.zeros((n + 1, W + 1, V + 1), dtype=int)

    for i in range(1, n + 1):
        for w in range(1, W + 1):
            for v in range(1, V + 1):
                wi, vi, vol_i = items[i - 1]
                if wi <= w and vol_i <= v:
                    dp[i][w][v] = max(dp[i - 1][w][v], dp[i - 1][w - wi][v - vol_i] + vi)
                else:
                    dp[i][w][v] = dp[i - 1][w][v]

    return dp[n][W][V]