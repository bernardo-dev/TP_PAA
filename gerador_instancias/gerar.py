import random
import os

def gerar_instancias():
    # Semente fixa para garantir repetibilidade dos dados em diferentes computadores
    random.seed(42)

    # Definições de "Pequeno", "Médio", "Grande"
    opcoes_quantidade_item = {'P': 10, 'M': 25, 'G': 50}
    # n=50 é um tamanho razoável para B&B/Backtracking exponencial. 
    # Se n=100+ algoritmos exatos não otimizados podem demorar muito, mas vamos incluir até 50 para garantir execução.
    
    opcoes_peso = {'P': 50, 'M': 250, 'G': 1000}
    opcoes_volume = {'P': 50, 'M': 250, 'G': 1000}
    
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
    # Gera todas as combinações
    for rotulo_qtd, quantidade in opcoes_quantidade_item.items():
        for rotulo_peso, peso in opcoes_peso.items():
            for rotulo_volume, volume in opcoes_volume.items():
                
                # Gera 10 instâncias para esta configuração
                for i in range(1, 11):
                    # Nome do arquivo descritivo
                    filename = f"in_qnt-{quantidade}_W-{peso}_V-{volume}_{i}.txt"
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    
                    with open(filepath, 'w') as f:
                        # Primeira linha: W V
                        f.write(f"{peso}\t{volume}\n")
                        
                        # Demais linhas: Peso Volume Valor
                        for _ in range(quantidade):
                            peso_item = random.randint(1, peso_max_item)
                            volume_item = random.randint(1, volume_max_item)
                            valor_item = random.randint(1, valor_maximo_item)
                            
                            f.write(f"{peso_item}\t{volume_item}\t{valor_item}\n")
                    count += 1
                    
    print(f"Total de arquivos gerados: {count}")

if __name__ == "__main__":
    gerar_instancias()
