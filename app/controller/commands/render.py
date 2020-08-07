from app.controller.console import command
from app import app
import numpy as np

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
        if node.geom is None:
            node.geom = panda3d.loader.loadModel("data/geom/node")

        geom = node.geom
        geom.setTag('entity_type', type(node).__name__)
        geom.setTag('entity_id', node.entity_id)
        x, y, z = node.position
        geom.setPos(x, y, z)
        geom.reparentTo(panda3d.render)

    entities_dict = model_register.get("Bar", dict())
    for entity_id in entities_dict:
        bar = entities_dict[entity_id]
        # Si no hay una geometría asignada, la carga y la asgina a la entidad

        if bar.geom is None:
            bar.geom = panda3d.loader.loadModel("data/geom/beam")

        geom = bar.geom
        geom.setTag('entity_type', type(bar).__name__)
        geom.setTag('entity_id', bar.entity_id)

        # Ubica un cubo de 1x1x1 [m] en la posición inicial de la barra
        x0, y0, z0 = bar.start.position
        x1, y1, z1 = bar.end.position
        geom.setPos(x0, y0, z0)

        # Escalamos el cubo de forma que adquiera el largo de la barra, y las dimensiones de la sección
        b, h = bar.section.size
        x = x1-x0
        y = y1-y0
        z = z1-z0
        vector = [x, y, z]
        norm = np.linalg.norm(vector)
        geom.setScale(b, norm, h)
        geom.lookAt(bar.end.geom)
        geom.reparentTo(panda3d.render)
