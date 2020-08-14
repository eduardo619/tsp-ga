import random, sys, json, pandas
from datetime import datetime
import numpy as np

class TSPSimple(object):

    def __init__(self, nCiudades: int, nVehiculos: int, prcMutacion: float, tPoblacion: int, nGeneraciones: int, prcElitismo: float, prcMuestra: float):
        self._Start = datetime.now()
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
        self._Poblacion = None
        
    def Algotitmo(self):

        self.CargarDatos()

        cant_sobrevivientes = int(self._tPoblacion * self._prcElitismo)
        can_mutados = int(self._tPoblacion * self._prcMutacion)

        #Inicializar poblacion
        #self._Poblacion = np.random.random_integers(0, 1, size=(self._tPoblacion, self._tIndividuo))
        self._Poblacion = np.empty(shape=(self._tPoblacion, self._tIndividuo), dtype=int)
        
        for i in range(self._tPoblacion):
            for j in range(self._tIndividuo):
                if random.random() < 0.3:
                    self._Poblacion[i, j] = 1
                else:
                    self._Poblacion[i, j] = 0
        
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
                x = random.randint(0, self._tPoblacion - 1)
                nueva_generacion[x] = self.Mutar(nueva_generacion[x])
            
            self._Poblacion = nueva_generacion
            print("Generacion: {}".format(i + 1))

        self.SaveBests(5)
    
    def SaveBests(self, cantidad):
        bests = np.empty(shape=cantidad, dtype=int)
        for i in range(self._tPoblacion):
                self._Fitness[i, 0] = self.EvaluaGanancia(self._Poblacion[i])
                self._Fitness[i, 1] = self.EvaluaTiempo(self._Poblacion[i])
        
        for i in range(cantidad):
            mejor = 0
            mejor_fit = self._Fitness[mejor]

            for j in range(self._tPoblacion):
                if self._Fitness[j, 0] > mejor_fit[0] and self._Fitness[j, 1] < mejor_fit[1]:
                    mejor = j
                    mejor_fit = self._Fitness[mejor]
            bests[i] = mejor
            self._Fitness[bests[i], 0] = sys.float_info.min
            self._Fitness[bests[i], 1] = sys.maxsize
        
        data = {
            'value': []
        }

        for i in range(len(bests)):
            data['value'].append(self.toString(bests[i]))

        with open("resultado.json", 'w+') as file:
            json.dump(data, file, indent=4)

        time_elapsed = datetime.now() - self._Start
        print("Tiempo de ejecución: (hh:mm:ss.ms) {}".format(time_elapsed))

    def toString(self, index: int):
        res = ""
        for i in range(self._tIndividuo):
            res = res + str(self._Poblacion[index, i])
        return res
    
    def CargarDatos(self):
        with open("datos.json", 'r') as file:
            data = json.load(file)

        for i in range(len(data['minutos'])):
            self._Ganancias[i] = float(data['ganancias'][i])
            self._Minutos[i] = int(data['minutos'][i])

    def VerResultados(self):
        with open("resultado.json", 'r') as file:
            data = json.load(file)
        
        resultado = np.empty(shape=(len(data['value']), self._tIndividuo), dtype=int)
        fitness = np.empty(shape=(len(data['value']), 2))

        for i in range(len(data['value'])):
            contador = 0
            for j in data['value'][i]:
                resultado[i, contador] = int(j)
                contador = contador + 1
            fitness[i, 0] = self.EvaluaGanancia(resultado[i])
            fitness[i, 1] = self.EvaluaTiempo(resultado[i])
        
        for i in range(len(data['value'])):
            print("Individuo {}: Ganancias: $ {}  Tiempo: {}".format(str(i + 1), str(fitness[i, 0]), str(fitness[i, 1] / 60)))

    def Mutar(self, individuo):
        gn_a_mutar = random.randint(0, int(self._tIndividuo * 0.2))

        for i in range(gn_a_mutar):
            x = random.randint(0, self._tIndividuo - 1)
            if individuo[x] == 1:
                individuo[x] = 0
            else:
                individuo[x] = 1
            
        return individuo

    def Cruza(self, padres):
        first = random.randint(0, self._tIndividuo -1)
        last = first

        while last == first:
            last = random.randint(0, self._tIndividuo - 1)
        res = np.empty(shape=(2, self._tIndividuo), dtype=int)

        if last > first:
            inicio = first
            fin = last
        else:
            inicio = last
            fin = first
            

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
                if fitness[j, 0] > mejor_fit[0] or fitness[j, 1] < mejor_fit[1]:
                    pos_mejor = j
                    mejor_fit = fitness[j]
            
            posicion_padres[i] = pos_mejor
            fitness[posicion_padres[i], 0] = sys.float_info.min
            fitness[posicion_padres[i], 1] = sys.maxsize
        
        res[0] = muestra[posicion_padres[0]]
        res[1] = muestra[posicion_padres[1]]
        return res

    def TomarMuestra(self):
        res = np.empty(shape=(self._tMuestra, self._tIndividuo), dtype=int)
        for i in range(self._tMuestra):
            pos = random.randint(0, self._tPoblacion - 1)
            res[i] = self._Poblacion[pos]
        return res
    
    def SelectSobrevivientes(self, cantidad: int):
        res = np.empty(shape=(cantidad, self._tIndividuo), dtype=int)
        
        for i in range(cantidad):
            mejor_pos = 0
            mejor_fit = self._Fitness[mejor_pos]

            for j in range(self._tPoblacion):
                if self._Fitness[j, 0] > mejor_fit[0] or self._Fitness[j, 1] < mejor_fit[1]:
                    mejor_pos = j
                    mejor_fit = self._Fitness[j]
            
            res[i] = self._Poblacion[mejor_pos]
            self._Fitness[mejor_pos, 0] = sys.float_info.min
            self._Fitness[mejor_pos, 1] = sys.maxsize
        
        return res

    def EvaluaGanancia(self, vector):
        res = 0.00
        cont = 0
        for i in range(len(vector)):
            if cont == self._nciudades:
                cont = 0
            if vector[i] == 1:
                res = res + self._Ganancias[cont]
            cont = cont + 1
        return res

    def EvaluaTiempo(self, vector):
        res = 0
        horas = 0.00
        cumplen = 0
        cont = 0
        for i in range(len(vector)):
            if cont == self._nciudades:
                t_horas = horas / 60
                if t_horas < 8:
                    cumplen = cumplen + 1
                cont = 0
                horas = 0.00
            if vector[i] == 1:
                res = res + self._Minutos[cont]
                horas = horas + self._Minutos[cont]
            cont = cont + 1
        return res

obj = TSPSimple(30, 3, 0.5, 50, 5, 0.09, 0.25)
obj.Algotitmo()
obj.VerResultados()