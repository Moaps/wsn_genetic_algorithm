import numpy as np

class Problema:
    def __init__(self, n_nos, dist_min, dist_max, energia_min, energia_max, custo_min, custo_max):
        self.n_nos = n_nos
        self.matriz_distancia, self.matriz_energia, self.matriz_comunicacao = self.gerar_matrizes(dist_min, dist_max, energia_min, energia_max, custo_min, custo_max)

    def gerar_matrizes(self, dist_min, dist_max, energia_min, energia_max, custo_min, custo_max):
        """
        Gera as matrizes de distância, consumo de energia e custo de comunicação.
        """
        print(dist_min, dist_max, energia_min, energia_max, custo_min, custo_max)
        matriz_distancia = np.random.randint(dist_min, dist_max, (self.n_nos, self.n_nos))
        matriz_energia = np.random.randint(energia_min, energia_max, (self.n_nos, self.n_nos))
        matriz_comunicacao = np.random.randint(custo_min, custo_max, (self.n_nos, self.n_nos))
        return matriz_distancia, matriz_energia, matriz_comunicacao

    def calcular_custo_total(self, caminho, matriz):
        """
        Calcula o custo total do caminho fornecido usando a matriz especificada.
        """
        custo_total = 0
        for i in range(len(caminho) - 1):
            custo_total += matriz[caminho[i]][caminho[i + 1]]
        custo_total += matriz[caminho[-1]][caminho[0]]  # Volta ao nó inicial
        return custo_total
