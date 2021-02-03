
from app import app
from app.controller.console import command
from app.controller.commands.Tomas import calculo

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Imports only for IDE type hints
    from app.view.interface.console_ui import ConsoleUI
    from app.model import *


import math
import numpy as np
from numpy import array
from numpy import matrix


@command(name="calcular", shortcut="c")
def start_analysis():
    print("----------------------------------------------------")
    print("start_analysis()")

    # Accede a la interfaz de kivy para obtener la información de panda3d

    panda3d = app.get_show_base()
    # Obtenemos el registro del modelo
    model_reg = app.model_reg


    areas = []
    inercias = []
    node_list = []


    # Recorremos la lista de barras e imprimimos en consola las posiciones de inicio y fin de cada barra
    print("model_reg", model_reg)

    Barras = []
    for bar in model_reg.get_bars():
        #print("Barra {}".format(i))
        print(bar)

        start = bar.start.position[0], bar.start.position[1]
        end = bar.end.position[0], bar.end.position[1]

        if bar.start not in node_list:
            node_list.append(bar.start)
        if bar.end not in node_list:
            node_list.append(bar.end)

        elastic_modulus = bar.material.elastic_modulus
        inertia_x = bar.section.inertia_x()
        area = bar.section.area()

        inercias.append(inertia_x)
        areas.append(area)

        Barras.append(calculo.Viga(elastic_modulus, inertia_x, area, start, end))

    b = len(Barras)
    puntos = np.ones((b * 2, 2))

    m = 0
    for i in range(0, b):
        puntos[m, 0] = Barras[i].a[0]
        puntos[m, 1] = Barras[i].a[1]
        puntos[m + 1, 0] = Barras[i].b[0]
        puntos[m + 1, 1] = Barras[i].b[1]
        m = m + 2

    # Lista "PUNTOS" es un valor cpor cada punto y el numero de adentro define su posibilidad de desplazamientos
    PUNTOS = []

    point: Node
    for point in node_list:
        restrictions = point.get_restrictions2d()

        new_point = calculo.Puntos(0)
        new_point.P = list(map(lambda x: not x, restrictions))

        PUNTOS.append(new_point)

    Rest = calculo.resticciones(PUNTOS)

    Con = np.zeros((b * 2, 1))
    Con[0] = 0
    Con[1] = 1

    for i in range(2, b * 2):
        for n in range(0, i):
            if puntos[i, 0] == puntos[n, 0] and puntos[i, 1] == puntos[n, 1]:
                Con[i] = Con[n]
        if Con[i] == 0:
            Con[i] = max(Con) + 1

    print("Con=", Con)

    # se Crea una matriz que contenga en forma ordenada el orden de puntos y las barras que llegan a los mismos
    # es deci la barra esta representada por renglones. el renglon uno representa a la barra uno
    # la barra uno va del punto que se encuentra en la primera columna al punto de la segunda columna
    matrizconectividad = np.ones((b, 2))
    d = 0
    for i in range(0, b):
        matrizconectividad[i, 0] = Con[d]
        matrizconectividad[i, 1] = Con[d + 1]
        d = d + 2

    print("Vector de puntos=", matrizconectividad)

    MC = calculo.Matrizconectividad(matrizconectividad)

    print("matriz conectividad=", MC)

    # Matriz de conectividad de baras (fila 1=barra 1, pos 1: Punto a, pos 2: Punto B)

    MG = calculo.MatrizGlobalEnsambalda(Barras, matrizconectividad)

    #print("Matriz Global=", MG)
