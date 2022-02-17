from app.model import Node, Beam, Bar, Section
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute

# Creamos una variable global coredata que almacenará información sobre el modulo
from app.model.transaction import Transaction

coredata = dict()


@command(name="beam", shortcut="b")
def create_bar():
    global coredata
    # Agrega una tarea al TaskManager para dibujar la barra a crear

    print("create_beam")
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
    coredata["last_node"] = None
    coredata["end_node"] = None

    del man


def bar_task(task):
    # Establece coredata como variable global
    global coredata

    # Accede a la instancia base de la aplicación

    panda3d = app.get_show_base()

    watcher = panda3d.mouseWatcherNode
    box_input = app.console_input
    if coredata["start"] is not None and coredata["end"] is not None:
        # Una vez que se tiene un inicio y un fin creamos los nodos y la barra en el modelo
        x0, y0, z0 = coredata["start"]
        x1, y1, z1 = coredata["end"]

        tr = Transaction()
        tr.start("Create beam")

        if coredata["last_node"] is None:
            start_node = Node(x0, y0, z0)
        else:
            start_node = coredata["last_node"]

        if coredata["end_node"] is None:
            end_node = Node(x1, y1, z1)
        else:
            end_node = coredata["end_node"]

        section = Section(0.2, 0.3)
        bar = Bar(start_node, end_node, section)
        bar.behavior = "Viga"
        coredata["last_node"] = end_node

        # Se crea una nueva linea para dibujar
        coredata["start"] = coredata["end"]
        coredata["line"].setVertex(0, x1, y1, z1)
        coredata["end"] = None

        tr.commit()

        #execute("regen")

    if app.mouse_on_workspace:

        if watcher.isButtonDown("mouse1"):
            if coredata["start"] is None and not coredata["press"]:
                # Almacena el valor de inicio del segmento de linea

                selection = app.main_ui.status_bar.entity_info
                if isinstance(selection, Node):
                    coredata["start"] = selection.position
                    coredata["last_node"] = selection
                else:
                    coredata["start"] = app.work_plane_mouse
                coredata["press"] = True
                print("start")

                #print(coredata)
                create_line_seg(panda3d)

            elif coredata["end"] is None and not coredata["press"]:
                # Almacena el valor final del segmento de linea

                selection = app.main_ui.status_bar.entity_info
                if isinstance(selection, Node) and selection is not coredata["last_node"]:
                    coredata["end"] = selection.position
                    coredata["end_node"] = selection
                else:
                    x0, y0, z0 = coredata["start"]
                    x1, y1, z1 = app.work_plane_mouse
                    z1 = z0

                    coredata["end"] = x1, y1, z1

                #coredata["end"] = app.work_plane_mouse
                coredata["press"] = True
                print("end")
                #print(coredata)
        else:
            if coredata["press"]:
                # Resetea una variable que permite detectar el momento en que se empieza a presionar el mouse
                coredata["press"] = False

        if coredata["start"] is not None and coredata["line"] is not None:
            # Actualiza la posición final de la línea a la ubicación del cursor, dejando fijo el origen
            line = coredata["line"]
            x0, y0, z0 = coredata["start"]
            x1, y1, z1 = app.work_plane_mouse
            z1 = z0

            bar_vect = np.array([x1-x0, y1-y0, z1-z0])
            bar_len = np.linalg.norm(bar_vect)

            if box_input["focus"] is True:
                print("focused")
                input_len = box_input.get()
                if input_len is not "":
                    try:
                        input_len = float(input_len)
                    except Exception as ex:
                        input_len = 0
                else:
                    input_len = 0

                if input_len is None:
                    input_len = 0

                if bar_len is 0:
                    bar_len = 1
                bar_vect = input_len*(bar_vect/bar_len)
                x1, y1, z1 = coredata["start"]+bar_vect
            else:
                # Mostrar la longitud de la barra en pantalla
                box_input.enterText("{}".format(round(bar_len,2)))
            line.setVertex(1, x1, y1, z1)

    if watcher.has_mouse() and (watcher.isButtonDown("escape") or watcher.isButtonDown("mouse3")):
        # Detiene la creación de la linea y resetea las variables
        box_input.enterText("")
        coredata["start"] = None
        coredata["end"] = None
        coredata["press"] = False
        if coredata["line_node"] is not None:
            print(coredata["line_node"])
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

    print(coredata["start"])

    x0, y0, z0 = coredata["start"]
    x1, y1, z1 = app.work_plane_mouse
    z0 = z1

    line.setColor(1.0, 0.0, 0.0, 1.0)
    line.moveTo(x0, y0, z0)
    line.drawTo(x1, y1, z1)

    coredata["line"] = line

    node = line.create(dynamic=True)

    node_path = NodePath(node)
    node_path.reparentTo(panda3d.render)

    coredata["line_node"] = node_path

    return line, node
