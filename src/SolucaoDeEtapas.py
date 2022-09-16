from copy import deepcopy
import random
#recombinação -> não faço ideia de como fazer
#mutação -> retirar um hobbit de uma etapa e colocar ele em uma etapa difierente
#usar elitismo???
#usar criacionismo???
class Individuo():
    
    def __init__(self):

        self.etapas = {
                        "etapa_2" : 10,
                        "etapa_3" : 30,
                        "etapa_4" : 60,
                        "etapa_5" : 65,
                        "etapa_6" : 70,
                        "etapa_7" : 75,
                        "etapa_8" : 80,
                        "etapa_9" : 85,
                        "etapa_A" : 90,
                        "etapa_B" : 95,
                        "etapa_C" : 100,
                        "etapa_D" : 110,
                        "etapa_E" : 120,
                        "etapa_F" : 130,
                        "etapa_G" : 140,
                        "etapa_H" : 150,
                      }

        self.hobbits = self.cria_hobbits()
        self.individuo = self.cria_individuo() #A estrutura representando o individuo em si
        self.tempoGasto = self.calcula_tempo() #Individuo mais apto sera o com menor tempo
        self.populacao = self.cria_populacao()
        #print(self.individuo)
        #print(self.hobbits)
        #print(self.tempoGasto)

    @staticmethod
    def cria_hobbits():
        # Nome do hobbit, Agilidade , Usos
        hobbits = [
            ["Frodo", 1.5, 7],
            ["Sam", 1.4, 7],
            ["Merry", 1.3, 7],
            ["Pippin", 1.2, 7]
        ]
        return hobbits
    
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


class Otimizacao():

    def __init__(self,qnt_individuos,taxa_de_mutacao):
            self.qnt_individuos = qnt_individuos
            self.taxa_de_mutacao = taxa_de_mutacao
    
   # def cria_populacao(self):
   #     populacao = []
   #     for i in range(self.qnt_individuos):
   #         populacao.append(self.cria_individuo())
   #     return populacao

if __name__ == '__main__':
    Oti = Otimizacao(qnt_individuos=20,taxa_de_mutacao=1/16)
    print("Terminei!")