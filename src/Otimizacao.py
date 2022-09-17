from Individuo import Individuo
from individuo_vars import *

from copy import deepcopy


class Otimizacao():

    def __init__(self,qnt_individuos,taxa_de_mutacao):
            
            self.qnt_individuos = qnt_individuos
            self.taxa_de_mutacao = taxa_de_mutacao
            
            self.populacao = self.cria_populacao()

    
    def cria_populacao(self):
        populacao = []
        for i in range(self.qnt_individuos):
            populacao.append(Individuo(etapas=etapas,hobbits=deepcopy(hobbits)))
        return populacao

if __name__ == '__main__':
    Otimizacao=Otimizacao(qnt_individuos=20, taxa_de_mutacao=1/16)
    print("Terminei")
