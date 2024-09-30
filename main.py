import csv
from collections import defaultdict, deque

# Função para ler o arquivo CSV e construir o grafo
def carregar_grafo(arquivo):
    grafo = defaultdict(list)  #armazenar as dependências entre disciplinas
    duracao = {}  #duração de cada disciplina
    nomes = {}  #nomes das disciplinas

    # Abre o arquivo CSV e lê os dados
    with open(arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            codigo = row['Código']
            nome = row['Nome']
            periodo = int(row['Período'])  #período da disciplina 
            dur = int(row['Duração'])  #duração da disciplina
            dependencias = row['Dependências'].split(';') if row['Dependências'] else []  #dependências
            duracao[codigo] = dur #duração
            nomes[codigo] = nome  #nome

            # Constrói o grafo com base nas dependências
            for dep in dependencias:
                grafo[dep].append(codigo)

    return grafo, duracao, nomes  #Retorna o grafo, as durações e os nomes

# Algoritmo para encontrar os caminhos críticos
def encontrar_caminhos_criticos(grafo, duracao):
    distancias = defaultdict(lambda: -float('inf'))  # Inicializa todas as distâncias com menos infinito
    distancias['s'] = 0  # Define a distância inicial do nó fictício s para 0
    predecessores = defaultdict(list)  # Armazena predecessores para reconstrução dos caminhos

    # Função interna para realizar a ordenação topológica
    def ordenacao_topologica(grafo):
        grau_entrada = defaultdict(int)  #Conta o grau de entrada de cada nó
        for u in grafo:
            for v in grafo[u]:
                grau_entrada[v] += 1  #Incrementa o grau 

        # Inicializa a fila com os nós sem dependências
        fila = deque([u for u in grafo if grau_entrada[u] == 0])
        ordem = []  #Lista que armazenará a ordem topológica
        while fila:
            u = fila.popleft()  # Remove o primeiro nó da fila
            ordem.append(u)  # Adiciona à ordem topológica
            for v in grafo[u]:
                grau_entrada[v] -= 1  # Reduz o grau de entrada
                if grau_entrada[v] == 0:
                    fila.append(v)  # Adiciona à fila se não tiver mais dependências

        return ordem  # Retorna a ordem topológica

    # Ordenação topológica para processar o grafo
    ordem = ordenacao_topologica(grafo)

    # Atualiza as arestas na ordem topológica
    for u in ordem:
        for v in grafo[u]:
            # Atualiza a distância máxima de cada nó
            if distancias[v] < distancias[u] + duracao.get(u, 0):
                distancias[v] = distancias[u] + duracao.get(u, 0)
                predecessores[v] = [u]  # Substitui a lista de predecessores
            elif distancias[v] == distancias[u] + duracao.get(u, 0):
                predecessores[v].append(u)  # Adiciona um novo predecessor em caso de empate

    # Lista para armazenar os caminhos críticos
    caminhos_criticos = []
    max_distancia = distancias['t']  # Armazena a maior distância até 't'

    # Função recursiva para encontrar os caminhos críticos
    def encontrar_caminho(atual, caminho):
        if atual == 's':  # Se chegar ao nó fictício 's'
            caminhos_criticos.append(caminho[::-1])  # Adiciona o caminho invertido
            return
        for pred in predecessores[atual]: 
            encontrar_caminho(pred, caminho + [pred])  # Continua construindo o caminho para cada predecessor

    encontrar_caminho('t', ['t']) #Busca pelo caminho crítico

    return caminhos_criticos, max_distancia  # Retorna os caminhos críticos e a distância máxima

# Função para exibir os caminhos críticos
def exibir_caminhos_criticos(caminhos_criticos, nomes, duracao_total):
    print("Caminhos Críticos:")
    for caminho in caminhos_criticos:
        for codigo in caminho[1:-1]:  # Ignora os nós fictícios 's' e 't'
            print(f"- {nomes[codigo]}")  # Exibe o nome das disciplinas no caminho
        print() 
    print(f"Tempo Mínimo: {duracao_total}")  # Exibe a duração total do caminho crítico

# Função principal de interação com o usuário
def main():
    while True:
        arquivo = input("Informe o arquivo (0 para sair): ")
        if arquivo == "0":
            break 

        print("\nProcessando...")
        grafo, duracao, nomes = carregar_grafo(arquivo)  # Carrega o grafo a partir do arquivo CSV

        #Adiciona nós s e t para conectar o início e fim
        grafo['s'] = []  
        grafo['t'] = []  

        for codigo in nomes:
            # Se o código não for dependência de nenhum outro conecta a 's'
            if all(codigo not in grafo[dep] for dep in grafo):
                grafo['s'].append(codigo)
            # Se o código não tiver dependências conecta a 't'
            if not grafo[codigo]:
                grafo[codigo].append('t')

        # Define a duração zero para os nós s e t
        duracao['s'] = 0
        duracao['t'] = 0

        # Encontra os caminhos críticos e exibe o resultado
        caminhos_criticos, duracao_total = encontrar_caminhos_criticos(grafo, duracao)
        exibir_caminhos_criticos(caminhos_criticos, nomes, duracao_total)

if __name__ == "__main__":
    main()
