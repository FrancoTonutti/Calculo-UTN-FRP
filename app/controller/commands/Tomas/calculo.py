import numpy as np
#import matplotlib.pyplot as plt
import math
from numpy import array

# Funciones prefijadas
from numpy.core._multiarray_umath import ndarray


def Matriztrans(X, Y):
    # Se calcula la longitud nuevamente
    DeltaX = Y[0] - X[0]
    DeltaY = Y[1] - X[1]
    L = math.sqrt(DeltaX ** 2 + DeltaY ** 2)
    # Calculo del coseno como delta X sobre L
    Cos = DeltaX / L
    # Calculo del seno como delta y sobre L
    Sen = DeltaY / L
    # Armado de renglones
    return array([
        [Cos, -Sen, 0, 0, 0, 0],
        [Sen, Cos, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, Cos, -Sen, 0],
        [0, 0, 0, Sen, Cos, 0],
        [0, 0, 0, 0, 0, 1]
    ])


def MatrizGlobal(local, transformacion):
    # transponesmos la matriz de transformacion
    T = np.transpose(transformacion)
    # pre-multiplicacion de matrices
    A = T.dot(local)
    # Posmultiplicacion de matrices
    E = A.dot(transformacion)
    return E


# Funcion que forma un vector de 1 y 0 a partir de los puntos definidos como dezplasamientos libres o restringidos
def resticciones(puntos):
    VRes = np.ones((len(puntos) * 3, 1))
    for i in range(0, len(puntos)):
        VRes[i * 3] = puntos[i].P[0]
        VRes[i * 3 + 1] = puntos[i].P[1]
        VRes[i * 3 + 2] = puntos[i].P[2]
    return VRes


def Matrizconectividad(CB):
    # Se arama una matriz de 6 columnas con las cantidad de renglones como puntos halla
    # La matriz es una matriz auxiliar que nos permite hacer una matriz de conectividad para luego
    # armar la matriz de rigidez global de la estructura
    TC = np.zeros((CB.shape[0], 6))
    # Para en el renglon i entre las columnas 1 y 3
    for i in range(0, CB.shape[0]):
        for j in range(0, 3):
            # si el valor de la matriz de puntos es 0 el valor que se otorga a la matriz de conectividad es 0
            if CB[i][0] == 0:
                TC[i][j] = int(j)
            else:
                TC[i][j] = int(j + 3 * (CB[i][0]))
        for j in range(3, 6):
            # Para los valores de j de 3 a 6
            if CB[i][1] == 0:
                TC[i][j] = int(j - 3)
            else:
                TC[i][j] = int((j - 3) + 3 * (CB[i][1]))
    A = array(TC, dtype=int)
    return A


# matriz de rigidez
def MatrizGlobalEnsambalda(Barras, CB):
    b = len(Barras)
    TC = Matrizconectividad(CB)
    # Ensamble de matriz Global de la estructura
    KG = np.zeros((b * 3, b * 3))
    Kiel = np.zeros((6, 6))
    for iel in range(0, CB.shape[0]):
        Kiel = Barras[iel].G
        for i in range(0, 6):
            for j in range(0, 6):
                try:
                    index_a = TC[iel][i]
                    index_b = TC[iel][j]
                    parte1 = KG[index_a][index_b]
                    parte2 = Kiel[i][j]
                    KG[TC[iel][i]][TC[iel][j]] = parte1 + parte2
                except IndexError as ex:
                    print(ex)
                    print("i", i)
                    print("j", j)
                    print("TC", TC)


    return KG


def FuerzaGlob(fuerzaloc, barras):
    Sen = barras.seno
    Cos = barras.coseno

    # pasaje de fuerzas a coordenas globales
    Fxa = fuerzaloc[0] * Cos + fuerzaloc[1] * Sen
    Fya = -fuerzaloc[0] * Sen + fuerzaloc[1] * Cos
    Ma = fuerzaloc[2]
    Fxb = fuerzaloc[3] * Cos + fuerzaloc[4] * Sen
    Fyb = -fuerzaloc[3] * Sen + fuerzaloc[4] * Cos
    Mb = fuerzaloc[5]
    F = np.zeros((6, 1))
    F[0] = Fxa
    F[1] = Fya
    F[2] = Ma
    F[3] = Fxb
    F[4] = Fyb
    F[5] = Mb
    return F


def CargaPunto(barras, cargas, matcon):
    # Se arma una matriz que obtenga las fuerzas en los nodos en cordenadas globales
    CPG = np.zeros((b, 6, 1))
    for n in range(0, b):
        if cargas[n] == 0:
            CPG[n] = np.zeros((6, 1))
        else:
            CPG[n] = FuerzaGlob(cargas[n].Qf(barras[n].L), barras[n])

    # Se suman las fuerzas en los nodos de las barras concurrentes

    CP = np.zeros((Cantpuntos, 3, 1))
    for i in range(0, Cantpuntos):
        for h in range(0, b):
            if int(matcon[h, 0]) == i:
                CP[i, 0, 0] = CPG[h, 0, 0]
                CP[i, 1, 0] = CPG[h, 1, 0]
                CP[i, 2, 0] = CPG[h, 2, 0]
    for i in range(0, b):
        for h in range(0, b):
            if matcon[h, 0] == i:
                CP[i + 1, 0, 0] = CP[i + 1, 0, 0] + CPG[h, 3, 0]
                CP[i + 1, 1, 0] = CP[i + 1, 1, 0] + CPG[h, 4, 0]
                CP[i + 1, 2, 0] = CP[i + 1, 2, 0] + CPG[h, 5, 0]

    # lo paso a valores en forma de vector

    Fultimas = np.zeros((Cantpuntos * 3, 1))
    for i in range(0, 4):
        Fultimas[i * 3] = CP[i, 0, 0]
        Fultimas[i * 3 + 1] = CP[i, 1, 0]
        Fultimas[i * 3 + 2] = CP[i, 2, 0]

    return Fultimas


def matrizmodificada(MatGlo, VectorApoyos):
    A = MatGlo
    # A partir de las restricciones de los puntos se modifican las rigideces de la matriz global
    for i in range(0, VectorApoyos.shape[0]):
        if VectorApoyos[i] == 0:
            A[i][i] = 999999999999999999999999999
    return A


def Desplazamientos(Matmod, FuerzasEnNodos):
    # Paso las fuerzas de KN a MN para poder multiplicarla en la matriz
    F = FuerzasEnNodos
    # Matriz inversa de la matriz Global con los valores eliminados
    Minv = (np.linalg.inv(Matmod))
    # Calculo de los desplazamientos, los movimientos impedidos no aparece aun
    Des = np.dot(Minv, F)
    return Des


# Clase de barras, incluye columnas y vigas (tal vez deberia cambiarlo y especificar en columnas y vigas por el tema de la armadura)

class Columna:
    '''Definimos un tramo de viga.
    E: Módulo de elasticidad
    I: Inercia de la sección transversal
    A: Area de la barra
    a: punto inicial
    b: punto final'''

    def __init__(self, E, I, A, a, b):
        '''ATRIBUTOS:
            self.E: Módulo de elasticidad
            self.I: Inercia de la sección transversal
            self.A: Area de la barra
            self.a: punto inicial
            self.b: punto final
            self.k: matriz de rigidez del tramo'''

        self.a = a
        self.b = b
        self.L = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)
        self.E = E
        self.I = I
        self.A = A
        self.seno = (b[1] - b[0]) / self.L
        self.coseno = (a[1] - a[0]) / self.L

        # Matriz de rigidez del elemento
        self.k = np.array([
            [E * A / self.L, 0, 0, -E * A / self.L, 0, 0],
            [0, 12 * E * I / self.L ** 3, 6 * E * I / self.L ** 2, 0, -12 * E * I / self.L ** 3,
             6 * E * I / self.L ** 2],
            [0, 6 * E * I / self.L ** 2, 4 * E * I / self.L, 0, -6 * E * I / self.L ** 2, 2 * E * I / self.L],
            [-E * A / self.L, 0, 0, E * A / self.L, 0, 0],
            [0, -12 * E * I / self.L ** 3, -6 * E * I / self.L ** 2, 0, 12 * E * I / self.L ** 3,
             -6 * E * I / self.L ** 2],
            [0, 6 * E * I / self.L ** 2, 2 * E * I / self.L, 0, -6 * E * I / self.L ** 2, 4 * E * I / self.L]
        ])

        # Matriz de rigidez del elemento en ejes globales
        # Calculo de matrices de transformacion
        self.T = Matriztrans(self.a, self.b)
        # Calculo de matriz de global por barra
        self.G = MatrizGlobal(self.k, self.T)


class Viga:
    '''Definimos un tramo de viga.
    E: Módulo de elasticidad
    I: Inercia de la sección transversal
    A: Area de la barra
    a: punto inicial
    b: punto final'''

    def __init__(self, E, I, A, a, b):
        '''ATRIBUTOS:
            self.E: Módulo de elasticidad
            self.I: Inercia de la sección transversal
            self.A: Area de la barra
            self.a: punto inicial
            self.b: punto final
            self.k: matriz de rigidez del tramo'''

        self.a = a
        self.b = b
        self.L = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)
        self.E = E
        self.I = I
        self.A = A
        self.seno = (b[1] - b[0]) / self.L
        self.coseno = (a[1] - a[0]) / self.L

        # Matriz de rigidez del elemento
        self.k = array([
            [E * A / self.L, 0, 0, -E * A / self.L, 0, 0],
            [0, 12 * E * I / self.L ** 3, 6 * E * I / self.L ** 2, 0, -12 * E * I / self.L ** 3,
             6 * E * I / self.L ** 2],
            [0, 6 * E * I / self.L ** 2, 4 * E * I / self.L, 0, -6 * E * I / self.L ** 2, 2 * E * I / self.L],
            [-E * A / self.L, 0, 0, E * A / self.L, 0, 0],
            [0, -12 * E * I / self.L ** 3, -6 * E * I / self.L ** 2, 0, 12 * E * I / self.L ** 3,
             -6 * E * I / self.L ** 2],
            [0, 6 * E * I / self.L ** 2, 2 * E * I / self.L, 0, -6 * E * I / self.L ** 2, 4 * E * I / self.L]
        ])

        # Matriz de rigidez del elemento en ejes globales
        # Calculo de matrices de transformacion
        self.T = Matriztrans(self.a, self.b)
        # Calculo de matriz de global por barra
        self.G = MatrizGlobal(self.k, self.T)


# Cargas incluye carga puntual y carga distribuida, (no esta incluyendo el momento puntual)

class Carga:
    '''Clase carga'''

    def __init__(self, tipo):
        '''
        tipo = 0: Carga puntual
        tipo = 1: Carga distribuida
        '''
        self.tipo = tipo

    def Tipo(self):
        if self.tipo == 0:
            print("Carga puntual")
        elif self.tipo == 1:
            print('Carga distribuida')
        else:
            print('No definido')


class CargaPuntual(Carga):
    '''Clase carga puntual'''

    def __init__(self, P=0, a=0, alfa=0):
        '''Carga puntual P.
        P: valor de la carga. Positivo hacia abajo.
        a: posicion de la carga respecto al extremo izquierdo del tramo.
        alfa: angulo de carga (90= perpendicular a la barra)'''
        Carga.__init__(self, 0)
        self.P = P
        self.a = a
        self.alfa = alfa

    def __str__(self):
        return 'Carga puntual\n   Valor= ' + str(self.P) + 'kN' \
               + '\n   Posición, x= ' + str(self.a) + 'm'

    # Reacciones nodales equivalentes
    def Qf(self, L):
        '''Reacciones nodales equivalentes para una carga puntual.
        L: Longitud de la viga'''
        a = self.a
        b = L - a
        Pver = (math.sin(self.alfa * (math.pi) / 180)) * self.P
        Phor = (math.cos(self.alfa * (math.pi) / 180)) * self.P

        Mat = array([
            [Phor / 2],
            [((Pver * (b ** 2)) / (L ** 3)) * (L + 2 * a)],
            [-Pver * a * (b ** 2) / (L ** 2)],
            [Phor / 2],
            [((Pver * (a ** 2)) / (L ** 3)) * (L + 2 * b)],
            [-Pver * (a ** 2) * b / (L ** 2)]
        ])
        return Mat

    # Fuerza cortante en una sección (viga sin apoyos)
    def FQ(self, x, L):
        '''Aporte a la fuerza cortante en una sección debido a una carga puntual,
        x: posición de la sección considerada respecto al extremo izquierdo
        L: longitud del tramo'''
        if self.a < x < L:
            return -(self.P * (math.sin(self.alfa * (math.pi) / 180)))
        else:
            return 0

    # Momento flector en una sección (viga simplemente apoyada)
    def MF(self, x, L):
        '''Aporte al Momento flector en una sección debido a una carga puntual,
        x: posición de la sección considerada respecto al extremo izquierdo
        L: longitud del tramo'''
        if 0 <= x < self.a:
            return (1 - self.a / L) * (self.P * (math.sin(self.alfa * (math.pi) / 180))) * x
        elif x <= L:
            return self.a * (self.P * (math.sin(self.alfa * (math.pi) / 180))) * (1 - x / L)
        else:
            return 0


class CargaDistribuida(Carga):
    '''Clase carga distribuida'''

    def __init__(self, q=0, a=0, c=0, alfa=0):
        '''Carga puntual P.
        P: valor de la carga. Positivo hacia abajo.
        a: distancia entre el extremo izquierdo del tramo y el centro de la carga.
        c: longitud de la carga distribuida
        alfa: Angulo de carga (90= prependicular a la viga)'''
        Carga.__init__(self, 1)
        self.q = q
        self.a = a
        self.c = c
        self.alfa = alfa

    def __str__(self):
        return 'Carga distribuida\n   Valor= ' + str(self.q) + 'N/m' \
                                                               ', ' + '\n   Inicio= ' + str(
            self.a) + 'm' + '\n   Longitud= ' + str(self.l) + 'm'

    def Qf(self, L):
        '''Reacciones nodales equivalentes para una carga
        unifomemente distribuida.
        L: longitud de la viga'''
        q = self.q
        a = self.a
        qver = (math.sin(self.alfa * (math.pi) / 180)) * q
        qhor = (math.cos(self.alfa * (math.pi) / 180)) * q

        b = L - self.a
        c = self.c
        Ma = -((qver * (c ** 3)) / (12 * L ** 2)) * (L - (3 * b) + (12 * a * (b ** 2)) / (c ** 2))
        Mb = -((qver * (c ** 3)) / (12 * L ** 2)) * (L - (3 * a) + (12 * (a ** 2) * b) / (c ** 2))

        return np.array([
            [qhor * self.c / 2],
            [(qver * b * c / L) - ((Ma - Mb) / L)],
            [Ma],
            [qhor * self.c / 2],
            [(qver * a * c / L) + (Ma - Mb) / L],
            [Mb]
        ])

    # Fuerza cortante en una sección (viga sin apoyos)
    def FQ(self, x, L):
        '''Aporte a la fuerza cortante en una sección debido a la carga distribuida.
        x: posición de la sección considerada respecto al extremo izquierdo
        L: Longitud del tramo'''
        if self.a <= x < self.a + self.l:
            return -self.q * (x - self.a) * (math.sin(self.alfa * (math.pi) / 180))
        elif x <= L:
            return -self.q * self.l * (math.sin(self.alfa * (math.pi) / 180))
        else:
            return 0

    # Momento flector en una sección (viga simplemente apoyada)
    def MF(self, x, L):
        '''Aporte al momento flector en una sección debido a la carga distribuida.
        x: posición de la sección considerada respecto al extremo izquierdo
        L: Longitud del tramo'''
        V1 = (self.q * (math.sin(self.alfa * (math.pi) / 180))) * self.l / L * (L - self.a - self.l / 2)
        V2 = (self.q * (math.sin(self.alfa * (math.pi) / 180))) * self.l - V1
        if 0 <= x < self.a:
            return V1 * x
        elif x <= self.a + self.l:
            return V1 * x - 0.5 * self.q * (x - self.a) ** 2
        elif x <= L:
            return V2 * (L - x)
        else:
            return 0


class Puntos:
    '''puntos.
            obtenemos los lugares de los puntos de la matriz puntos de arriba
            Ahora definiremos su inclinacion y su rigidez'''

    def __init__(self, rigidez=0):
        '''Carga puntual P.
        rigidez: rigidez del punto (apoyado, empotrado libre, etc
        rigidez : 0 sin apoyo en el punto
        rigidez : 1 Apoyo simple, permite el giro y el desplazamiento horizontal
        rigidez : 2 Apoyo simple, permite el giro y el desplazamiento vertical
        rigidez : 3 Apoyo fijo, permite el giro
        rigidez : 4 Empotrado no permite movimiento
        '''
        self.rigidez = rigidez

        self.P = array(np.ones((3, 1)))
        if self.rigidez == 0:
            # Sin Apoyo
            # El valor 1 indica que es desplazable, el valor 0 indica indeplazable
            self.P[0] = 1
            self.P[1] = 1
            self.P[2] = 1
        elif self.rigidez == 1:
            # Apoyo simple, permite el giro y el desplazamiento horizontal
            # El valor 1 indica que es desplazable, el valor 0 indica indeplazable
            self.P[0] = 1
            self.P[1] = 0
            self.P[2] = 1
        elif self.rigidez == 2:
            # Apoyo simple, permite el giro y el desplazamiento vertical
            # El valor 1 indica que es desplazable, el valor 0 indica indeplazable
            self.P[0] = 0
            self.P[1] = 1
            self.P[2] = 1
        elif self.rigidez == 3:
            # Apoyo fijo, permite el giro
            # El valor 1 indica que es desplazable, el valor 0 indica indeplazable
            self.P[0] = 0
            self.P[1] = 0
            self.P[2] = 1
        elif self.rigidez == 4:
            # Empotrado no permite movimiento
            # El valor 1 indica que es desplazable, el valor 0 indica indeplazable
            self.P[0] = 0
            self.P[1] = 0
            self.P[2] = 0
        else:
            self.P[0] = 1
            self.P[1] = 1
            self.P[2] = 1