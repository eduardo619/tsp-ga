import random
import numpy as np


class TSPSimple(object):

    def __init__(self, nCiudades: int, nVehiculos: int, prcMutacion: float, tPoblacion: int, nGeneraciones: int, prcElitismo: float, prcMuestra: float):
        self._nciudades = nCiudades
        self._nVehiculos = nVehiculos
        self._tIndividuo = self._nciudades * self._nVehiculos
        self._tPoblacion = tPoblacion
        self._tMuestra = int(self._tPoblacion * prcMuestra)
        self._nGeneraciones = nGeneraciones
        self._prcMutacion = prcMutacion
        self._prcElitismo = prcElitismo
        self._Ganancias = np.empty(shape=self._nciudades, dtype=float)
        self._Fitness = np.empty(shape=(self._tPoblacion, 2), dtype=float)
        self._Minutos = np.empty(shape=self._nciudades, dtype=int)
        self._Poblacion = np.empty(shape=(self._tPoblacion, self._tIndividuo), dtype=int)

    def Algotitmo(self):

        cant_sobrevivientes = int(self._tPoblacion * self._prcElitismo)
        can_mutados = int(self._tPoblacion * self._prcMutacion)

        #Inicializar poblacion
        for i in range(self._tPoblacion):
            self._Poblacion[i] = self.GeneraIndAleatorio()
        
        #Hacer de acuerdo al numero de generaciones
        for i in range(self._nGeneraciones):
            nueva_generacion = np.empty(shape=(self._tPoblacion, self._tIndividuo), dtype=int)
            muestra = np.empty(shape=(self._tMuestra, self._tIndividuo), dtype=int)
            padres = np.empty(shape=(2, self._tIndividuo), dtype=int)
            hijos = np.empty(shape=(2, self._tIndividuo), dtype=int)
            sobrevivientes = np.empty(shape=(cant_sobrevivientes, self._tIndividuo), dtype=int)

            for j in range(self._tPoblacion):
                self._Fitness[j, 0] = self.EvaluaGanancia(self._Poblacion[j])
                self._Fitness[j, 1] = self.EvaluaTiempo(self._Poblacion[j])
    
    def GeneraIndAleatorio(self):

        c_x_v = int(self._nciudades / self._nVehiculos)

    def EvaluaGanancia(self, vector):
        print("s")

    def EvaluaTiempo(self, vector):
        print("s")