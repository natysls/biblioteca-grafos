from grafo_digrafo import Grafo, Digrafo

class Main:
    @staticmethod
    def abrir_arquivo(filename, usar_matriz, usar_diagrafo):
        if(usar_diagrafo):
            grafo = Digrafo(usar_matriz=usar_matriz)
        else:
            grafo = Grafo(usar_matriz=usar_matriz)

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
    def mostrar_resultados(usar_matriz, usar_digrafo, teste):
        arquivo = "USA-road-d.NY.gr"
        grafo = Main.abrir_arquivo(arquivo, usar_matriz, usar_digrafo)
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
        print("")


# Teste 1: Digrafo com Lista de Adjacencia
Main.mostrar_resultados(usar_matriz=False, usar_digrafo=True, teste='Teste 1: Digrafo com Lista de Adjacencia')

# Teste 2: Grafo com Lista de Adjacencia
Main.mostrar_resultados(usar_matriz=False, usar_digrafo=False, teste='Teste 2: Grafo com Lista de Adjacencia')

# Teste 3: Digrafo com Matriz de Adjacencia
Main.mostrar_resultados(usar_matriz=True, usar_digrafo=True, teste='Teste 3: Digrafo com Matriz de Adjacencia')

# Teste 4: Grafo com Matriz de Adjacencia
Main.mostrar_resultados(usar_matriz=True, usar_digrafo=False, teste='Teste 4: Grafo com Matriz de Adjacencia')