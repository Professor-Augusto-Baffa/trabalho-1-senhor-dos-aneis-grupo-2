from Individuo import Individuo
from individuo_vars import *

import random

from copy import deepcopy


class Otimizacao():

    def __init__(self, qnt_individuos, taxa_de_mutacao, qnt_elite, geracoes):
            
            self.qnt_individuos = qnt_individuos
            self.taxa_de_mutacao = taxa_de_mutacao
            self.qnt_elite = qnt_elite
            self.geracoes = geracoes
            
            self.populacao = self.cria_populacao()
            
            for geracao in range(self.geracoes):
                populacao_ordenada = self.ordena_populacao()
                elite = deepcopy(populacao_ordenada[:self.qnt_elite])
                #recombina os genes dos pais
                self.populacao = []
                self.regenera_populacao()
                self.etapa_mutacao()
                for individuo in elite:
                    self.populacao.append(individuo)
                print("Geração {geracao} concluida!".format(geracao = geracao))
            
            self.ultima_geracao_ordenada = self.ordena_populacao()
            self.melhor_individuo = self.ultima_geracao_ordenada[0]

    def cria_populacao(self):
        populacao = []
        for i in range(self.qnt_individuos):
            populacao.append(Individuo(etapas=etapas,hobbits=deepcopy(hobbits)))
        return populacao

    def regenera_populacao(self): 
        while(len(self.populacao)<self.qnt_individuos-self.qnt_elite):
            self.populacao.append(Individuo(etapas=etapas,hobbits=deepcopy(hobbits)))
        return
    
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

    def ordena_populacao(self):
        populacao_ordenada=sorted(self.populacao, key=Individuo.get_fitness)
        return populacao_ordenada
    
    def get_melhor_individuo(self):
        return self.melhor_individuo

if __name__ == '__main__':
    Otimizacao=Otimizacao(qnt_individuos=1000, taxa_de_mutacao=1/16, qnt_elite=40, geracoes=1000)
    melhor_individuo = Otimizacao.get_melhor_individuo()
    print("Terminei")
