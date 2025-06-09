import numpy as np
import matplotlib.pyplot as plt
from otimizacao_discreto import SimulatedAnnealing


def f(cidades, caminho):
    s = 0
    for i in range(len(caminho)):
        p1 = cidades[caminho[i], :]
        p2 = cidades[caminho[(i + 1) % len(caminho)], :]
        s += np.linalg.norm(p1 - p2)
    return s


N = 20 

cidades = np.random.randint(0, 100, size=(N, 2))

origem = np.array([
    [50, 50]
])

max_iteracoes = 2000
temperatura_inicial = 1000
num_trocas = 1
taxa_resfriamento = 0.995

sa = SimulatedAnnealing(max_iteracoes, f, cidades, origem, temperatura_inicial, num_trocas, taxa_resfriamento)

sa.busca()

bp = 1