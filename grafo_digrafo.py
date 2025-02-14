from collections import defaultdict, deque
class Grafo:
    def __init__(self, direcionado=False, usar_matriz=False):
        self.direcionado = direcionado
        self.usar_matriz = usar_matriz
        self.vertices = set()
        self.pesos = {} if not usar_matriz else None
        self.lista_adjacencia = defaultdict(dict) if not usar_matriz else None
        self.matriz_adjacencia = defaultdict(dict) if usar_matriz else None

    def adicionar_aresta(self, u, v, peso=1):
        self.vertices.update([u, v])

        if self.usar_matriz:
            self.matriz_adjacencia[u][v] = peso

            if not self.direcionado:
                self.matriz_adjacencia[v][u] = peso
                
        else:
            # Verifica se já existe a aresta para evitar contagem repetida no grau
            if v not in self.lista_adjacencia[u]:
                self.lista_adjacencia[u][v] = peso  # Tentando melhorar o desempenho do bf

            if not self.direcionado and u not in self.lista_adjacencia[v]:
                self.lista_adjacencia[v][u] = peso

    def n(self): # Quantidade de Vértices
        return len(self.vertices)
    
    def m(self): # Quantidade de Arestas
        if self.usar_matriz:
            # Somando todos os tamanhos da quantidade de vizinhos de cada iteração/pagina do dicionario
            total_arestas = sum(len(vizinhos) for vizinhos in self.matriz_adjacencia.values())
        else:
            total_arestas =  sum(len(vizinhos) for vizinhos in self.lista_adjacencia.values())
        
        # Divide por 2 por causa do grafo que possui duas areastas no mesmo arco
        return total_arestas if self.direcionado else (total_arestas // 2)

    def viz(self, v):  # Vizinhança do vértice v
        if self.usar_matriz:
            return list(self.matriz_adjacencia[v].keys())
        else:
            return list(self.lista_adjacencia[v].keys())
        
    def d(self, v):  # Grau do vértice v
        if self.usar_matriz:
            return len(self.matriz_adjacencia[v].keys())
        else:
            return len(self.lista_adjacencia[v].keys())
            
    def w(self, u, v):  # Peso da aresta uv
        if self.usar_matriz:
            return self.matriz_adjacencia.get(u, {}).get(v, None)
        else:
            return self.lista_adjacencia.get(u, {}).get(v, None) 
        
    def mind(self):  # Menor grau presente no grafo
        vertice_minimo = min(self.vertices, key=self.d)  
        grau_minimo = self.d(vertice_minimo)
        return vertice_minimo, grau_minimo 
    
    def maxd(self): # Vértice com o maior grau e o valor do maior grau no grafo
        vertice_maximo = max(self.vertices, key=self.d)   
        grau_maximo = self.d(vertice_maximo)
        return vertice_maximo, grau_maximo 

    def bfs(self, v):
        d = defaultdict(lambda: -1)  # -1 = vértice não foi visitado
        pi = {}
        '''''
        d = [-1] * (self.n() + 1) 
        pi = [None] * (self.n() + 1)
        '''
        d[v] = 0
        fila = deque([v])

        caminhos = {v: [v]} 

        while fila:
            vertice_atual = fila.popleft()
            for atual in self.viz(v=vertice_atual): 
                #peso = self.w(u=vertice_atual, v=atual)  
                if d[atual] == -1:  
                    d[atual] = d[vertice_atual] + 1 # 1 = peso uniforme  
                    pi[atual] = vertice_atual 
                    caminhos[atual] = caminhos[vertice_atual] + [atual]
                    fila.append(atual) 
                    #print(f"Aresta visitada: ({vertice_atual}, {atual}) com peso {peso}")
        
        caminho_maior_10_arestas = next((caminho for caminho in caminhos.values() if len(caminho) >= 11), None)

        return d, pi, caminho_maior_10_arestas
    
    def vertices_alcancaveis(self, v): 
        """"
        Pré-procesamento dos dados para o BF
        Evita percorrer vértices que nunca serão atualizados.
        Filtra apenas os vértices alcançáveis
        """
        distancias, _, _ = self.bfs(v)
        return {u for u, d in distancias.items() if d != -1} 

    def relaxamento(self, origem, destino, peso, d, pi, fila, na_fila):
        if d[destino] > d[origem] + peso:  
            d[destino] = d[origem] + peso
            pi[destino] = origem

            if destino not in na_fila:
                fila.append(destino)
                na_fila.add(destino)

    def bf(self, v): # Bellman-Ford
        """
        Será preciso um pré-processamento dos dados para otimizar o tempo
        - d: distâncias mínimas de v para cada vértice (calculada iterativamente) (soma dos pesos)
        - pi: pai de cada vértice no caminho mínimo.
        Pior caso: |V| - 1 iterações complexidade O(V * E) não processa alto volume de vertices
        Melhor caso: Fila O(E)
        """
        # PRÉ-PROCESSAMENTO
        alcancaveis = self.vertices_alcancaveis(v)

        d = {vertice: float('inf') for vertice in alcancaveis}
        pi = {vertice: None for vertice in alcancaveis}
        
        d[v] = 0  # A distância do vértice de origem para ele mesmo é 0
        msg = "Tudo certo"

        # Processando grande volume de vértices (somente vértices que realmente mudaram na última iteração)
        fila = deque([v])
        na_fila = {v}  # Vértices que estão na fila

        while fila:
            u = fila.popleft()
            na_fila.remove(u)  # Pois agora será processado

            vizinhos = self.viz(u)
            for v in vizinhos:
                if v not in alcancaveis:
                    continue

                peso = self.w(u, v)  
                self.relaxamento(origem=u, destino=v, peso=peso, d=d, pi=pi, fila=fila, na_fila=na_fila)

        # Verificação de ciclos de peso negativo
        for u in alcancaveis:
            for v in (self.lista_adjacencia[u] if not self.usar_matriz else self.matriz_adjacencia.get(u, {})):
                if v in alcancaveis:  # Só verifica ciclos em vértices alcançáveis
                    peso = self.w(u, v)
                    if d[v] > d[u] + peso:
                        msg = "O grafo contém um ciclo de peso negativo!"

        return d, pi, msg

class Digrafo(Grafo):
    def __init__(self, usar_matriz=False):
        super().__init__(direcionado=True, usar_matriz=usar_matriz)