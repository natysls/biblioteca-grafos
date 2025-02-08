from collections import defaultdict
class Grafo:
    def __init__(self, direcionado=False, usar_matriz=False):
        self.direcionado = direcionado
        self.usar_matriz = usar_matriz
        self.vertices = set()
        self.pesos = {} if not usar_matriz else None
        self.lista_adjacencia = {} if not usar_matriz else None
        self.matriz_adjacencia = defaultdict(dict) if usar_matriz else None
        self.grau = defaultdict(int) # de cada vertice

    def adicionar_aresta(self, u, v, peso=1):
        self.vertices.update([u, v])

        if self.usar_matriz:
            self.matriz_adjacencia[u][v] = peso

            if not self.direcionado:
                self.matriz_adjacencia[v][u] = peso
                
        else:
            if u not in self.lista_adjacencia:
                self.lista_adjacencia[u] = []
            if v not in self.lista_adjacencia:
                self.lista_adjacencia[v] = []
            
            self.lista_adjacencia[u].append(v)
            self.pesos[(u, v)] = peso
            
            if not self.direcionado:
                self.lista_adjacencia[v].append(u)
                self.pesos[(v, u)] = peso

        self.grau[u] += 1
        self.grau[v] += 1 

    def n(self): # Quantidade de Vértices
        return len(self.vertices)
    
    def m(self): # Quantidade de Arestas
        if self.usar_matriz:
            # Somando todos os tamanhos da quantidade de vizinhos de cada iteração/pagina do dicionario
            total_arestas = sum(len(vizinhos) for vizinhos in self.matriz_adjacencia.values())
        else:
            total_arestas = len(self.pesos)
        
        # Divide por 2 por causa do grafo que possui duas areastas no mesmo arco
        return total_arestas if self.direcionado else (total_arestas // 2)

    def viz(self, v):  # Vizinhança do vértice v
        if self.usar_matriz:
            return list(self.matriz_adjacencia[v].keys())
        else:
            return self.lista_adjacencia.get(v, [])
        
    def d(self, v):  # Grau do vértice v
        return self.grau[v] # O(1)
            
    def w(self, u, v):  # Peso da aresta uv
        if self.usar_matriz:
            return self.matriz_adjacencia.get(u, {}).get(v, None)
        else:
            return self.pesos.get((u, v), None)
        
    def mind(self):  # Menor grau presente no grafo
        vertice_minimo = min(self.grau, key=self.grau.get)  
        grau_minimo = self.d(vertice_minimo)
        return vertice_minimo, grau_minimo 
    
    def maxd(self): # Vértice com o maior grau e o valor do maior grau no grafo
        vertice_maximo = max(self.grau, key=self.grau.get)  
        grau_maximo = self.d(vertice_maximo)
        return vertice_maximo, grau_maximo 

    def relaxamento(self, origem, destino, peso, d, pi):
        if d[destino] > d[origem] + peso:  
            d[destino] = d[origem] + peso
            pi[destino] = origem
    
    def bf(self, v): # Bellman-Ford
        """
        - d: distâncias mínimas de v para cada vértice (calculada iterativamente) (soma dos pesos)
        - pi: pai de cada vértice no caminho mínimo.
        """
        d = {vertice: float('inf') for vertice in self.vertices}
        pi = {vertice: None for vertice in self.vertices}
        
        d[v] = 0  # A distância do vértice de origem para ele mesmo é 0
        msg = "Tudo certo"

        for _ in range(len(self.vertices) - 1): # Relaxamento das arestas |V| - 1 vezes
            for u in self.vertices:
                for v in (self.lista_adjacencia[u] if not self.usar_matriz else self.matriz_adjacencia.get(u, {})):
                    peso = self.w(u, v)  
                    self.relaxamento(origem=u, destino=v, peso=peso, d=d, pi=pi)
                    
                    if not self.direcionado:
                        self.relaxamento(origem=v, destino=u, peso=peso, d=d, pi=pi)

        # Verificação de ciclos de peso negativo
        for u in self.vertices:
            for v in (self.lista_adjacencia[u] if not self.usar_matriz else self.matriz_adjacencia.get(u, {})):
                peso = self.w(u, v)
                if d[v] > d[u] + peso:
                    msg = "O grafo contém um ciclo de peso negativo!"

        return d, pi, msg

class Digrafo(Grafo):
    def __init__(self, usar_matriz=False):
        super().__init__(direcionado=True, usar_matriz=usar_matriz)