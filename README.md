# Cálculo do Caminho Crítico

## 1. Introdução

Este projeto tem como objetivo resolver o problema do cálculo do caminho crítico em um grafo que representa dependências entre disciplinas de um curso. O caminho crítico é a sequência de disciplinas que determina o tempo mínimo necessário para completar o curso, considerando as durações e dependências entre as disciplinas. O programa é capaz de ler um arquivo CSV contendo informações sobre as disciplinas, como código, nome, duração e dependências, e calcular o caminho crítico, exibindo o resultado ao usuário.

### Visão Geral do Funcionamento

O programa é estruturado em várias funções principais:

- **Carregar o Grafo**: Lê o arquivo CSV e constrói um grafo que representa as disciplinas e suas dependências.
- **Encontrar o Caminho Crítico**: Utiliza um algoritmo de ordenação topológica e relaxamento de arestas para calcular o caminho crítico no grafo.
- **Exibir o Caminho Crítico**: Formata e exibe o caminho crítico e o tempo mínimo total ao usuário.

## 2. Implementação

### Estruturas de Dados Utilizadas

1. **Grafo**: Representado como um dicionário onde cada chave é um nó (disciplina) e cada valor é uma lista de adjacências (disciplinas que dependem da chave).
   - Exemplo:
     ```python
     grafo = {
         'A': ['B', 'C'],
         'B': ['D'],
         'C': ['D'],
         'D': []
     }
     ```

2. **Duração**: Dicionário que armazena a duração de cada disciplina, usando o código da disciplina como chave.
   - Exemplo:
     ```python
     duracao = {
         'A': 3,
         'B': 2,
         'C': 1,
         'D': 4
     }
     ```

3. **Nomes**: Dicionário que armazena os nomes das disciplinas, usando o código da disciplina como chave.
   - Exemplo:
     ```python
     nomes = {
         'A': 'Disciplina A',
         'B': 'Disciplina B',
         'C': 'Disciplina C',
         'D': 'Disciplina D'
     }
     ```

### Funcionamento das Principais Funções

- **`carregar_grafo(arquivo)`**: Lê um arquivo CSV e constrói o grafo, as durações e os nomes das disciplinas.
  
- **`encontrar_caminho_critico(grafo, duracao)`**: Implementa o algoritmo de ordenação topológica para calcular o caminho crítico e a duração total. A função realiza o seguinte:
  - Inicializa as distâncias com -∞, exceto para o nó inicial 's', que é 0.
  - Realiza a ordenação topológica dos nós.
  - Relaxa as arestas do grafo conforme a ordem topológica para atualizar as distâncias.
  
- **`exibir_caminho_critico(caminho_critico, nomes, duracao_total)`**: Formata e exibe o caminho crítico e o tempo total.

### Formato de Entrada e Saída de Dados

- **Entrada**: Arquivo CSV no seguinte formato:

    Código,Nome,Período,Duração,Dependências A,Disciplina A,1,3,B,C B,Disciplina B,2,2,D C,Disciplina C,1,1, D,Disciplina D,3,4,


- **Saída**: Exibe o caminho crítico e o tempo mínimo no console:
Caminho Crítico:

    Disciplina A

    Disciplina B

    Disciplina D
    
    Tempo Mínimo: 9


### Decisões Tomadas

- A escolha de usar um grafo orientado é crucial, já que as disciplinas têm dependências diretas.
- A utilização de um dicionário para representar as durações e nomes das disciplinas facilita o acesso e manipulação dos dados.

## 3. Listagem de Testes Executados

### Teste 1: Arquivo Válido
- **Entrada**: Um arquivo CSV corretamente formatado.
- **Resultado Esperado**: O caminho crítico e o tempo total devem ser exibidos corretamente.
- **Resultado Obtido**: Corretamente exibido.

### Teste 2: Arquivo Vazio
- **Entrada**: Um arquivo CSV vazio.
- **Resultado Esperado**: Mensagem de erro ao tentar processar um arquivo vazio.
- **Resultado Obtido**: Mensagem de erro foi gerada corretamente.

### Teste 3: Dependências Cíclicas
- **Entrada**: Um arquivo com dependências que formam um ciclo.
- **Resultado Esperado**: Mensagem de erro sobre a presença de um ciclo.
- **Resultado Obtido**: Mensagem de erro foi gerada corretamente.

### Teste 4: Disciplina Sem Dependências
- **Entrada**: Um arquivo onde algumas disciplinas não têm dependências.
- **Resultado Esperado**: O caminho crítico deve incluir essas disciplinas como pontos de partida.
- **Resultado Obtido**: O resultado foi exibido corretamente.

## 4. Conclusão

O projeto foi bem-sucedido em calcular o caminho crítico a partir de um conjunto de disciplinas e suas dependências. Durante a implementação, algumas dificuldades foram encontradas, principalmente relacionadas à manipulação do grafo e à ordenação topológica. A abordagem adotada provou ser eficaz, e os testes realizados demonstraram a robustez do programa.

## 5. Bibliografia

1. Cormen, Thomas H., et al. *Introduction to Algorithms*. MIT Press, 2009.
2. Knuth, Donald E. *The Art of Computer Programming, Volume 1: Fundamental Algorithms*. Addison-Wesley, 1997.
3. Sítio da Internet: [GeeksforGeeks](https://www.geeksforgeeks.org/) - Utilizado para referência sobre algoritmos de grafos e ordenação topológica.
