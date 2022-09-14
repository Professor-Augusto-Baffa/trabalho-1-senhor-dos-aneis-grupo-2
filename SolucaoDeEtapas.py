


class ResolveEtapas():
    
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

if __name__ == '__main__':
    MinhaClasse = ResolveEtapas()