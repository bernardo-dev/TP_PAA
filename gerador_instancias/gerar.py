import random
import os


def get_experiment_data(experiment_number, combination):
    """
    Retorna os dados W, V e n baseado no experimento e combinação.
    
    Args:
        experiment_number: Número do experimento (1, 2 ou 3)
        combination: Número da combinação (1, 2 ou 3)
    
    Returns:
        Tupla contendo (W, V, n)
    """
    data = {
        1: {
            1: (200, 200, 100),
            2: (200, 200, 1000),
            3: (200, 200, 10000),
        },
        2: {
            1: (100, 100, 1000),
            2: (250, 100, 1000),
            3: (500, 100, 1000),
        },
        3: {
            1: (100, 100, 1000),
            2: (100, 250, 1000),
            3: (100, 500, 1000),
        },
    }
    
    W, V, n = data[experiment_number][combination]
    return W, V, n

def gerar_instancias():
    # Semente fixa para garantir repetibilidade dos dados em diferentes computadores
    random.seed(42)
    
    # Intervalo fixo para geração dos itens para permitir comparação consistente
    # Pesos e volumes dos itens entre 1 e 50.
    # Valores dos itens entre 1 e 100.
    peso_max_item = 50
    volume_max_item = 50
    valor_maximo_item = 100
    
    OUTPUT_DIR = "instancias"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Gerando instâncias em '{OUTPUT_DIR}'...")
    
    count = 0
    
    # EXPERIMENTO 1 - Alterando a quantidade de itens
    print("Experimento 1: Alterando quantidade de itens...")
    exp1_dir = os.path.join(OUTPUT_DIR, "experimento_1")
    os.makedirs(exp1_dir, exist_ok=True)
    
    for combinacao_idx in range(1, 4):
        peso_mochila, volume_mochila, quantidade = get_experiment_data(1, combinacao_idx)
        
        for i in range(1, 11):
            filename = f"combinacao{combinacao_idx}_{i}.txt"
            filepath = os.path.join(exp1_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"{peso_mochila}\t{volume_mochila}\n")
                
                for _ in range(quantidade):
                    peso_item = random.randint(1, peso_max_item)
                    volume_item = random.randint(1, volume_max_item)
                    valor_item = random.randint(1, valor_maximo_item)
                    
                    f.write(f"{peso_item}\t{volume_item}\t{valor_item}\n")
            count += 1
    
    # EXPERIMENTO 2 - Alterando o peso da mochila
    print("Experimento 2: Alterando peso da mochila...")
    exp2_dir = os.path.join(OUTPUT_DIR, "experimento_2")
    os.makedirs(exp2_dir, exist_ok=True)
    
    for combinacao_idx in range(1, 4):
        peso_mochila, volume_mochila, quantidade = get_experiment_data(2, combinacao_idx)
        
        for i in range(1, 11):
            filename = f"combinacao{combinacao_idx}_{i}.txt"
            filepath = os.path.join(exp2_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"{peso_mochila}\t{volume_mochila}\n")
                
                for _ in range(quantidade):
                    peso_item = random.randint(1, peso_max_item)
                    volume_item = random.randint(1, volume_max_item)
                    valor_item = random.randint(1, valor_maximo_item)
                    
                    f.write(f"{peso_item}\t{volume_item}\t{valor_item}\n")
            count += 1
    
    # EXPERIMENTO 3 - Alterando o volume da mochila
    print("Experimento 3: Alterando volume da mochila...")
    exp3_dir = os.path.join(OUTPUT_DIR, "experimento_3")
    os.makedirs(exp3_dir, exist_ok=True)
    
    for combinacao_idx in range(1, 4):
        peso_mochila, volume_mochila, quantidade = get_experiment_data(3, combinacao_idx)
        
        for i in range(1, 11):
            filename = f"combinacao{combinacao_idx}_{i}.txt"
            filepath = os.path.join(exp3_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"{peso_mochila}\t{volume_mochila}\n")
                
                for _ in range(quantidade):
                    peso_item = random.randint(1, peso_max_item)
                    volume_item = random.randint(1, volume_max_item)
                    valor_item = random.randint(1, valor_maximo_item)
                    
                    f.write(f"{peso_item}\t{volume_item}\t{valor_item}\n")
            count += 1
                    
    print(f"Total de arquivos gerados: {count}")

if __name__ == "__main__":
    gerar_instancias()
