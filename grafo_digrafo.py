from collections import defaultdict
class Grafo:
    def __init__(self, direcionado=False, usar_matriz=False):
        self.direcionado = direcionado
        self.usar_matriz = usar_matriz
        self.vertices = set()
        self.pesos = {} if not usar_matriz else None
        self.lista_adjacencia = {} if not usar_matriz else None
        self.matriz_adjacencia = defaultdict(dict) if usar_matriz else None
    
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

    def n(self): # Vértices
        return len(self.vertices)
    
    def m(self): # Arestas
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
        if self.direcionado:
            if self.usar_matriz:
                # Grau de entrada + grau de saída em um grafo direcionado
                grau_saida = len(self.matriz_adjacencia[v])
                grau_entrada = sum(1 for u in self.matriz_adjacencia if v in self.matriz_adjacencia[u])
                return grau_saida, grau_entrada 
            else:
                grau_saida = len(self.lista_adjacencia.get(v, []))
                grau_entrada = sum(1 for u in self.lista_adjacencia if v in self.lista_adjacencia[u])
                return grau_saida, grau_entrada
        else:
            if self.usar_matriz:
                return len(self.matriz_adjacencia[v])
            else:
                return len(self.lista_adjacencia.get(v, []))
            
    def w(self, u, v):  # Peso da aresta uv
        if self.usar_matriz:
            return self.matriz_adjacencia.get(u, {}).get(v, None)
        else:
            return self.pesos.get((u, v), None)


class Digrafo(Grafo):
    def __init__(self, usar_matriz=False):
        super().__init__(direcionado=True, usar_matriz=usar_matriz)