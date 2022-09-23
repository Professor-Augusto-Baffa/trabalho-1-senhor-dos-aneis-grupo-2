from Individuo import Individuo
from individuo_vars import *

import random

from copy import deepcopy


class Otimizacao():

    def __init__(self, qnt_individuos, taxa_de_mutacao, qnt_elite, geracoes, qnt_pais, qnt_filhos, tamanho_do_individuo):
            
            self.qnt_individuos = qnt_individuos
            self.taxa_de_mutacao = taxa_de_mutacao
            self.taxa_de_mutacao_original = taxa_de_mutacao
            self.qnt_elite = qnt_elite
            self.geracoes = geracoes
            self.qnt_pais = qnt_pais
            self.qnt_filhos = qnt_filhos
            self.tamanho_do_individuo = tamanho_do_individuo
            populacao_ordenada = []
            antigo_melhor = []
            
            self.populacao = self.cria_populacao()
            
            for geracao in range(self.geracoes):
                if populacao_ordenada != []:
                    antigo_melhor = populacao_ordenada[0]
                populacao_ordenada = self.ordena_populacao()
                melhor_individuo = populacao_ordenada[0]
                if antigo_melhor == melhor_individuo:
                    self.taxa_de_mutacao+=0.01
                else: 
                    self.taxa_de_mutacao = self.taxa_de_mutacao_original
                elite = deepcopy(populacao_ordenada[:self.qnt_elite])
                #recombina os genes dos pais
                self.populacao = self.recombina_messy(populacao_ordenada)
                self.etapa_mutacao()
                self.regenera_populacao()
                for individuo in elite:
                    self.populacao.append(individuo)
                
                print("Geracao {geracao} concluida! --- Tempo do melhor individuo = {tempo:.2f}".format(geracao = geracao, tempo=populacao_ordenada[0].tempoGasto))
            
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
    
    def recombina_populacao(self, populacao_ordenada):
        
        nova_populacao = []
        pais = populacao_ordenada[:self.qnt_pais]
        
        for i in range(self.qnt_filhos):
            pai_especifico = random.choices(populacao_ordenada,k=2)
            #primeira metade do primeiro pai, segunda metade do segundo pai
            individuo = pai_especifico[0].individuo[:int(self.tamanho_do_individuo/2)] + pai_especifico[1].individuo[int(self.tamanho_do_individuo/2):]
            individuo = self.valida_individuo(individuo)
            filho = Individuo(hobbits=deepcopy(hobbits), etapas=etapas, individuo=individuo)
            nova_populacao.append(filho)

        return nova_populacao
    
    def recombina_messy(self, populacao_ordenada):

        nova_populacao = []
        pais = populacao_ordenada[:self.qnt_pais]

        for i in range(self.qnt_filhos):
            individuo = []
            pais_especificos = random.choices(populacao_ordenada,k=2)
            for j in range(len(pais_especificos[0].individuo)):
                genes = [deepcopy(pais_especificos[0].individuo[j]),deepcopy(pais_especificos[1].individuo[j])]
                individuo.append(random.choice(genes))
            individuo = self.valida_individuo(individuo)
            filho = Individuo(hobbits=deepcopy(hobbits), etapas=etapas, individuo=individuo)
            nova_populacao.append(deepcopy(filho))
        
        return nova_populacao

    def valida_individuo(self, individuo): # recebe uma lista com o individuo e confere se ele esta nos conformes
        
        qnt_hobbit = [0,0,0,0]

        for etapa in individuo:
            if "Frodo" in etapa[1]:
                qnt_hobbit[hobbitsEnum.Frodo.value] += 1
            if "Sam" in etapa[1]:
                qnt_hobbit[hobbitsEnum.Sam.value] += 1
            if "Merry" in etapa[1]:
                qnt_hobbit[hobbitsEnum.Merry.value] += 1
            if "Pippin" in etapa[1]:
                qnt_hobbit[hobbitsEnum.Pippin.value] += 1
        #retirar sobressalentes
        for i,qnt in enumerate(qnt_hobbit):
            etapa = 0
            hobbit = hobbits[i][0]
            while qnt_hobbit[i] > 7:
                if hobbit in individuo[etapa][1] and len(individuo[etapa][1]) > 1:
                    individuo[etapa][1].remove(hobbit)
                    qnt_hobbit[i] -= 1
                etapa+=1
                if etapa >= self.tamanho_do_individuo:
                    #print("Houve algum erro na validação do individuo")
                    #Individuo é invalido, retorna None para gerar um novo individuo
                    return None
        #colocar os que faltam
        for pos in range(len(qnt_hobbit)):
            hobbit = hobbits[pos][0]
            while qnt_hobbit[pos] < 7:
                etapa = random.choice(range(15))
                if hobbit not in individuo[etapa][1]:
                    individuo[etapa][1].append(hobbit)
                    qnt_hobbit[pos] += 1
        return individuo


    def mutacao_parcial(self):          #Funcao que define uma unica mutacao
        
        individuo = random.randint(0,len(self.populacao)-1) #individuo a ser mutado
        #retirando um hobbit
        etapa = random.randint(0,len(self.populacao[0].individuo)-1)

        if len(self.populacao[individuo].individuo[etapa][1]) > 1:
            hobbit_pos = random.randint(0,len(self.populacao[individuo].individuo[etapa][1])-1)
            hobbit = self.populacao[individuo].individuo[etapa][1].pop(hobbit_pos)
        else:
            self.mutacao_parcial()
            return
        
        #adicionando o hobbit retirado
        nova_etapa = random.randint(0,len(self.populacao[0].individuo)-1)
        while(nova_etapa == etapa or hobbit in self.populacao[individuo].individuo[nova_etapa][1]): #seleciona etapa diferentes se for a mesma de onde foir retirada ou se o hobbit ja esta la
            nova_etapa = random.randint(0,len(self.populacao[0].individuo)-1)
        
        self.populacao[individuo].individuo[nova_etapa][1].append(hobbit)
        
        return
    
    def mutacao_completa(self):
        
        individuo = random.randint(0,len(self.populacao)-1)
        etapa = random.randint(0,len(self.populacao[0].individuo)-1)
        nova_etapa = random.randint(0,len(self.populacao[0].individuo)-1)
        while(etapa == nova_etapa):
            nova_etapa = random.randint(0,len(self.populacao[0].individuo)-1)

        self.populacao[individuo].individuo[etapa][1],self.populacao[individuo].individuo[nova_etapa][1] = self.populacao[individuo].individuo[nova_etapa][1],self.populacao[individuo].individuo[etapa][1]
        return



    def etapa_mutacao(self):    #Responsavel pela etapa de mutacao do algoritimo genetico
        for i in range(round(self.taxa_de_mutacao * (self.qnt_individuos-self.qnt_filhos))):
            mutacao = random.randint(0,1)
            if mutacao == 1:
                self.mutacao_completa()
            else:
                self.mutacao_parcial()
        return

    def ordena_populacao(self):
        populacao_ordenada=sorted(self.populacao, key=Individuo.get_fitness)
        return populacao_ordenada
    
    def get_melhor_individuo(self):
        return self.melhor_individuo

if __name__ == '__main__':
    Otimizacao=Otimizacao(qnt_individuos=1000, taxa_de_mutacao=0.05, qnt_elite=20, geracoes=1000, qnt_pais=500, qnt_filhos=800, tamanho_do_individuo=16)
    melhor_individuo = Otimizacao.get_melhor_individuo()
    print("Terminei")
    print("Melhor individuo:")
    print(melhor_individuo.individuo)
    melhor_individuo.salva_individuo()
