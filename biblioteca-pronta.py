import networkx as nx

class Main:
    @staticmethod
    def abrir_arquivo(filename, usar_matriz, usar_digrafo):
        # Criação do grafo baseado em se é direcionado ou não
        if usar_digrafo:
            grafo = nx.DiGraph()  # Grafo direcionado
        else:
            grafo = nx.Graph()  # Grafo não direcionado

        # Leitura do arquivo e adição de arestas
        with open(filename, 'r') as f:
            lines = f.readlines()
            num_vertices, num_arcos = map(int, lines[4].split()[2:4])  # Linha 5 contém os valores
            
            for line in lines[7:]:
                parts = line.split()
                if parts[0] == 'a':
                    u, v, p = map(int, parts[1:])
                    grafo.add_edge(u, v, weight=p)
        return grafo
    
    @staticmethod
    def salvar_resultado_bf(distancias, predecessores, nome_arquivo="resultado_bf.txt"):
        with open(nome_arquivo, "w") as f:
            f.write("v\td\tpi\n")
            for vertice, distancia in distancias.items():
                predecessor = predecessores.get(vertice, "None")
                f.write(f"{vertice}\t{distancia}\t{predecessor}\n")
        print(f"Arquivo salvo como {nome_arquivo}")
    
    @staticmethod
    def exemplo_facil(usar_matriz, usar_diagrafo):
        if usar_diagrafo:
            g = nx.DiGraph()  # Grafo direcionado
        else:
            g = nx.Graph()  # Grafo não direcionado

        g.add_edge(0, 1, weight=6)
        g.add_edge(0, 2, weight=7)
        g.add_edge(1, 3, weight=5)
        g.add_edge(1, 2, weight=8)
        g.add_edge(1, 4, weight=-4)
        g.add_edge(2, 3, weight=-3)
        g.add_edge(2, 4, weight=9)
        g.add_edge(3, 1, weight=-2)
        g.add_edge(4, 3, weight=7)
        return g
    
    @staticmethod
    def mostrar_resultados(usar_matriz, usar_digrafo, teste):
        arquivo = "USA-road-d.NY.gr"
        grafo = Main.abrir_arquivo(arquivo, usar_matriz, usar_digrafo)
        # grafo = Main.exemplo_facil(usar_matriz, usar_digrafo)

        print("")
        print(teste)
        print(f"a) Número de vértices: {grafo.number_of_nodes()}")
        print(f"b) Número de arestas: {grafo.number_of_edges()}")
        print(f"c) Vizinhança do vértice 56: {list(grafo.neighbors(56))}")
        print(f"d) Grau do vértice 56: {grafo.degree(56)}")
        print(f"e) Peso da aresta (55, 56): {grafo.get_edge_data(55, 56, {}).get('weight', 'Não existe')}")
        print(f"f) O vértice de menor grau é {min(grafo.degree, key=lambda x: x[1])}")
        print(f"g) O vértice de maior grau é {max(grafo.degree, key=lambda x: x[1])}")
        
        # Executando BFS
        distancias, predecessores = nx.single_source_shortest_path_length(grafo, 56), nx.single_source_shortest_path(grafo, 56)
        vertice_max = max(distancias, key=distancias.get)
        predecessor_max = predecessores.get(vertice_max, "Não encontrado")
        print(f"h) BFS: O vértice de maior distância até 56 é {vertice_max} com o seguinte predecessor {predecessor_max}")
        
        # Executando Bellman-Ford
        print("Espere uns 2 minutinhos para execução do Bellman-Ford iniciando pelo vertice 1, será baixado um .txt...")
        try:
            distancias_bf, predecessores_bf = nx.single_source_bellman_ford(grafo, 1)
            mais_distante = max(distancias_bf, key=distancias_bf.get)
            print("j) Bellman-Ford")
            Main.salvar_resultado_bf(distancias_bf, predecessores_bf)
            print(f"e2) Vértice mais distante de 1: {mais_distante}, Distância: {distancias_bf[mais_distante]}")
        except nx.NetworkXUnbounded:
            print("Erro no Bellman-Ford: O grafo contém ciclos negativos.")
        
        print("")

        # Executando Bellman-Ford a partir do vértice 129
        print("Espere mais uns 3 minutinhos para execução do Bellman-Ford para encontrar o vértice mais distante do vértice 129...")
        try:
            distancias_bf, predecessores_bf = nx.single_source_bellman_ford(grafo, 129)
            mais_distante = max(distancias_bf, key=distancias_bf.get)
            print("j) Bellman-Ford")
            Main.salvar_resultado_bf(distancias_bf, predecessores_bf)
            print(f"e2) Vértice mais distante de 129: {mais_distante}, Distância: {distancias_bf[mais_distante]}")
        except nx.NetworkXUnbounded:
            print("Erro no Bellman-Ford: O grafo contém ciclos negativos.")

        print("")
    
    @staticmethod
    def escolher_teste():
        print("Escolha um teste para rodar:")
        print("1 - Teste 1: Digrafo com Lista de Adjacencia")
        print("2 - Teste 2: Grafo com Lista de Adjacencia")
        print("3 - Teste 3: Digrafo com Matriz de Adjacencia")
        print("4 - Teste 4: Grafo com Matriz de Adjacencia")

        escolha = input("Digite o número do teste que deseja rodar (1-4): ")

        if escolha == '1':
            Main.mostrar_resultados(usar_matriz=False, usar_digrafo=True, teste='Teste 1: Digrafo com Lista de Adjacencia')
        elif escolha == '2':
            Main.mostrar_resultados(usar_matriz=False, usar_digrafo=False, teste='Teste 2: Grafo com Lista de Adjacencia')
        elif escolha == '3':
            Main.mostrar_resultados(usar_matriz=True, usar_digrafo=True, teste='Teste 3: Digrafo com Matriz de Adjacencia')
        elif escolha == '4':
            Main.mostrar_resultados(usar_matriz=True, usar_digrafo=False, teste='Teste 4: Grafo com Matriz de Adjacencia')
        else:
            print("Opção inválida! Por favor, escolha um número de 1 a 4.")

Main.escolher_teste()
