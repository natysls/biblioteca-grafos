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
    def salvar_resultado_bf(distancias, predecessores, nome_arquivo="resultado_bf.txt"):
        with open(nome_arquivo, "w") as f:  # Remove "/mnt/data/"
            f.write("v\td\tpi\n")
            for vertice, distancia in distancias.items():
                predecessor = predecessores.get(vertice, "None")
                f.write(f"{vertice}\t{distancia}\t{predecessor}\n")
        print(f"Arquivo salvo como {nome_arquivo}")
    
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

        print("")
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
        
        distancias, predecessores, caminho_maior_10_areastas = grafo.bfs(v=56)
        vertice_max = max(distancias, key=distancias.get)
        predecessor_max = predecessores[vertice_max]
        print(f"h) BFS: O vértice de maior distância até 56 é {vertice_max} com o seguinte predecessor {predecessor_max}")
        print(f"c2) Um caminho com uma qtde. de arestas maior ou igual a 10 com BFS: {caminho_maior_10_areastas}")

        pi_dfs, v_ini, v_fim,  caminho_maior_10_areastas_dfs= grafo.dfs(v=56)
        if pi_dfs.get(56, 'Não possui predecessor') == 'Não possui predecessor':
            print(f"i) DFS: Vértice 56 não possui predecessor")
        else:
            print(f"i) DFS: Vértice 56 com o seguinte predecessor: {pi_dfs.get(56, 'Não possui predecessor')}")
        print(f"  - Tempo de início: {v_ini[57]}")
        print(f"  - Tempo de término: {v_fim[57]}")
        print(f"  - Diferença: {v_fim[57] - v_ini[57]}")
        if (v_fim[57] - v_ini[57]) == 1:
            print("    -> Este vértice é uma folha na árvore de busca (não tem descendentes).")
        else:
            print(f"    -> Este vértice tem {(v_fim[57] - v_ini[57]) - 1} unidades de tempo gastas explorando seus descendentes.")
        print(f"c2) Um caminho com uma qtde. de arestas maior ou igual a 10 com DFS: {caminho_maior_10_areastas_dfs}")
        print("")

        print("")
        print("Espere uns 2 minutinhos para execução do Bellman-Ford iniciando pelo vertice 1, será baixado um .txt...")
        d, pi, msg = grafo.bf(1)
        mais_distante = max(d, key=d.get)
        print("j) Bellman-Ford")
        # Gerando o arquivo
        Main.salvar_resultado_bf(d, pi, "resultado_bf_1.txt")
        print(msg)
        print(f"e2) Vértice mais distante de 1: {mais_distante}, Distância: {d[mais_distante]}")

        print("")
        print("Espere mais uns 3 minutinhos para execução do Bellman-Ford para encontrar o vértice mais distante do vértice 129...")
        d2, _, _ = grafo.bf(129)
        mais_distante2 = max(d2, key=d2.get)
        print(f"e2) Vértice mais distante de 129: {mais_distante2}, Distância: {d2[mais_distante2]}")
        print("")

        print("")
        distancia_minima_djikstra, predecessor_djikstra = grafo.djikstra(1)
        mais_distante_djikstra = max(distancia_minima_djikstra, key=distancia_minima_djikstra.get)
        print("k) Djikstra")
        Main.salvar_resultado_bf(distancia_minima_djikstra, predecessor_djikstra, "resultado_djikstra_1.txt")
        print(f"e2) Vértice mais distante de 1: {mais_distante_djikstra}, Distância: {distancia_minima_djikstra[mais_distante_djikstra]}, Predecessor: {predecessor_djikstra[mais_distante_djikstra]}")

        print("")
        distancia_minima_djikstra_129, _ = grafo.djikstra(129)
        mais_distante_djikstra_129= max(distancia_minima_djikstra_129, key=distancia_minima_djikstra_129.get)
        print(f"e2) Vértice mais distante de 129: {mais_distante_djikstra_129}, Distância: {distancia_minima_djikstra_129[mais_distante_djikstra_129]}")
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