from panda3d.core import Point3, OrthographicLens, PerspectiveLens, PointLight, AmbientLight, CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionRay, GeomNode
import math
import os
"""if os.name == 'nt':
    # Importar solo en windows
    import win32api
    import win32con"""


class CameraControl:
    def __init__(self, panda3d):
        # Inicialización de variables
        self.winsize = [0, 0]
        self.panda3d = panda3d
        self.panda3d.mouse_on_workspace = False

        # Desabilita el comportamiento por defecto de la camara
        self.panda3d.disable_mouse()

        # Llama a la función self.window_rezise_event cuando la ventana cambia de tamaño
        self.panda3d.accept('window-event', self.window_rezise_event)

        # Creamos el punto donde se centrará la cámara
        target_pos = Point3(0., 0., 0.)

        self.panda3d.cam_target = self.panda3d.render.attach_new_node("camera_target")
        self.panda3d.cam_target.set_pos(target_pos)
        self.panda3d.camera.reparent_to(self.panda3d.cam_target)
        self.panda3d.camera.set_y(-50.)
        
        # Definimos la cambinación de teclas para el control de la camara
        self.camera_active = False

        self.orbit_mouse_btn = "mouse2"
        self.orbit_keyboard_btn = "shift"
        self.orbit_mouse_reference = None
        self.orbit_camera_reference = None

        self.pan_mouse_btn = "mouse2"
        self.pan_keyboard_btn = "mouse2"
        self.pan_mouse_reference = None
        self.pan_camera_reference = None

        self.zoom_mouse_btn = "mouse2"
        self.zoom_keyboard_btn = "control"
        self.zoom_mouse_reference = None
        self.zoom_camera_reference = None

        # Establecemos los valores máximos y minimos para el zoom
        
        self.max_zoom = 10
        self.min_zoom = 0.1
        
        # Creamos la tarea de control de la camara
        self.panda3d.task_mgr.add(self.camera_control_task, "camera_control")

        # El movimiento de la rueda del mouse controla el zoom
        self.panda3d.accept("wheel_up", self.zoom_in)
        self.panda3d.accept("wheel_down", self.zoom_out)

        # Una fución de prueba para comprobar la posición del mouse en el modelo 3d
        self.panda3d.accept("mouse1", self.entity_select)

        # Se establece la lente ortografica en lugar de la perspectiva
        self.lens_type = "OrthographicLens"
        self.set_lens(self.lens_type)

        # Agrega un indicador de ejes en la esquina inferior izquierda
        self.show_view_cube()

        # Agregamos una luz puntual en la ubicación de la camara
        plight = PointLight("camera_light")
        plight.setColor((1, 1, 1, 1))
        plight.setAttenuation((1, 0, 0))
        print("getMaxDistance {}".format(plight.getMaxDistance()))
        self.panda3d.plight_node = self.panda3d.render.attach_new_node(plight)
        self.panda3d.plight_node.setPos(0, -50, 0)
        self.panda3d.render.setLight(self.panda3d.plight_node)

        # Agregamos luz ambiental que disminuya las zonas oscuras
        alight = AmbientLight('alight')
        alight.setColor((0.3, 0.3, 0.3, 1))

        alnp = self.panda3d.render.attachNewNode(alight)
        self.panda3d.render.setLight(alnp)

    def set_lens(self, lens_type="OrthographicLens"):
        """
        Permite cambiar la lente de la camara

        :param lens_type: El tipo de lente a utilizar: OrthographicLens/PerspectiveLens
        :return: None
        """

        self.lens_type = lens_type
        width = self.panda3d.win.getXSize()
        height = self.panda3d.win.getYSize()

        if lens_type is "OrthographicLens":
            lens = OrthographicLens()
            lens.setFilmSize(width / 100, height / 100)
        if lens_type is "PerspectiveLens":
            lens = PerspectiveLens()
            lens.setFilmSize(width / 100, height / 100)
        else:
            # Default value
            lens = OrthographicLens()
            lens.setFilmSize(width / 100, height / 100)

        print("new lens {}: {} {}".format(lens_type, width / 100, height / 100))
        print(lens)
        self.panda3d.cam.node().setLens(lens)

    def window_rezise_event(self, window=None):
        """
        Se activa con cualquier evento de la ventana de windows, en caso de que haya
        cambiado de tamaño la ventana regenera la lente

        :param window: Información del evento
        :return: None
        """
        if window is not None:  # Window será igual a None si la aplicación panda3d no se inició
            wp = window.getProperties()
            newsize = [wp.getXSize(), wp.getYSize()]
            if self.winsize != newsize:
                self.winsize = newsize
                self.set_lens()

    def mouse_is_over_workspace(self):
        """
        Detecta si el mouse se encuentra dentro del area de trabajo del modelo 3d

        :return: True/False
        """
        is_over = False
        workspace = self.panda3d.kyvi_workspace

        if self.panda3d.mouseWatcherNode.has_mouse() and workspace is not None and workspace.active:
            pos = workspace.pos
            size = workspace.size
            offset_left, offset_top, offset_right, offset_bottom = workspace.offset

            offset = [0, 0, 0, 0]

            height = self.panda3d.win.getYSize()

            mouse_data = self.panda3d.win.getPointer(0)
            mouse_pos = mouse_data.getX(), height - mouse_data.getY()

            overmouse_x = (pos[0]+offset_left <= mouse_pos[0] <= pos[0]-offset_right + size[0])
            overmouse_y = (pos[1]+offset_bottom <= mouse_pos[1] <= pos[1]-offset_top + size[1])

            if overmouse_x and overmouse_y:
                is_over = True

        self.panda3d.mouse_on_workspace = is_over

        return is_over

    def camera_control_task(self, task):
        """
        Se ejecuta constantemente y realiza las tareas de movimiento de la camara según las teclas presionadas
        """

        # El codigo se ejecuta si el mouse está dentro del espacio de trabajo o si ya se está realizando alguna acción
        if self.mouse_is_over_workspace() or self.camera_active:
            # Desactivamos el espacio de trabajo
            self.panda3d.kyvi_workspace.active = False

            # El nodo mouseWatcherNode permite recibir la entrada de mouse y teclado
            btn = self.panda3d.mouseWatcherNode

            # Obtenemos la posición del cursor
            mouse_data = self.panda3d.win.getPointer(0)
            mouse_pos = mouse_data.getX(), mouse_data.getY()

            # En función de la combinación de teclas se ejecuta una acción
            cam_task = 0
            if btn.isButtonDown(self.orbit_mouse_btn) and btn.isButtonDown(self.orbit_keyboard_btn):
                cam_task = 1
            elif btn.isButtonDown(self.zoom_mouse_btn) and btn.isButtonDown(self.zoom_keyboard_btn):
                cam_task = 2
            elif btn.isButtonDown(self.pan_mouse_btn) and btn.isButtonDown(self.pan_keyboard_btn):
                cam_task = 3

            # Orbit
            if cam_task is 1:
                self.camera_orbit(mouse_pos)
                self.camera_active = True
            else:
                self.orbit_mouse_reference = None

            # Zoom
            if cam_task is 2:
                self.camera_zoom(mouse_pos)
                self.camera_active = True
            else:
                self.zoom_mouse_reference = None

            # Pan
            if cam_task is 3:
                self.camera_pan(mouse_pos)
                self.camera_active = True
            else:
                self.pan_mouse_reference = None

            # Si la combinación de teclas no coincide con niguna acción se establece la camara como inactiva
            if cam_task is 0:
                self.camera_active = False
                # Se reactiva el espacio de trabajo
                self.panda3d.kyvi_workspace.active = True
            else:
                # Actualizamos la posición de la luz puntual
                cam = self.panda3d.camera
                self.panda3d.plight_node.setPos(cam.get_pos(self.panda3d.render))

            # Ejecutar  solo en windows
            """if os.name == 'nt':
                # Se coloca la camra en determinadas vistas (frontal, lateral, superior, etc) al apretar el
                # teclado numérico

                # Lista de teclas http://www.kbdedit.com/manual/low_level_vk_list.html

                target = self.panda3d.cam_target
                if win32api.GetAsyncKeyState(win32con.VK_NUMPAD1):
                    target.set_hpr(0, 0, 0.)
                elif win32api.GetAsyncKeyState(win32con.VK_NUMPAD3):
                    target.set_hpr(90, 0, 0.)
                elif win32api.GetAsyncKeyState(win32con.VK_NUMPAD7):
                    target.set_hpr(0, -90, 0.)"""

        return task.cont

    def camera_orbit(self, mouse_pos):

        """
        Orbita la camara alrededor del objetivo de ésta, según la posición del mouse
        respecto del punto donde se hizo click
        """

        target = self.panda3d.cam_target

        if self.orbit_mouse_reference is None:
            self.orbit_mouse_reference = mouse_pos
            self.orbit_camera_reference = target.get_hpr()

        x_diff = self.orbit_mouse_reference[0] - mouse_pos[0]
        y_diff = self.orbit_mouse_reference[1] - mouse_pos[1]

        new_h = self.orbit_camera_reference[0] + x_diff / 4
        new_p = self.orbit_camera_reference[1] + y_diff / 4

        target.set_hpr(new_h, new_p, 0.)

    def camera_pan(self, mouse_pos):
        """
        Panea la camara alrededor del objetivo de ésta, según la posición del mouse
        respecto del punto donde se hizo click
        """
        target = self.panda3d.camera

        if self.pan_mouse_reference is None:
            self.pan_mouse_reference = mouse_pos
            self.pan_camera_reference = target.get_pos()

        x_diff = self.pan_mouse_reference[0] - mouse_pos[0]
        y_diff = self.pan_mouse_reference[1] - mouse_pos[1]

        new_x = self.pan_camera_reference[0] + x_diff / 100
        new_y = self.pan_camera_reference[1]
        new_z = self.pan_camera_reference[2] - y_diff / 100

        target.set_pos(new_x, new_y, new_z)

    def camera_zoom(self, mouse_pos):

        """
        Orbita la camara alrededor del objetivo de ésta, según la posición del mouse
        respecto del punto donde se hizo click
        """

        target = self.panda3d.cam_target

        if self.zoom_mouse_reference is None:
            self.zoom_mouse_reference = mouse_pos
            self.zoom_camera_reference = target.getScale()[0]

        y_diff = self.zoom_mouse_reference[1] - mouse_pos[1]

        new_scale = self.zoom_camera_reference * math.exp(y_diff/100)

        new_scale = max(new_scale, 0.1)
        new_scale = min(new_scale, 10)

        target.setScale(new_scale, new_scale, new_scale)

    def zoom_in(self):
        if self.mouse_is_over_workspace():
            target = self.panda3d.cam_target
            old_scale = target.getScale()[0]
            new_scale = old_scale - 0.1 * old_scale
            new_scale = max(new_scale, self.min_zoom)
            target.setScale(new_scale, new_scale, new_scale)

    def zoom_out(self):
        if self.mouse_is_over_workspace():
            target = self.panda3d.cam_target
            old_scale = target.getScale()[0]
            new_scale = old_scale + 0.1 * old_scale
            new_scale = min(new_scale, self.max_zoom)
            target.setScale(new_scale, new_scale, new_scale)

    def show_view_cube(self):
        """
        Agrega un indicador de ejes en la esquina inferior izquierda
        """
        scale = 0.08
        corner = self.panda3d.camera.attachNewNode("corner of screen")
        corner.setPos(-12.8 / 2 + 10 * scale, 5, -7.2 / 2 + 10 * scale)
        axis = self.panda3d.loader.loadModel("data/geom/custom-axis")

        # Dibujar por encima de todos los objetos
        axis.setBin("fixed", 0)

        """
        Tarea pendiente:
        
        Hay que corregir un error por el cual el indicador de ejes no se dubuja por encima de todos los objetos
        pudiendo intersectarse cona las geometrías del modelo
        
        Simplemente es un error visual, no afecta al funcionamiento
        
        axis.setDepthTest(False)
        
        https://discourse.panda3d.org/t/model-always-on-screen/8135/5
        """

        axis.setScale(scale)
        # axis.setScale(1)
        axis.reparentTo(corner)
        axis.setPos(-5 * scale, -5 * scale, -5 * scale)
        axis.setCompass()

    def add_cube(self):
        """
        Función de prueba, coloca cubos en la ubicación del cursor
        """
        if self.panda3d.mouse_on_workspace:
            print("add_cube")
            pos = self.panda3d.work_plane_mouse
            cube = self.panda3d.loader.loadModel("models/box")
            # Reparent the model to render.
            cube.reparentTo(self.panda3d.render)
            # Apply scale and position transforms on the model.
            cube.setScale(0.25, 0.25, 0.25)
            cube.setPos(pos[0], pos[1], pos[2])

    def myFunction(self):
        "Returns a collision entry for the closest object colliding with the ray."

        traverser = CollisionTraverser("")
        chq = CollisionHandlerQueue()
        rayNode = CollisionNode("")
        pickerRay = CollisionRay()


        # Make a collision node with one collision ray.
        ray.setOrigin(origin)
        ray.setDirection(dir)
        rayNode.addSolid(ray)

        # Attach the collision node to the provided node path.
        rayNP = rootNP.attachNewNode(rayNode)

        # This will let the ray detect collisions with normal geometry.
        rayNode.setFromCollideMask(GeomNode.getDefaultCollideMask())

        # Add the queue to a traverser, which will do the traversal
        # on the provided root node path.
        traverser.addCollider(rayNP, chq)
        traverser.traverse(rootNP)

        # Get the first node path in the sorted queue and discard the rest.
        if chq.getNumEntries() < 1:
            return None
        chq.sortEntries()
        return chq.getEntry(0)

    def entity_select(self):
        traverser = CollisionTraverser("")
        picker_ray = CollisionRay()
        handler = CollisionHandlerQueue()

        picker_node = CollisionNode('mouseRay')
        picker_np = self.panda3d.camera.attachNewNode(picker_node)
        picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
        picker_ray = CollisionRay()
        picker_node.addSolid(picker_ray)
        traverser.addCollider(picker_np, handler)

        mpos = self.panda3d.mouseWatcherNode.getMouse()
        picker_ray.setFromLens(self.panda3d.camNode, mpos.getX(), mpos.getY())
        traverser.traverse(self.panda3d.render)
        # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.

        if handler.getNumEntries() > 0:
            # This is so we get the closest object.
            handler.sortEntries()

            entity = handler.getEntry(0).getIntoNodePath()
            entity = entity.findNetTag('entity_id')
            if not entity.isEmpty():

                print("entity selected: {}".format(entity.getTag("entity_id")))

                entity_id = entity.getTag("entity_id")
                entity_type = entity.getTag("entity_type")
                print(entity_type)
                model = self.panda3d.model_reg

                category_type = model.get(entity_type, dict())
                entity = category_type.get(entity_id, None)
                widget = self.panda3d.kyvy_wid_properties
                print(entity)
                widget.entity_read(entity)
        else:

            entity = self.panda3d.view_entity
            widget = self.panda3d.kyvy_wid_properties
            widget.entity_read(entity)



