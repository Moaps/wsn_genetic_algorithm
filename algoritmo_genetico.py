import numpy as np
import random as rd
import math as mh
from problema import Problema

class AlgoritmoGenetico:
    def __init__(self, problema, tamanho_populacao, taxa_cruzamento, taxa_mutacao, num_geracoes):
        self.problema = problema
        self.tamanho_populacao = tamanho_populacao
        self.taxa_cruzamento = taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao
        self.num_geracoes = num_geracoes

    def gerar_cromossomo(self):
        """ Gera um cromossomo aleatório. """
        return np.random.permutation(self.problema.n_nos)

    def populacao_inicial(self):
        """ Gera a população inicial de cromossomos. """
        return np.array([self.gerar_cromossomo() for _ in range(self.tamanho_populacao)])

    def calcular_aptidao(self, populacao):
        """ Calcula a aptidão da população com base na matriz de energia. """
        aptidoes = np.zeros(self.tamanho_populacao)
        for i, individuo in enumerate(populacao):
            aptidoes[i] = self.problema.calcular_custo_total(individuo, self.problema.matriz_energia)
        return aptidoes / sum(aptidoes)

    def crossover(self, populacao, aptidoes):
        """ Realiza cruzamento entre indivíduos. """
        qtd_cruzamentos = mh.ceil(self.taxa_cruzamento * self.tamanho_populacao)
        descendentes = []
        for _ in range(qtd_cruzamentos):
            pai1, pai2 = self.selecionar_pais(aptidoes)
            ponto_corte = rd.randint(0, self.problema.n_nos)
            descendentes.append(np.concatenate((populacao[pai1][:ponto_corte], populacao[pai2][ponto_corte:])))
            descendentes.append(np.concatenate((populacao[pai2][:ponto_corte], populacao[pai1][ponto_corte:])))
        return descendentes

    def selecionar_pais(self, aptidoes):
        """ Seleciona dois pais para cruzamento. """
        roleta = np.cumsum(aptidoes)
        aleatorio1 = rd.random()
        aleatorio2 = rd.random()
        p1 = np.where(roleta >= aleatorio1)[0][0]
        p2 = np.where(roleta >= aleatorio2)[0][0]
        return p1, p2

    def mutacao(self, descendentes):
        """ Realiza mutação em descendentes. """
        qtd_mutacoes = mh.ceil(self.taxa_mutacao * len(descendentes))
        for _ in range(qtd_mutacoes):
            idx_descendente = rd.randint(0, len(descendentes) - 1)
            idx1, idx2 = rd.sample(range(self.problema.n_nos), 2)
            descendentes[idx_descendente][idx1], descendentes[idx_descendente][idx2] = descendentes[idx_descendente][idx2], descendentes[idx_descendente][idx1]
        return descendentes

    def executar(self):
        """ Executa o algoritmo genético. """
        populacao = self.populacao_inicial()
        aptidoes = self.calcular_aptidao(populacao)

        for _ in range(self.num_geracoes):
            descendentes = self.crossover(populacao, aptidoes)
            descendentes = self.mutacao(descendentes)
            populacao = self.nova_populacao(populacao, descendentes)
            aptidoes = self.calcular_aptidao(populacao)

        return self.selecionar_melhor(populacao, aptidoes)

    def nova_populacao(self, populacao, descendentes):
        """ Substitui a população pelos descendentes. """
        elite = int(self.tamanho_populacao * 0.1)
        nova_populacao = populacao[:elite]
        nova_populacao = np.concatenate((nova_populacao, descendentes[:self.tamanho_populacao - elite]))
        return nova_populacao

    def selecionar_melhor(self, populacao, aptidoes):
        """ Retorna o melhor indivíduo da população. """
        idx_melhor = np.argmax(aptidoes)
        return populacao[idx_melhor]
