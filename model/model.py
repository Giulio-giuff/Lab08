from database.consumo_DAO import ConsumoDAO
from database.impianto_DAO import ImpiantoDAO
import datetime

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO

        consumi1=ConsumoDAO.get_consumi(1)
        consumi2=ConsumoDAO.get_consumi(2)
        num_conti1=0
        consumo_tot1=0
        for consumo in consumi1:
            mese2=consumo.data.month
            if mese2-mese==0:
                consumo_tot1=consumo.kwh+consumo_tot1
                num_conti1=num_conti1+1
        print(f"consumo medio impianto1 = {consumo_tot1/num_conti1}")
        num_conti2 = 0
        consumo_tot2 = 0
        for consumo in consumi2:
            mese2=consumo.data.month
            if mese2-mese==0:
                consumo_tot2=consumo.kwh+consumo_tot2
                num_conti2=num_conti2+1
        print(f"consumo medio impianto2 = {consumo_tot2 / num_conti2}")
        return [("Impianto A",consumo_tot1/num_conti1), ("Impianto B",consumo_tot2/num_conti2)]

        print(consumi1)


    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno==7:
            if self.__costo_ottimo==-1 or costo_corrente<self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale.copy()
            return
        for impianto in [1,2]:
            consumo=consumi_settimana[impianto][giorno]
            costo_extra=0
            if ultimo_impianto is not None and ultimo_impianto != impianto:
                costo_extra=5 #costo del cambio
            nuovo_costo=costo_corrente+costo_extra+consumo
            self.__ricorsione(sequenza_parziale+[impianto] , giorno+1, impianto, nuovo_costo, consumi_settimana)


    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        consumi1 = ConsumoDAO.get_consumi(1)
        consumi2 = ConsumoDAO.get_consumi(2)
        consumi_settimana={}
        consumi_settimana[1] = []
        consumi_settimana[2] = []
        cont=0
        for consumo in consumi1:
            mese2=consumo.data.month
            if mese2-mese==0:
                consumi_settimana[1].append(consumo.kwh)
                cont+=1
            if cont==7:
                break
        cont=0
        for consumo in consumi2:
            mese2=consumo.data.month
            if mese2-mese==0:
                consumi_settimana[2].append(consumo.kwh)
                cont+=1
            if cont==7:
                break
        return consumi_settimana



