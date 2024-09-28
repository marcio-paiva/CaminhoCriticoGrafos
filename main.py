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
            dependencias = row['Dependências'].split(';') if row['Dependências'] else []

            duracao[codigo] = dur
            nomes[codigo] = nome

            for dep in dependencias:
                grafo[dep].append(codigo)

    return grafo, duracao, nomes

# Algoritmo para encontrar os caminhos críticos
def encontrar_caminhos_criticos(grafo, duracao):
    distancias = defaultdict(lambda: -float('inf'))
    distancias['s'] = 0
    predecessores = defaultdict(list)

    # Função interna para realizar a ordenação topológica
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
            if distancias[v] < distancias[u] + duracao.get(u, 0):
                distancias[v] = distancias[u] + duracao.get(u, 0)
                predecessores[v] = [u]  # Substitui a lista de predecessores
            elif distancias[v] == distancias[u] + duracao.get(u, 0):
                predecessores[v].append(u)  # Adiciona um novo predecessor

    # Caminhos críticos
    caminhos_criticos = []
    max_distancia = distancias['t']
    def encontrar_caminho(atual, caminho):
        if atual == 's':
            caminhos_criticos.append(caminho[::-1])  # Adiciona o caminho invertido
            return
        for pred in predecessores[atual]:
            encontrar_caminho(pred, caminho + [pred])

    # Inicia a busca pelo caminho crítico
    encontrar_caminho('t', ['t'])

    return caminhos_criticos, max_distancia

# Função para exibir os caminhos críticos
def exibir_caminhos_criticos(caminhos_criticos, nomes, duracao_total):
    print("Caminhos Críticos:")
    for caminho in caminhos_criticos:
        for codigo in caminho[1:-1]:  # Ignora 's' e 't'
            print(f"- {nomes[codigo]}")
        print()  # Linha em branco entre os caminhos
    print(f"Tempo Mínimo: {duracao_total}")

# Função principal de interação com o usuário
def main():
    while True:
        arquivo = input("Informe o arquivo (0 para sair): ")
        if arquivo == "0":
            break

        print("\nProcessando...")
        grafo, duracao, nomes = carregar_grafo(arquivo)

        # Adiciona nós fictícios "s" e "t"
        grafo['s'] = []
        grafo['t'] = []

        for codigo in nomes:
            if all(codigo not in grafo[dep] for dep in grafo):
                grafo['s'].append(codigo)
            if not grafo[codigo]:
                grafo[codigo].append('t')

        # Adiciona duração zero para os nós fictícios "s" e "t"
        duracao['s'] = 0
        duracao['t'] = 0

        caminhos_criticos, duracao_total = encontrar_caminhos_criticos(grafo, duracao)
        exibir_caminhos_criticos(caminhos_criticos, nomes, duracao_total)

if __name__ == "__main__":
    main()
