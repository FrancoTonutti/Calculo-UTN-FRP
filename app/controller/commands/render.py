from app.controller.console import command
from app import app
import numpy as np
from panda3d.core import LineSegs, NodePath
from app.view import draw

wireframe = False


@command("regen")
def regen():
    print("regen")
    # Accede a la interfaz de kivy para obtener la información de panda3d
    panda3d = app.get_show_base()
    # Obtenemos el registro del modelo
    model_register = app.model_reg
    print(model_register)
    print(model_register.get("Node", dict()).items())
    print("-----t----")
    # Recorre todos los nodos del modelo y coloca una esfera en el punto correspondiente
    entities_dict = model_register.get("Node", dict())
    for entity_id in entities_dict:
        node = entities_dict[entity_id]
        # Si no hay una geometría asignada, la carga y la asgina a la entidad

        ux, uz, ry = node.get_restrictions2d()
        if node.geom is None:
            node.geom = [None]

        if ry is False:
            if "node_box" in str(node.geom[0]):
                node.geom[0].removeNode()
                node.geom[0] = None

            if node.geom[0] is None:
                node.geom[0] = panda3d.loader.loadModel("data/geom/node")
        else:
            if "node_box" not in str(node.geom[0]):
                node.geom[0].removeNode()
                node.geom[0] = None

            if node.geom[0] is None:
                node.geom[0] = panda3d.loader.loadModel("data/geom/node_box")

        geom1 = node.geom[0]

        geom1.setTag('entity_type', type(node).__name__)
        geom1.setTag('entity_id', node.entity_id)
        x, y, z = node.position
        geom1.setPos(x, y, z)
        geom1.reparentTo(panda3d.render)

        geom2 = None

        if ux + uz == 0 and len(node.geom) is 2:
            geom2 = node.geom.pop()
            geom2.removeNode()
            geom2 = None

        if ux + uz == 1:
            if len(node.geom) is 1:
                geom2 = panda3d.loader.loadModel("data/geom/support_roller_x")
                node.geom.append(geom2)
            else:
                geom2 = node.geom[1]
                if "support_roller_x" not in str(geom2):
                    geom2.removeNode()
                    node.geom[1] = panda3d.loader.loadModel("data/geom/support_roller_x")
                    geom2 = node.geom[1]

            if uz is True:
                geom1.setR(0)
            else:
                geom1.setR(90)

        if ux is True and uz is True:
            geom1.setR(0)
            if len(node.geom) is 1:
                geom2 = panda3d.loader.loadModel("data/geom/support_pinned_x")
                node.geom.append(geom2)
            else:
                geom2 = node.geom[1]
                if "support_pinned_x" not in str(geom2):
                    geom2.removeNode()
                    node.geom[1] = panda3d.loader.loadModel("data/geom/support_pinned_x")
                    geom2 = node.geom[1]

        if geom2 is not None:
            geom2.setTag('entity_type', type(node).__name__)
            geom2.setTag('entity_id', node.entity_id)
            geom2.reparentTo(geom1)
            geom2.setPos(0, 0, -0.2)
            geom2.setScale(0.20, 0.20, 0.20)

    entities_dict = model_register.get("Bar", dict())
    for entity_id in entities_dict:
        bar = entities_dict[entity_id]
        # Si no hay una geometría asignada, la carga y la asgina a la entidad

        if bar.geom is None:
            bar.geom = []
            bar.geom.append(panda3d.loader.loadModel("data/geom/beam"))
        else:
            geom = bar.geom[0]
            if "data/geom/beam" not in str(geom):
                geom.removeNode()
                bar.geom[0] = panda3d.loader.loadModel("data/geom/beam")

        geom = bar.geom[0]
        geom.setTag('entity_type', type(bar).__name__)
        geom.setTag('entity_id', bar.entity_id)

        # Ubica un cubo de 1x1x1 [m] en la posición inicial de la barra
        x0, y0, z0 = bar.start.position
        x1, y1, z1 = bar.end.position
        geom.setPos(x0, y0, z0)

        # Escalamos el cubo de forma que adquiera el largo de la barra, y las dimensiones de la sección
        b, h = bar.section.size
        x = x1 - x0
        y = y1 - y0
        z = z1 - z0
        vector = [x, y, z]
        norm = np.linalg.norm(vector)
        geom.setScale(b, norm, h)
        geom.lookAt(bar.end.geom[0])
        geom.reparentTo(panda3d.render)

        if wireframe is True:
            geom.hide()
            geom.setScale(0.1, norm, 0.1)
            if len(bar.geom) is 1:
                line = draw.draw_line_3d(x0, y0, z0, x1, y1, z1, 3, "C_BLUE")

                line.setDepthOffset(1)
                bar.geom.append(line)
            else:
                line = bar.geom[1]
                if line is not None:
                    line.removeNode()
                line = draw.draw_line_3d(x0, y0, z0, x1, y1, z1, 3, "C_BLUE")

                line.setDepthOffset(1)
                bar.geom[1] = line
            print("!!!!!!!!!!!!!!!!!!!!!!line")
            print(line)
            #line.setLight(panda3d.plight_node)

        else:
            if len(bar.geom) > 1:
                line = bar.geom[1]
                if line is not None:
                    line.removeNode()
                    bar.geom[1] = None
