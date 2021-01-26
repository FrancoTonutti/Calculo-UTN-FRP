from app import app
from app.controller.console import command
from app.model import Diagram
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

        # Guardamos la matriz transpuesta para futuros calculos
        bar_element.set_analysis_results("m_transform_t", m_transform_t)

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

        # Matriz de rigidez local

        k_l = np.block([[k_aa_l, k_ab_l],
                        [k_ba_l, k_bb_l]])

        # Guardamos la matriz de rigideces local para futuros calculos

        bar_element.set_analysis_results("K_l", k_l)

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

        bar_element.set_analysis_results("load_x", load_x)
        bar_element.set_analysis_results("load_y", load_y)

        v_forces_a_l = np.array([[fx],
                                 [fy],
                                 [moment]])

        v_forces_b_l = np.array([[fx],
                                 [fy],
                                 [-moment]])

        print("save fb_l")
        print(v_forces_a_l)
        print(v_forces_b_l)
        fb_l = np.concatenate([v_forces_a_l, v_forces_b_l])
        print(fb_l)
        bar_element.set_analysis_results("fb_l", fb_l)
        print(bar_element.get_analysis_results("fb_l"))
        print("end save")




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

    # Buscamos las columnas de ceros para borrarlas
    to_delete_0 = np.argwhere(np.all(m_global_system_reduced[..., :] == 0, axis=0))

    # Elimianamos filas y columnas restringidas por los vinculos
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
        # Realizamos el calculo de desplazamientos nudos
        m_global_system_invert = np.linalg.inv(m_global_system_reduced)
        v_f = v_global_fe_reduced - v_global_fb_reduced
        v_desp = np.matmul(m_global_system_invert, v_f)

        # Convierto el vector de desplazamientos reducido al vector de desplazamietos globales
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

        # Almaceno los desplazamientos globales de cada nudo
        for ref, desp in zip(v_global_references, v_global_desp):

            d_g = ref["node"].get_analysis_results("d_g")

            if d_g is None:
                d_g = [0, 0, 0]

            d_g[ref["pos"]] = desp
            ref["node"].set_analysis_results("d_g", d_g)

        # Procedo al calculo de esfuerzos en extremos de barra
        bar_element: Bar
        for bar_element in model.get_bars():
            print("Caluclo de esfuerzos")

            # Obtenemos la matriz de rigidez local de la barra, calculada previamente
            k_l = bar_element.get_analysis_results("K_l")
            print("k_l")
            print(k_l)

            # obtenemos el vector de fuerzas en extremo de barra, en sistema local
            fb_l = bar_element.get_analysis_results("fb_l")
            print("fb_l")
            print(fb_l)
            # Obtenenmos los desplazamientos globales de los nudos

            d_a_g = bar_element.start.get_analysis_results("d_g")
            d_b_g = bar_element.end.get_analysis_results("d_g")

            # Obtenenmos la matriz de transformación transpuesta de la barra

            m_transform_t = bar_element.get_analysis_results("m_transform_t")

            # Determinamos los desplazamientos de nudos en el sistema local

            d_a_l = np.matmul(m_transform_t, d_a_g)
            d_b_l = np.matmul(m_transform_t, d_b_g)
            d_l = np.concatenate([d_a_l, d_b_l])
            # d_l = np.transpose(d_l)

            print("d_l")
            print(d_l)

            # Determinamos las fuerzas en extremo de barra en sistema local

            f = np.matmul(k_l, d_l) + fb_l
            bar_element.set_analysis_results("f_l", f)

            print("Esfueros en barra {}-{}".format(bar_element.start.index, bar_element.end.index))
            print(f)

            # Detrminacion de esfuerzos internos en distintos puntos de la barra

            step = 0.25
            load_x = bar_element.get_analysis_results("load_x")
            load_y = bar_element.get_analysis_results("load_y")

            print("load_x {}".format(load_x))
            print("load_y {}".format(load_y))
            long = bar_element.longitude()

            shear = lambda x: f[1, 0] - load_y * x
            normal = lambda x: f[0, 0] - load_x * x
            moment = lambda x: f[2, 0] - f[1, 0] * x + load_y * x * x / 2

            v_shear = [shear(0.00*long),
                       shear(0.25*long),
                       shear(0.50*long),
                       shear(0.75*long),
                       shear(1.00*long)]

            v_normal = [normal(0.00 * long),
                        normal(0.25 * long),
                        normal(0.50 * long),
                        normal(0.75 * long),
                        normal(1.00 * long)]

            v_moment = [moment(0 * long),
                        moment(0.25 * long),
                        moment(0.50 * long),
                        moment(0.75 * long),
                        moment(1.00 * long)]

            v_x_coord = [.00 * long,
                         0.25 * long,
                         0.50 * long,
                         0.75 * long,
                         1.00 * long]

            v_shear = np.column_stack([v_x_coord, v_shear])
            v_normal = np.column_stack([v_x_coord, v_normal])
            v_moment = np.column_stack([v_x_coord, v_moment])

            bar_element.set_analysis_results("v_shear", v_shear)
            bar_element.set_analysis_results("v_normal", v_normal)
            bar_element.set_analysis_results("v_moment", v_moment)

            Diagram(bar_element, v_moment)


    else:
        print("Matriz singular, vinculos insuficientes: mecanismo")







