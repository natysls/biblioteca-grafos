from grafo_digrafo import Grafo, Digrafo

class Main:
    @staticmethod
    def abrir_arquivo(filename, usar_matriz, usar_diagrafo):
        if(usar_diagrafo):
            grafo = Digrafo(usar_matriz)
        else:
            grafo = Grafo(usar_matriz)

        with open(filename, 'r') as f:
            lines = f.readlines()
            num_vertices, num_arcos = map(int, lines[4].split()[2:4])  # Linha 5 contém os valores
            
            for line in lines[7:]:
                parts = line.split()
                if parts[0] == 'a':
                    u, v, p = map(int, parts[1:])
                    grafo.adicionar_aresta(u, v, p)
        return grafo
    
    @staticmethod
    def exemplo_facil(usar_matriz, usar_diagrafo):
        if(usar_diagrafo):
            g = Digrafo(usar_matriz)
        else:
            g = Grafo(usar_matriz)

        g.adicionar_aresta(0, 1, 6)
        g.adicionar_aresta(0, 2, 7)
        g.adicionar_aresta(1, 3, 5)
        g.adicionar_aresta(1, 2, 8)
        g.adicionar_aresta(1, 4, -4)
        g.adicionar_aresta(2, 3, -3)
        g.adicionar_aresta(2, 4, 9)
        g.adicionar_aresta(3, 1, -2)
        g.adicionar_aresta(4, 3, 7)
        return g
    
    @staticmethod
    def mostrar_resultados(usar_matriz, usar_digrafo, teste):
        arquivo = "USA-road-d.NY.gr"
        grafo = Main.abrir_arquivo(arquivo, usar_matriz, usar_digrafo)
        #grafo = Main.exemplo_facil(usar_matriz, usar_digrafo)

        print(teste)
        print(f"a) Número de vértices: {grafo.n()}")
        print(f"b) Número de arestas: {grafo.m()}")
        print(f"c) Vizinhança do vértice 56: {grafo.viz(56)}")
        print(f"d) Grau do vértice 56: {grafo.d(56)}")
        print(F"e) Peso da aresta (55, 56): {grafo.w(u=55, v=56)}")
        print(F"e) Peso da aresta (2, 4): {grafo.w(u=2, v=4)}")
        v1, grau1 = grafo.mind()
        print(F"f) O vértice de menor grau é {v1} com grau {grau1}")
        v2, grau2 = grafo.maxd()
        print(F"g) O vértice de maior grau é {v2} com grau {grau2}")
        
        distancias, predecessores = grafo.bfs(v=56)
        vertice_max = max(distancias, key=distancias.get)
        predecessor_max = predecessores[vertice_max]
        print(f"h) BFS: O vértice de maior distância até 56 é {vertice_max} com o seguinte predecessor {predecessor_max}")
        
        d, pi, msg = grafo.bf(1)
        print("j) Bellman-Ford")
        print("Distâncias mínimas:", d)
        print("Pais:", pi)
        print(msg)
        print("")


# Teste 1: Digrafo com Lista de Adjacencia
Main.mostrar_resultados(usar_matriz=False, usar_digrafo=True, teste='Teste 1: Digrafo com Lista de Adjacencia')

# Teste 2: Grafo com Lista de Adjacencia
#Main.mostrar_resultados(usar_matriz=False, usar_digrafo=False, teste='Teste 2: Grafo com Lista de Adjacencia')

# Teste 3: Digrafo com Matriz de Adjacencia
#Main.mostrar_resultados(usar_matriz=True, usar_digrafo=True, teste='Teste 3: Digrafo com Matriz de Adjacencia')

# Teste 4: Grafo com Matriz de Adjacencia
#Main.mostrar_resultados(usar_matriz=True, usar_digrafo=False, teste='Teste 4: Grafo com Matriz de Adjacencia')