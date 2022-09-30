from Individuo import Individuo
from individuo_vars import *

import random

from copy import deepcopy


class Otimizacao():

    def __init__(self, qnt_individuos, taxa_de_mutacao, taxa_elite, geracoes, taxa_pais, taxa_filhos, taxa_novos_individuos, tamanho_do_individuo):
            
            if taxa_elite + taxa_filhos + taxa_novos_individuos > 1:
                print("Taxas de elite + filhos + novos individuos deve ser inferior que 1")
                return None

            self.qnt_individuos = qnt_individuos
            self.taxa_de_mutacao = taxa_de_mutacao
            self.taxa_de_mutacao_original = taxa_de_mutacao
            self.qnt_elite =int(qnt_individuos * taxa_elite)
            self.geracoes = geracoes
            self.qnt_pais = int(qnt_individuos * taxa_pais)
            self.qnt_filhos = int(qnt_individuos * taxa_filhos)
            self.tamanho_do_individuo = tamanho_do_individuo
            self.peso_da_mutacao = 50
            self.tamanho_nova_geracao = qnt_individuos - self.qnt_elite - int(qnt_individuos * taxa_novos_individuos)
            self.ultima_geracao_ordenada = []
            self.melhor_individuo = []
            
            self.populacao = self.cria_populacao()

    def run(self):
        populacao_ordenada = []
        antigo_melhor = []    
        for geracao in range(self.geracoes):
            #salva melhor individuo antigo para usar depois
            if populacao_ordenada != []:
                antigo_melhor = populacao_ordenada[0]
            #ordena pelo melhor fitness
            populacao_ordenada = self.ordena_populacao()
            melhor_individuo = populacao_ordenada[0]
            #altera a taxa de mutacao baseado se o melhor individuo esta mudando ou nao
            if self.taxa_de_mutacao > 0.05:
                pass
            elif antigo_melhor == melhor_individuo:
                self.taxa_de_mutacao+=0.001
                if self.peso_da_mutacao < 100:
                    self.peso_da_mutacao += 1
            else: 
                self.taxa_de_mutacao = self.taxa_de_mutacao_original
                self.peso_da_mutacao = 50
            #seleciona a elite
            elite = deepcopy(populacao_ordenada[:self.qnt_elite])
            #recombina os genes dos pais na nova geracao
            nova_geracao = self.recombinacao_aleatoria(populacao_ordenada)
            #adiciona nova geracao a populacao
            for individuo in nova_geracao:
                self.populacao.append(individuo)
            #selecionando a nova geracao baseado nos melhores
            self.populacao = self.ordena_populacao()[:self.tamanho_nova_geracao]
            #mutacao
            self.etapa_mutacao()
            #volta com a elite
            for individuo in elite:
                self.populacao.append(individuo)
            #cria novos individuos aleatorios
            self.regenera_populacao()
            
            print("Geracao {geracao} concluida! --- Tempo do melhor individuo = {tempo:.2f}".format(geracao = geracao, tempo=populacao_ordenada[0].tempoGasto))
        
        self.ultima_geracao_ordenada = self.ordena_populacao()
        self.melhor_individuo = self.ultima_geracao_ordenada[0]

    def cria_populacao(self):
        populacao = []
        for i in range(self.qnt_individuos):
            populacao.append(Individuo(etapas=etapas,hobbits=deepcopy(hobbits)))
        return populacao

    def regenera_populacao(self): 
        while(len(self.populacao)<self.qnt_individuos):
            self.populacao.append(Individuo(etapas=etapas,hobbits=deepcopy(hobbits)))
        return
    
    def recombinacao_pelo_meio(self, populacao_ordenada):
        
        nova_populacao = []
        pais = populacao_ordenada[:self.qnt_pais]
        
        for i in range(self.qnt_filhos):
            #pai_especifico = random.choices(pais,k=2)
            pai_especifico = []
            pai_especifico.append(self.seleciona_pais())
            pai_especifico.append(self.seleciona_pais())
            #primeira metade do primeiro pai, segunda metade do segundo pai
            individuo = pai_especifico[0].individuo[:int(self.tamanho_do_individuo/2)] + pai_especifico[1].individuo[int(self.tamanho_do_individuo/2):]
            individuo = self.valida_individuo(individuo)
            filho = Individuo(hobbits=deepcopy(hobbits), etapas=etapas, individuo=individuo)
            nova_populacao.append(filho)

        return nova_populacao
    
    def recombinacao_aleatoria(self, populacao_ordenada):

        nova_populacao = []
        pais = populacao_ordenada[:self.qnt_pais]

        for i in range(self.qnt_filhos):
            individuo = []
            pais_especificos = random.choices(pais,k=2)
            #pais_especificos = self.seleciona_pais()
            if len(pais_especificos) != 2:
                filho = Individuo(hobbits=deepcopy(hobbits), etapas=etapas)
            else:
                for j in range(len(pais_especificos[0].individuo)):
                    genes = [deepcopy(pais_especificos[0].individuo[j]),deepcopy(pais_especificos[1].individuo[j])]
                    individuo.append(random.choice(genes))
                individuo = self.valida_individuo(individuo)
                filho = Individuo(hobbits=deepcopy(hobbits), etapas=etapas, individuo=individuo)
            nova_populacao.append(deepcopy(filho))
        
        return nova_populacao

    def seleciona_pais(self): # recebe a populacao e faz a selecao dos pais via metodo da roleta
        pais = []
        total_fitness = 0.0
        r = random.random()

        for i in self.populacao:
            total_fitness += i.get_fitness()

        for i in self.populacao:
            pi = i.get_fitness()/total_fitness

            if r < pi:
                return i
            else:
                r -= pi

            if len(pais) == 2:
                break

        return pais

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
            etapas = []
            if qnt_hobbit[i] > 7:
                for j, posicao in enumerate(individuo):
                    if hobbit in posicao[1] and len(posicao[1]) > 1:
                        etapas.append(j)
            while qnt_hobbit[i] > 7:
                    #if hobbit in individuo[etapa][1] and len(individuo[etapa][1]) > 1:
                    #    individuo[etapa][1].remove(hobbit)
                    #    qnt_hobbit[i] -= 1
                    #etapa+=1
                    #if etapa >= self.tamanho_do_individuo:
                    #    #print("Houve algum erro na validação do individuo")
                    #    #Individuo é invalido, retorna None para gerar um novo individuo
                    #    return None
                if etapas == []:
                    return None
                etapa = random.choice(etapas)
                individuo[etapa][1].remove(hobbit)
                etapas.remove(etapa)
                qnt_hobbit[i] -= 1
                etapa+=1
                if etapa >= self.tamanho_do_individuo:
                    #Individuo é invalido, retorna None para gerar um novo individuo
                    return None
        #colocar os que faltam
        for pos in range(len(qnt_hobbit)):
            hobbit = hobbits[pos][0]
            while qnt_hobbit[pos] < 7:
                etapa = random.choice(range(self.tamanho_do_individuo))
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
        
        lista_ponderada = [0] * self.peso_da_mutacao + [1] * (100 - self.peso_da_mutacao)
        for i in range(round(self.taxa_de_mutacao * (self.qnt_individuos-self.qnt_filhos))):
            mutacao = random.choice(lista_ponderada)
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
    #Otimizacao=Otimizacao(qnt_individuos=500, taxa_de_mutacao=0.01, qnt_elite=50, geracoes=500, qnt_pais=300, qnt_filhos=300, tamanho_do_individuo=16)
    Otimizacao=Otimizacao(qnt_individuos=1000, taxa_de_mutacao=0.01, taxa_elite=0.2, geracoes=1000, taxa_pais=0.8, taxa_filhos=0.7,taxa_novos_individuos=0.1 , tamanho_do_individuo=16)
    Otimizacao.run()
    melhor_individuo = Otimizacao.get_melhor_individuo()
    print("Terminei")
    print("Melhor individuo:")
    print(melhor_individuo.individuo)
    melhor_individuo.salva_individuo()
