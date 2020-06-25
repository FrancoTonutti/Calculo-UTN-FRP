from app.model.core import Node, Bar
from direct.task.Task import TaskManager
from kivy.app import App

from panda3d.core import LineSegs, NodePath

# Creamos una variable global coredata que almacenará información sobre el modulo

coredata = dict()


def create_bar():
    global coredata
    # Agrega una tarea al TaskManager para dibujar la barra a crear

    print("create_bar")
    man = TaskManager()
    if not man.hasTaskNamed("create_bar"):
        man.add(bar_task, "create_bar")
    else:
        if coredata["line_node"] is not None:
            coredata["line_node"].removeNode()

    coredata["start"] = None
    coredata["end"] = None
    coredata["press"] = False
    coredata["line"] = None
    coredata["line_node"] = None

    del man


def bar_task(task):
    # Establece coredata como variable global
    global coredata

    # Accede a la interfaz de kivy para obtener la información de panda3d
    app = App.get_running_app()
    panda3d = app.root.panda3D

    watcher = panda3d.mouseWatcherNode

    if coredata["start"] is not None and coredata["end"] is not None:
        # Una vez que se tiene un inicio y un fin creamos los nodos y la barra en el modelo
        x0, y0, z0 = coredata["start"]
        x1, y1, z1 = coredata["end"]

        start_node = Node(x0, y0, z0)
        end_node = Node(x1, y1, z1)
        Bar(start_node, end_node)

        # Se crea una nueva linea para dibujar
        coredata["start"] = coredata["end"]
        create_line_seg(panda3d)
        coredata["end"] = None

    if panda3d.mouse_on_workspace:

        if watcher.isButtonDown("mouse1"):
            if coredata["start"] is None and not coredata["press"]:
                # Almacena el valor de inicio del segmento de linea
                coredata["start"] = panda3d.work_plane_mouse
                coredata["press"] = True
                print(coredata)
                create_line_seg(panda3d)

            elif coredata["end"] is None and not coredata["press"]:
                # Almacena el valor final del segmento de linea
                coredata["end"] = panda3d.work_plane_mouse
                coredata["press"] = True
                print(coredata)
        else:
            if coredata["press"]:
                # Resetea una variable que permite detectar el momento en que se empieza a presionar el mouse
                coredata["press"] = False

        if coredata["start"] is not None and coredata["line"] is not None:
            # Actualiza la posición final de la línea a la ubicación del cursor, dejando dijo el origen
            line = coredata["line"]
            x1, y1, z1 = panda3d.work_plane_mouse
            line.setVertex(1, x1, y1, z1)

    if watcher.has_mouse() and watcher.isButtonDown("escape"):
        # Detiene la cración de la linea y resetea las variables

        coredata["start"] = None
        coredata["end"] = None
        coredata["press"] = False
        if coredata["line_node"] is not None:
            coredata["line_node"].removeNode()

        man = TaskManager()
        man.remove("create_bar")
        del man




    return task.cont


def create_line_seg(panda3d):
    print("Draw LineSeg")
    line = LineSegs()
    print(LineSegs)
    line.setThickness(4)

    x0, y0, z0 = coredata["start"]
    x1, y1, z1 = panda3d.work_plane_mouse

    line.setColor(1.0, 0.0, 0.0, 1.0)
    line.moveTo(x0, y0, z0)
    line.drawTo(x1, y1, z1)

    coredata["line"] = line

    node = line.create(dynamic=True)

    np = NodePath(node)
    np.reparentTo(panda3d.render)

    coredata["line_node"] = np

    return line, node
