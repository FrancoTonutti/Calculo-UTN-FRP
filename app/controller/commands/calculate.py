from kivy.app import App
from app.controller.console import command

import math
import numpy as np
from numpy import array
from numpy import matrix


@command(name="calcular", shortcut="c")
def start_analysis():
    print("----------------------------------------------------")
    print("start_analysis()")

    # Accede a la interfaz de kivy para obtener la información de panda3d
    app = App.get_running_app()
    panda3d = app.root.panda3D
    # Obtenemos el registro del modelo
    model_reg = panda3d.model_reg

    puntos = []
    areas = []
    inercias = []

    # Recorremos la lista de barras e imprimimos en consola las posiciones de inicio y fin de cada barra
    bar_list = model_reg.get("Bar", [])
    i = 1
    for bar in bar_list:
        print("Barra {}".format(i))
        start = bar.start.position[0], bar.start.position[1]
        end = bar.end.position[0], bar.end.position[1]
        if start not in puntos:
            puntos.append(start)
        if end not in puntos:
            puntos.append(end)

        b, h = bar.section.size
        areas.append([b*h])
        inercias.append([(b*h**3)/12])

        i += 1

    i = 1
    mcb = []
    for bar in bar_list:
        start = bar.start.position[0], bar.start.position[1]
        end = bar.end.position[0], bar.end.position[1]

        start_index = puntos.index(start)
        end_index = puntos.index(end)
        mcb.append([start_index, end_index])


    puntos = array(puntos)
    areas = array(areas)
    inercias = array(inercias)
    mcb = array(mcb)
    print(mcb)
    # Elasticidad una sola prefijada
    elasticidad = 1007
    print(mcb)

    R = MatizGlobalEnsambalda(puntos, areas, inercias, elasticidad, mcb)
    print(R)
    print("----------------------------------------------------")

    return None


# Funciones prefijadas
def MatrizLocal(L, A, I, E):
    R1 = (E * A / L, 0, 0, -E * A / L, 0, 0)
    R2 = (0, 12 * E * I / L ** 3, 6 * E * I / L ** 2, 0, -12 * E * I / L ** 3, 6 * E * I / L ** 2)
    R3 = (0, 6 * E * I / L ** 2, 4 * E * I / L, 0, -6 * E * I / L ** 2, 2 * E * I / L)
    R4 = (-E * A / L, 0, 0, +E * A / L, 0, 0)
    R5 = (0, -12 * E * I / L ** 3, -6 * E * I / L ** 2, 0, 12 * E * I / L ** 3, -6 * E * I / L ** 2)
    R6 = (0, 6 * E * I / L ** 2, 2 * E * I / L, 0, -6 * E * I / L ** 2, 4 * E * I / L)
    M = np.array([[R1], [R2], [R3], [R4], [R5], [R6]])
    M = matrix(M)
    return M


def Matriztrans(ang):
    R1 = (math.cos(ang), -math.sin(ang), 0, 0, 0, 0)
    R2 = (math.sin(ang), math.cos(ang), 0, 0, 0, 0)
    R3 = (0, 0, 1, 0, 0, 0)
    R4 = (0, 0, 0, math.cos(ang), -math.sin(ang), 0)
    R5 = (0, 0, 0, math.sin(ang), math.cos(ang), 0)
    R6 = (0, 0, 0, 0, 0, 1)
    M = np.array([[R1], [R2], [R3], [R4], [R5], [R6]])
    M = matrix(M)
    return M


def MatrizGlobal(local, transformacion):
    T = np.transpose(transformacion)
    A = T.dot(local)
    E = A.dot(transformacion)
    return E


def Matrizconectividad(CB):
    TC = np.zeros((CB.shape[0], 6))
    for i in range(0, CB.shape[0]):
        for j in range(0, 3):
            if CB[i][0] == 0:
                TC[i][j] = int(j)
            else:
                TC[i][j] = int(j + 3 * (CB[i][0]))
        for j in range(3, 6):
            if CB[i][1] == 0:
                TC[i][j] = int(j - 3)
            else:
                TC[i][j] = int((j - 3) + 3 * (CB[i][1]))
    A = array(TC, dtype=int)
    return A


"""
# Puntos no se desarrolla, se hara con extraccion de la grafica, lo mismo con areas e inercia, buscar la forma de obtenerla mediante el grafico o tablas
Puntos = array([[0, 0], [0, 10], [5, 7], [8, 0]])
Areas = array(([[1], [2], [3], [4]]))
Inercias = array(([[10], [20], [30], [40]]))
# Elasticidad una sola prefijada
Elasticidad = 1007
# Matriz de conectividad de baras (fila 1=barra 1, pos 1: Punto a, pos 2: Punto B)
MCB = array(([[0, 1], [1, 2], [2, 3], [0, 2]]))
print(MCB)
# Matriz de conectividad
TC = Matrizconectividad(MCB)
print(TC)
"""


def MatizGlobalEnsambalda(P, A, I, E, CB):
    # calculo de distancias considerando una sola barra entre 2 nudos y nudos sucecivos (bara1 va de 1 a 2, barra 2, de 2 a 3)
    H = np.ones((A.shape[0], P.shape[1]))
    for i in range(0, P.shape[0] - 1):
        H[i][0] = P[CB[i][1]][0] - P[CB[i][0]][0]
        H[i][1] = P[CB[i][1]][1] - P[CB[i][0]][1]
    # Calculos de longitudes de barras
    D = np.ones((A.shape[0], 1))
    for i in range(0, P.shape[0] - 1):
        D[i] = math.sqrt(H[i][0] ** 2 + H[i][1] ** 2)
    # calculo de pendientes y angulos
    pen = np.ones((A.shape[0], 1))
    for i in range(0, P.shape[0] - 1):
        if H[i][0] == 0:
            pen[i] = 9999999999999999999999
        else:
            pen[i] = H[i][1] / H[i][0]
    # Calculo de angulos
    ang = np.ones((A.shape[0], 1))
    for i in range(0, P.shape[0] - 1):
        ang[i] = np.arctan(pen[i])
    # Calculo de matrices de rigidez local
    K = np.ones((A.shape[0], 6, 6))
    for i in range(0, A.shape[0]):
        K[i] = MatrizLocal(D[i], A[i], I[i], E)
    # Calculo de matrices de transformacion
    T = np.ones((A.shape[0], 6, 6))
    for i in range(0, P.shape[0] - 1):
        T[i] = Matriztrans(ang[i])
    # Calculo de matriz de global por barra
    G = np.ones((A.shape[0], 6, 6))
    for i in range(0, A.shape[0]):
        G[i] = MatrizGlobal(K[i], T[i])
    # Matriz de conectividad
    TC = Matrizconectividad(CB)
    # Ensamble de matriz Global de la estructura
    KG = np.zeros((P.shape[0] * 3, P.shape[0] * 3))
    Kiel = np.zeros((6, 6))
    for iel in range(0, A.shape[0]):
        Kiel = G[iel]
        for i in range(0, 6):
            for j in range(0, 6):
                KG[TC[iel][i]][TC[iel][j]] = KG[TC[iel][i]][TC[iel][j]] + Kiel[i][j]
    return KG
