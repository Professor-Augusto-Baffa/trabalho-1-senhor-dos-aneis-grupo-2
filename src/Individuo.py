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
        self.tempoGasto = self.calcula_tempo() #Individuo mais apto sera o com menor tempo
        #print(self.individuo)
        #print(self.hobbits)
        #print(self.tempoGasto)
    
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
        return tempoTotal

    def get_fitness(self):
        return self.tempoGasto

    def salva_individuo(self):
        fitness = 0
        arq = open("melhor_individuo.txt","r")
        for linha in arq:
            if "Fitness" in linha:
                lista_linha = linha.split(" ")
                fitness = float(lista_linha[1][:-2])
                arq.close()
                break
        
        if self.tempoGasto < fitness:
            arq = open("melhor_individuo.txt",'w')
            arq.write("Fitness: {fitness}".format(fitness = self.tempoGasto))
            for etapa in self.individuo:
                arq.write("\n" + etapa[0] + " ")
                for hobbit in etapa[1]:
                    arq.write(hobbit + " ")
        arq.close

if __name__ == '__main__':
    indiv = Individuo(etapas=individuo_vars.etapas, hobbits=individuo_vars.hobbits)
    indiv.salva_individuo()
    print(indiv.get_fitness())
    print("Terminei!")