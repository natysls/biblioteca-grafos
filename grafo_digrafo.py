class Grafo:
    def __init__(self, direcionado=False, usar_matriz=False):
        self.direcionado = direcionado
        self.usar_matriz = usar_matriz
        self.vertices = set()
        self.arestas = []
        self.pesos = {} if not usar_matriz else None
        self.lista_adjacencia = {} if not usar_matriz else None
        self.matriz_adjacencia = [] if usar_matriz else None
    
    def adicionar_aresta(self, u, v, peso=1):
        self.vertices.update([u, v])
        self.arestas.append((u, v))
        
        if self.usar_matriz:
            max_index = max(u, v)
            while len(self.matriz_adjacencia) <= max_index:
                self.matriz_adjacencia.append([0] * (max_index + 1))
                for linha in self.matriz_adjacencia:
                    linha.extend([0] * (max_index + 1 - len(linha)))
            
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

    def n(self):
        return len(self.vertices)

    def m(self):
        if self.usar_matriz:
            return sum(row.count(1) for row in self.matriz) // (1 if self.direcionado else 2)
        return len(self.pesos) // (1 if self.direcionado else 2)



class Digrafo(Grafo):
    def __init__(self, usar_matriz=False):
        super().__init__(direcionado=True, usar_matriz=usar_matriz)