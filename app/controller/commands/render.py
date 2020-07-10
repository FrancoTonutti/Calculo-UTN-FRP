from app.controller.console import command
from kivy.app import App
import numpy as np

@command("regen")
def regen():
    print("regen")
    # Accede a la interfaz de kivy para obtener la información de panda3d
    app = App.get_running_app()
    panda3d = app.root.panda3D
    # Obtenemos el registro del modelo
    model_register = panda3d.model_reg

    # Recorre todos los nodos del modelo y coloca una esfera en el punto correspondiente
    for node in model_register.get("Node", []):
        # Si no hay una geometría asignada, la carga y la asgina a la entidad
        if node.geom is None:
            node.geom = panda3d.loader.loadModel("data/geom/node")

        geom = node.geom
        x, y, z = node.position
        geom.setPos(x, y, z)
        geom.reparentTo(panda3d.render)

    for bar in model_register.get("Bar", []):
        # Si no hay una geometría asignada, la carga y la asgina a la entidad
        if bar.geom is None:
            bar.geom = panda3d.loader.loadModel("data/geom/beam")

        geom = bar.geom
        geom.setTag('entity_id', bar.id)

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
        geom.setScale(norm, b, h)

        # Orientamos la geometría para que se oriente hacia el punto final
        angle_xz = np.arctan(z/x)*(180/np.pi)
        if x < 0:
            angle_xz = angle_xz+180

        angle_yz = np.arctan(y / x) * (180 / np.pi)
        if y < 0:
            angle_xz = angle_yz + 180

        geom.setHpr(0, -angle_yz, -angle_xz)
        geom.reparentTo(panda3d.render)



