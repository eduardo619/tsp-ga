import random, sys
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
            for j in range(self._tIndividuo):
                self._Poblacion[i, j] = random.randint(0, 1)
        
        #Hacer de acuerdo al numero de generaciones
        for i in range(self._nGeneraciones):
            nueva_generacion = np.empty(shape=(self._tPoblacion, self._tIndividuo), dtype=int)
            muestra = None
            padres = None
            hijos = None
            sobrevivientes = None

            for j in range(self._tPoblacion):
                self._Fitness[j, 0] = self.EvaluaGanancia(self._Poblacion[j])
                self._Fitness[j, 1] = self.EvaluaTiempo(self._Poblacion[j])

                sobrevivientes = self.SelectSobrevivientes(cant_sobrevivientes)

            for j in range(cant_sobrevivientes):
                nueva_generacion[j] = sobrevivientes[j]

            for j in range(cant_sobrevivientes, self._tPoblacion):
                muestra = self.TomarMuestra()
                padres = self.ObtenerPadres(muestra)
                hijos = self.Cruza(padres)
                nueva_generacion[j] = hijos[0]
                j = j+1
                if j < self._tPoblacion:
                    nueva_generacion[j] = hijos[1]

            for j in range(can_mutados):
                x = random.randint(0, self._tPoblacion)
                nueva_generacion[x] = self.Mutar(nueva_generacion[x])
            
            self._Poblacion = nueva_generacion

    def Mutar(self, individuo):
        x = random.randint(0, self._tIndividuo)
        if individuo[x] == 1:
            individuo[x] = 0
        else:
            individuo[x] = 1
            
        return individuo

    def Cruza(self, padres):
        lim = int(self._tIndividuo / 2)
        inicio = random.randint(0, lim)
        fin = random.randint(lim, self._tIndividuo)
        res = np.empty(shape=(2, self._tIndividuo), dtype=int)

        for i in range(0, inicio):
            res[0, i] = padres[0, i]
            res[1, i] = padres[1, i]

        for i in range(inicio, fin):
            res[1, i] = padres[0, i]
            res[0, i] = padres[1, i]

        for i in range(fin, self._tIndividuo):
            res[0, i] = padres[0, i]
            res[1, i] = padres[1, i]

        return res

    def ObtenerPadres(self, muestra):
        res = np.empty(shape=(2, self._tIndividuo), dtype=int)
        fitness = np.empty(shape=(self._tMuestra, 2), dtype=float)

        for i in range(self._tMuestra):
            fitness[i, 0] = self.EvaluaGanancia(muestra[i])
            fitness[i, 1] = self.EvaluaTiempo(muestra[i])
        
        posicion_padres = np.empty(shape=2, dtype=int)

        for i in range(2):
            pos_mejor = 0
            mejor_fit = fitness[pos_mejor]

            for j in range(self._tMuestra):
                if fitness[j, 0] < mejor_fit[0] or fitness[j, 1] < mejor_fit[1]:
                    pos_mejor = j
                    mejor_fit = fitness[j]
            
            posicion_padres[i] = pos_mejor
            fitness[posicion_padres[i], 0] = sys.float_info.max
            fitness[posicion_padres[i], 1] = sys.maxsize
        
        res[0] = muestra[posicion_padres[0]]
        res[0] = muestra[posicion_padres[1]]
        return res

    def TomarMuestra(self):
        res = np.empty(shape=(self._tMuestra, self._tIndividuo), dtype=int)
        for i in range(self._tMuestra):
            pos = random.randint(0, self._tPoblacion)
            res[i] = self._Poblacion[pos]
        return res
    
    def SelectSobrevivientes(self, cantidad: int):
        res = np.empty(shape=(cantidad, self._tIndividuo), dtype=int)
        
        for i in range(cantidad):
            mejor_pos = 0
            mejor_fit = self._Fitness[mejor_pos]

            for j in range(self._tPoblacion):
                if self._Fitness[j, 0] < mejor_fit[0] or self._Fitness[j, 1] < mejor_fit[1]:
                    mejor_pos = j
                    mejor_fit = self._Fitness[j]
            
            res[i] = self._Poblacion[mejor_pos]
            self._Fitness[mejor_pos, 0] = sys.float_info.max
            self._Fitness[mejor_pos, 1] = sys.maxsize
        
        return res

    def EvaluaGanancia(self, vector):
        res = 0.00
        for i in range(vector):
            if vector[i] == 1:
                res = res + self._Ganancias[i]
        return res

    def EvaluaTiempo(self, vector):
        res = 0
        for i in range(vector):
            if vector[i] == 1:
                res = res + self._Minutos[i]
        return res