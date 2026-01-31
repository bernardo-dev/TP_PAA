import random
import os

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
    peso_mochila = 200
    volume_mochila = 200
    quantidades = [100, 1000, 10000]
    
    for quantidade in quantidades:
        for i in range(1, 11):
            filename = f"exp1_qnt-{quantidade}_W-{peso_mochila}_V-{volume_mochila}_{i}.txt"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
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
    volume_mochila = 100
    quantidade = 1000
    pesos = [100, 250, 500]
    
    for peso_mochila in pesos:
        for i in range(1, 11):
            filename = f"exp2_qnt-{quantidade}_W-{peso_mochila}_V-{volume_mochila}_{i}.txt"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
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
    peso_mochila = 100
    quantidade = 1000
    volumes = [100, 250, 500]
    
    for volume_mochila in volumes:
        for i in range(1, 11):
            filename = f"exp3_qnt-{quantidade}_W-{peso_mochila}_V-{volume_mochila}_{i}.txt"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
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
