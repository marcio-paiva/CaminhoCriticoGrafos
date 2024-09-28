import csv
from collections import defaultdict, deque

# Função para ler o arquivo CSV e construir o grafo
def carregar_grafo(arquivo):
    grafo = defaultdict(list)
    duracao = {}
    nomes = {}
    
    with open(arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            codigo = row['Código']
            nome = row['Nome']
            periodo = int(row['Período'])
            dur = int(row['Duração'])
            dependencias = row['Dependências'].split(',') if row['Dependências'] else []
            
            duracao[codigo] = dur
            nomes[codigo] = nome
            
            for dep in dependencias:
                grafo[dep].append(codigo)
    
    return grafo, duracao, nomes

# Algoritmo para encontrar o caminho crítico (caminho máximo)
def encontrar_caminho_critico(grafo, duracao):
    distancias = defaultdict(lambda: -float('inf'))  # Inicializa com -∞
    distancias['s'] = 0  # O nó inicial tem distância 0
    predecessores = {}

    # Ordenação topológica para evitar ciclos
    def ordenacao_topologica(grafo):
        grau_entrada = defaultdict(int)
        for u in grafo:
            for v in grafo[u]:
                grau_entrada[v] += 1
        fila = deque([u for u in grafo if grau_entrada[u] == 0])
        ordem = []
        while fila:
            u = fila.popleft()
            ordem.append(u)
            for v in grafo[u]:
                grau_entrada[v] -= 1
                if grau_entrada[v] == 0:
                    fila.append(v)
        return ordem

    # Ordenação topológica para processar o grafo
    ordem = ordenacao_topologica(grafo)

    # Relaxamento das arestas na ordem topológica
    for u in ordem:
        for v in grafo[u]:
            if distancias[v] < distancias[u] + duracao.get(u, 0):  # Usa duracao.get para evitar KeyError
                distancias[v] = distancias[u] + duracao.get(u, 0)
                predecessores[v] = u

    # Caminho crítico
    caminho_critico = []
    u = 't'  # Nó de destino
    while u in predecessores:
        caminho_critico.append(u)
        u = predecessores[u]
    caminho_critico.append('s')
    caminho_critico.reverse()

    return caminho_critico, distancias['t']

# Função para exibir o caminho crítico
def exibir_caminho_critico(caminho_critico, nomes, duracao_total):
    print("Caminho Crítico:")
    for codigo in caminho_critico[1:-1]:
        print(f"- {nomes[codigo]}")
    print(f"\nTempo Mínimo: {duracao_total}")

# Função principal de interação com o usuário
def main():
    while True:
        arquivo = input("Informe o arquivo (0 para sair): ")
        if arquivo == "0":
            break

        print("\nProcessando...")
        grafo, duracao, nomes = carregar_grafo(arquivo)
        
        # Adiciona nós fictícios "s" e "t" para representar o início e o fim
        for codigo in nomes:
            if all(codigo not in grafo[dep] for dep in grafo):
                grafo['s'].append(codigo)
            if not grafo[codigo]:
                grafo[codigo].append('t')
        
        # Adiciona duração zero para os nós fictícios "s" e "t"
        duracao['s'] = 0
        duracao['t'] = 0

        caminho_critico, duracao_total = encontrar_caminho_critico(grafo, duracao)
        exibir_caminho_critico(caminho_critico, nomes, duracao_total)

if __name__ == "__main__":
    main()
