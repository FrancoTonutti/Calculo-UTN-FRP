
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


@command(name="matricial", shortcut="c")
def start_analysis():
    print("----------------------------------------------------")
    print("start_analysis()")

    # Obtenemos el registro del modelo
    model = app.model_reg

    # Creamos la matriz del sitema global

    total_nodes = model.get_node_count()

    m_global_system = np.zeros((total_nodes * 3, total_nodes * 3))
    v_global_fb = np.zeros((total_nodes * 3, 1))
    v_global_fe = np.zeros((total_nodes * 3, 1))

    v_global_references = []
    i = 0
    node_element: Node
    for node_element in model.get_nodes():
        node_element.index = i
        v_global_references.append({"index": i, "node": node_element, "pos": 0, "name": "x"})
        v_global_references.append({"index": i, "node": node_element, "pos": 1, "name": "y"})
        v_global_references.append({"index": i, "node": node_element, "pos": 2, "name": "r"})

        # Vector de fuerzas en extremos de barra por cargas en barras, en coordeandas locales

        load_y = 0
        load_x = 0

        for puntual_load in node_element.get_loads():
            load_angle = np.deg2rad(puntual_load.angle)
            load_y += puntual_load.value * np.cos(load_angle)
            load_x = puntual_load.value * np.sin(load_angle)

        v_forces_ext = np.array([[load_x],
                                 [load_y],
                                 [0]])

        # m_global_system[fila_inicial:fila_final, columna_inicial:columna_final]
        v_global_fe[i:i + 3, :] += v_forces_ext

        i += 1

    v_global_references = np.array(v_global_references)



    bar_element: Bar
    for bar_element in model.get_bars():

        start = bar_element.start.position[0], bar_element.start.position[1]
        end = bar_element.end.position[0], bar_element.end.position[1]

        # Creamos la matriz de transformación para estructuras de plano medio

        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]

        angle = np.arctan(delta_y / delta_x)

        s = np.sin(angle)
        c = np.cos(angle)

        m_transform = np.array([[c, -s, 0],
                                [s,  c, 0],
                                [0,  0, 1]])

        m_transform_t = np.transpose(m_transform)

        # Procedemos a definir terminos para las submatrices de rigidez

        e = bar_element.material.elastic_modulus
        a = bar_element.section.area()
        long = np.linalg.norm([delta_x, delta_y])
        inertia = bar_element.section.inertia_x()

        c2 = c**2
        s2 = s**2

        ea_l = e*a/long
        ei_l3 = 12*e*inertia/long**3
        ei_l2 = 6*e*inertia/long**2
        ei_l = 4*e*inertia/long

        # Submatrices de rigidez locales

        k_aa_l = np.array([[ea_l,     0,     0],
                           [   0, ei_l3, ei_l2],
                           [   0, ei_l2,  ei_l]])

        k_ab_l = np.array([[-ea_l,      0,      0],
                           [    0, -ei_l3,  ei_l2],
                           [    0, -ei_l2, ei_l/2]])

        k_ba_l = np.array([[-ea_l,      0,      0],
                           [    0, -ei_l3, -ei_l2],
                           [    0,  ei_l2, ei_l/2]])

        k_bb_l = np.array([[ea_l,      0,      0],
                           [   0,  ei_l3, -ei_l2],
                           [   0, -ei_l2,  ei_l]])

        # Submatrices de rigidez globales

        """
        k_aa_l = np.array([[c2*ea_l + s2*ei_l3,   s*c*(ea_l-ei_l3), -s*ei_l2],
                           [  s*c*(ea_l-ei_l3),   s2*ea_l-c2*ei_l3,  c*ei_l2],
                           [          -s*ei_l2,            c*ei_l2,    ei_l]])

        k_ab_l = np.array([[-c2*ea_l - s2*ei_l3, -s*c*(ea_l-ei_l3), -s*ei_l2],
                           [  -s*c*(ea_l-ei_l3), -s2*ea_l-c2*ei_l3,  c*ei_l2],
                           [           s*ei_l2,          -c*ei_l2,   ei_l/2]])

        k_ba_l = np.array([[-c2*ea_l - s2*ei_l3, -s*c*(ea_l-ei_l3),  s*ei_l2],
                           [  -s*c*(ea_l-ei_l3), -s2*ea_l-c2*ei_l3, -c*ei_l2],
                           [           -s*ei_l2,           c*ei_l2,   ei_l/2]])

        k_bb_l = np.array([[c2*ea_l + s2*ei_l3,   s*c*(ea_l-ei_l3),  s*ei_l2],
                           [  s*c*(ea_l-ei_l3),   s2*ea_l-c2*ei_l3, -c*ei_l2],
                           [           s*ei_l2,           -c*ei_l2,     ei_l]])

        """

        k_aa_g = np.matmul(np.matmul(m_transform, k_aa_l), m_transform_t)
        k_ab_g = np.matmul(np.matmul(m_transform, k_ab_l), m_transform_t)
        k_ba_g = np.matmul(np.matmul(m_transform, k_ba_l), m_transform_t)
        k_bb_g = np.matmul(np.matmul(m_transform, k_bb_l), m_transform_t)

        # Matriz de rigidez globales

        k_g = np.block([[k_aa_g, k_ab_g],
                        [k_ba_g, k_bb_g]])

        # Ensablamos las submatrices en la matriz del sitema global

        index_a = bar_element.start.index * 3
        index_b = bar_element.end.index * 3

        # m_global_system[fila_inicial:fila_final, columna_inicial:columna_final]
        m_global_system[index_a:index_a + 3, index_a:index_a + 3] += k_aa_g
        m_global_system[index_a:index_a + 3, index_b:index_b + 3] += k_ab_g
        m_global_system[index_b:index_b + 3, index_a:index_a + 3] += k_ba_g
        m_global_system[index_b:index_b + 3, index_b:index_b + 3] += k_bb_g

        # Vector de fuerzas en extremos de barra por cargas en barras, en coordeandas locales

        load_y = 0
        load_x = 0

        for distributed_load in bar_element.get_loads():

            load_angle = np.deg2rad(distributed_load.angle) - angle
            load_y += distributed_load.value * np.sin(load_angle)
            load_x += distributed_load.value * np.cos(load_angle)

            print("Carga encontrada de {} con {}º".format(distributed_load.value, distributed_load.angle))
            print("load_angle {}º".format(load_angle))
            print("load_y {}".format(load_y))
            print("load_x {}".format(load_x))

        fx = load_x * long / 2
        fy = load_y * long / 2
        moment = load_y * long**2/12

        v_forces_a_l = np.array([[fx],
                                 [fy],
                                 [moment]])

        v_forces_b_l = np.array([[fx],
                                 [fy],
                                 [moment]])
        print("v_forces_a_l {}".format(v_forces_a_l))

        # Vector de fuerzas en extremos de barra por cargas en barras, en coordeandas globales

        v_forces_a_g = np.matmul(m_transform, v_forces_a_l)
        v_forces_b_g = np.matmul(m_transform, v_forces_b_l)

        print("v_forces_a_g {}".format(v_forces_a_g))

        # m_global_system[fila_inicial:fila_final, columna_inicial:columna_final]
        v_global_fb[index_a:index_a + 3, :] += v_forces_a_g
        v_global_fb[index_b:index_b + 3, :] += v_forces_b_g

    #np.set_printoptions(precision=3)
    #np.set_printoptions(suppress=True)

    print(m_global_system)
    print(v_global_fb)

    m_global_system_reduced = m_global_system.copy()

    node_element: Node
    for node_element in model.get_nodes():
        node_index = node_element.index*3

        # Obtenemos las restricciones de vinculos
        restrictions = node_element.get_restrictions2d()

        i = 0


        for restriction in restrictions:
            if restriction:
                # Reemplazamos por ceros las filas y columnas con desplazamientos restringidos por vinculos
                m_global_system_reduced[::, node_index + i] = 0
                m_global_system_reduced[node_index + i, ::] = 0

                #v_global_fb[node_index + i, ::] = 0
                ##v_global_fe[node_index + i, ::] = 0
                #v_global_references[node_index + i] = 0
            i += 1

    to_delete_0 = np.argwhere(np.all(m_global_system_reduced[..., :] == 0, axis=0))

    m_global_system_reduced = np.delete(m_global_system_reduced, to_delete_0, axis=1)
    m_global_system_reduced = np.delete(m_global_system_reduced, to_delete_0, axis=0)
    v_global_fb_reduced = np.delete(v_global_fb, to_delete_0, axis=0)
    v_global_fe_reduced = np.delete(v_global_fe, to_delete_0, axis=0)
    v_global_references_reduced = np.delete(v_global_references, to_delete_0, axis=0)

    det = np.linalg.det(m_global_system_reduced)

    print(m_global_system_reduced)
    print(det)
    print(v_global_fb_reduced)

    if det != 0:
        m_global_system_invert = np.linalg.inv(m_global_system_reduced)

        v_f = v_global_fe_reduced - v_global_fb_reduced

        v_desp = np.matmul(m_global_system_invert, v_f)

        v_global_desp = np.zeros((total_nodes * 3, 1))

        for (desp, ref) in zip(v_desp, v_global_references_reduced):
            v_global_desp[ ref.get("index")*3 + ref.get("pos"), 0] = desp

        print("Calculo de desplazamientos realizado")
        print(v_global_references_reduced)
        print(v_desp)

        # Calculo de reacciones
        v_reactions = np.matmul(m_global_system, v_global_desp) + v_global_fb

        print("Reacciones de vinculos")
        print(np.matmul(m_global_system, v_global_desp))
        print(v_global_fb)

        print(v_reactions)

    else:
        print("Matriz singular, vinculos insuficientes: mecanismo")







