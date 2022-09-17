from Individuo import Individuo
from individuo_vars import *

import random

from copy import deepcopy


class Otimizacao():

    def __init__(self,qnt_individuos,taxa_de_mutacao):
            
            self.qnt_individuos = qnt_individuos
            self.taxa_de_mutacao = taxa_de_mutacao
            
            self.populacao = self.cria_populacao()
            self.antiga_populacao = deepcopy(self.populacao)
            self.etapa_mutacao()
    
    def cria_populacao(self):
        populacao = []
        for i in range(self.qnt_individuos):
            populacao.append(Individuo(etapas=etapas,hobbits=deepcopy(hobbits)))
        return populacao
    
    def mutacao(self):          #Funcao que define uma unica mutacao
        
        individuo = random.randint(0,len(self.populacao)-1) #individuo a ser mutado
        #retirando um hobbit
        etapa = random.randint(0,len(self.populacao[0].individuo)-1)

        if len(self.populacao[individuo].individuo[etapa][1]) > 1:
            hobbit_pos = random.randint(0,len(self.populacao[individuo].individuo[etapa][1])-1)
            hobbit = self.populacao[individuo].individuo[etapa][1].pop(hobbit_pos)
        else:
            self.mutacao()
            return
        
        #adicionando o hobbit retirado
        nova_etapa = random.randint(0,len(self.populacao[0].individuo)-1)
        while(nova_etapa == etapa or hobbit in self.populacao[individuo].individuo[nova_etapa][1]): #seleciona etapa diferentes se for a mesma de onde foir retirada ou se o hobbit ja esta la
            nova_etapa = random.randint(0,len(self.populacao[0].individuo)-1)
        
        self.populacao[individuo].individuo[nova_etapa][1].append(hobbit)
        
        return
    
    def etapa_mutacao(self):    #Responsavel pela etapa de mutacao do algoritimo genetico
        for i in range(round(self.taxa_de_mutacao * self.qnt_individuos)):
            self.mutacao()
        return


if __name__ == '__main__':
    Otimizacao=Otimizacao(qnt_individuos=20, taxa_de_mutacao=1/16)
    print("Terminei")
