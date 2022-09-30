from copy import deepcopy
import individuo_vars
import random

class Individuo():
    
    def __init__(self, etapas, hobbits, individuo = None):

        self.etapas = etapas

        self.hobbits = hobbits
        if individuo:
            self.individuo = individuo
        else:
            self.individuo = self.cria_individuo() #A estrutura representando o individuo em si
        self.tempoGasto,self.tempo_por_etapa = self.calcula_tempo() #Individuo mais apto sera o com menor tempo   
    
    def cria_individuo(self):
        distr = []
        for key in self.etapas:
            etapa = [key,[]]
            hob = random.choice(self.hobbits)
            #checa pra ver se tem uso disponivel
            while hob[2]== 0:
                hob = random.choice(self.hobbits)
            #adiciona o hobbit na lista de distribuição    
            etapa[1].append(hob[0])
            hob[2]=hob[2]-1

            distr.append(deepcopy(etapa))
        #distribui todos os hobbits restantes
        #esse for ta repugnante mas confia q funciona
        for hobbit in self.hobbits:
            while hobbit[2] > 0:
                etapa = random.choice(distr)
                if hobbit[0] not in etapa[1]:
                    etapa[1].append(hobbit[0])
                    hobbit[2] = hobbit[2]-1
        return distr
    
    def calcula_tempo(self):
        tempoTotal = 0
        tempo_por_etapa = []
        for etapa,hobbits in self.individuo:
            dificuldade = self.etapas[etapa]
            agilidade = 0
            for hobbit in hobbits:
                for i in self.hobbits:
                    if i[0]==hobbit:
                        agilidade+=i[1]
            try:
                tempoGasto = dificuldade/agilidade
            except:
                raise Exception
            tempoTotal+=tempoGasto
            tempo_por_etapa.append(tempoGasto)
        return tempoTotal,tempo_por_etapa

    def get_fitness(self):
        return self.tempoGasto

    def salva_individuo(self):
        fitness = 10000
        arq = open("trabalho-1-senhor-dos-aneis-grupo-2/melhor_individuo.txt","r")
        for linha in arq:
            if "Fitness" in linha:
                lista_linha = linha.split(" ")
                fitness = float(lista_linha[1][:-2])
                arq.close()
                break
        
        if self.tempoGasto < fitness:
            arq = open("trabalho-1-senhor-dos-aneis-grupo-2/melhor_individuo.txt",'w')
            arq.write("Fitness: {fitness}".format(fitness = self.tempoGasto))
            for i,etapa in enumerate(self.individuo):
                arq.write("\n" + etapa[0] + " ")
                for hobbit in etapa[1]:
                    arq.write(hobbit + " ")
                arq.write(str(self.tempo_por_etapa[i]))
        arq.close

if __name__ == '__main__':
    indiv = Individuo(etapas=individuo_vars.etapas, hobbits=individuo_vars.hobbits)
    indiv.salva_individuo()
    print(indiv.get_fitness())
    print("Terminei!")