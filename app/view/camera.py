from panda3d.core import Point3, OrthographicLens, PerspectiveLens, PointLight, \
    AmbientLight, CollisionTraverser, \
    CollisionHandlerQueue, CollisionNode, CollisionRay, GeomNode, LVecBase4, \
    DirectionalLight, BoundingSphere, BitMask32
import math
from app import app
from direct.showbase.DirectObject import DirectObject
import numpy as np
from app.model import View
from app.model.transaction import Transaction
from app.model.view_gizmo import ViewGizmoZone

"""if os.name == 'nt':
    # Importar solo en windows
    import win32api
    import win32con"""


class CameraControl(DirectObject):
    def __init__(self, panda3d):
        # Inicialización de variables
        self.mouse_1_status = 0
        self.winsize = [0, 0]
        self.panda3d = panda3d
        self.panda3d.mouse_on_workspace = False

        # Desabilita el comportamiento por defecto de la camara
        self.panda3d.disable_mouse()

        # Llama a la función self.window_rezise_event cuando la ventana cambia de tamaño
        self.accept('window-event', self.window_rezise_event)
        # self.panda3d.accept('aspectRatioChanged', lambda: print("ss"))
        # Creamos el punto donde se centrará la cámara
        target_pos = Point3(0., 0., 0.)

        self.panda3d.cam_target = self.panda3d.render.attach_new_node("camera_target")
        self.panda3d.cam_target.set_pos(target_pos)
        self.panda3d.camera.reparent_to(self.panda3d.cam_target)
        self.panda3d.camera.set_y(-50.)
        self.panda3d.camera.getChildren()[0].node().setCameraMask(BitMask32.bit(0))
        
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
        # self.panda3d.accept("mouse1", self.entity_select)

        # Se establece la lente ortografica en lugar de la perspectiva
        self.lens_type = "OrthographicLens"
        self.set_lens(self.lens_type)

        # Agrega un indicador de ejes en la esquina inferior izquierda
        self.corner = self.panda3d.camera.attachNewNode("corner of screen")
        # self.axis = self.panda3d.loader.loadModel("data/geom/custom-axis")
        # self.axis = self.panda3d.loader.loadModel("data/geom/view_gizmo_F")
        self.view_gizmo = list()
        self.view_gizmo.append(self.panda3d.loader.loadModel("data/geom/view_gizmo_compass"))

        # self.view_gizmo.append(self.panda3d.loader.loadModel("data/geom/view_gizmo_L"))
        # self.view_cube = ViewGizmoZone()
        # self.view_cube.set_geom(self.axis)

        for gizmo_geom in self.view_gizmo:
            gizmo_geom.setLightOff(1)
            # gizmo_geom.setColorScale(1,1,1,1)
            gizmo_geom.setShaderInput("colorborders", LVecBase4(0, 0, 0, 0.25))

            tr = Transaction()
            tr.start("Create ViewGizmoZone")
            gizmo = ViewGizmoZone()

            gizmo.set_geom(gizmo_geom)
            tr.commit()
            gizmo_geom.node().setBounds(BoundingSphere(Point3(0, 0, 0), 10))
            gizmo_geom.node().setFinal(True)

            #gizmo_geom.showTightBounds()
            # gizmo_geom.showBounds()



        self.show_view_gizmo()

        # Agregamos una luz puntual en la ubicación de la camara
        plight = DirectionalLight("camera_light")
        plight.setColor((1, 1, 1, 1))
        #plight.setAttenuation((1, 0, 0))
        #print("getMaxDistance {}".format(plight.getMaxDistance()))
        self.panda3d.plight_node = self.panda3d.render.attach_new_node(plight)
        self.panda3d.plight_node.setPos(0, -50, 0)
        self.panda3d.render.setLight(self.panda3d.plight_node)
        self.panda3d.plight_node.reparentTo(self.panda3d.camera)



        # Agregamos luz ambiental que disminuya las zonas oscuras
        alight = AmbientLight('alight')
        alight.setColor((0.3, 0.3, 0.3, 1))

        alnp = self.panda3d.render.attachNewNode(alight)
        self.panda3d.render.setLight(alnp)

        #def init_select_detection(self):
        self.traverser = CollisionTraverser("")
        # self.traverser.show_collisions(self.panda3d.render)
        self.picker_ray = CollisionRay()
        self.handler = CollisionHandlerQueue()

        self.picker_node = CollisionNode('mouseRay')
        self.picker_np = self.panda3d.camera.attachNewNode(self.picker_node)
        self.picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.picker_ray = CollisionRay()
        self.picker_node.addSolid(self.picker_ray)
        self.traverser.addCollider(self.picker_np, self.handler)

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
            lens.setFilmSize(width, height )
        if lens_type is "PerspectiveLens":
            lens = PerspectiveLens()
            lens.setFilmSize(width , height )
        else:
            # Default value
            lens = OrthographicLens()
            lens.setFilmSize(width / 100, height / 100)

        print("new lens {}: {} {}".format(lens_type, width / 100, height / 100))
        print(lens)
        self.panda3d.cam.node().setLens(lens)

        shader_control = self.panda3d.shader_control
        if shader_control is not None:
            shader_control.update_camera_lens(lens)

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
                self.show_view_gizmo()

    def mouse_is_over_workspace(self):
        """
        Detecta si el mouse se encuentra dentro del area de trabajo del modelo 3d

        :return: True/False
        """
        gui_objects = app.gui_objects
        is_over_workspace = False

        if self.panda3d.mouseWatcherNode.has_mouse() and app.workspace_active:
            is_over_workspace = True
            mouse_data = self.panda3d.win.getPointer(0)
            mouse_x, mouse_y = mouse_data.getX(), mouse_data.getY()
            objects_to_clear = list()

            for name, gui_obj in gui_objects.items():

                if gui_obj.isHidden():
                    continue

                if gui_obj.is_empty():
                    objects_to_clear.append(name)
                    continue


                pos = gui_obj.getPos(pixel2d)
                frame_size = list(gui_obj["frameSize"])

                x0 = pos[0] + frame_size[0]
                x1 = pos[0] + frame_size[1]
                y0 = -pos[2] - frame_size[2]
                y1 = -pos[2] - frame_size[3]

                x_left = min(x0, x1)
                x_right = max(x0, x1)
                y_top = min(y0, y1)
                y_bottom = max(y0, y1)

                #if name is "status_bar":
                #print(pos)
                #print("{} {} / {} {}".format(x_left, x_right, y_top, y_bottom))

                overmouse_x = (x_left <= mouse_x <= x_right)
                overmouse_y = (y_top <= mouse_y <= y_bottom)

                # Revisa si el mouse se encuentra sobre un elemento de interfaz
                if overmouse_x and overmouse_y:

                    # print("mouse is over {}".format(name))
                    is_over_workspace = False
                    break

            for name in objects_to_clear:
                gui_objects.pop(name)


        app.mouse_on_workspace = is_over_workspace
        if is_over_workspace:
            get_mouse_3d_coords_task()

        return is_over_workspace

    def camera_control_task(self, task):
        """
        Se ejecuta constantemente y realiza las tareas de movimiento de la camara según las teclas presionadas
        """

        # El codigo se ejecuta si el mouse está dentro del espacio de trabajo o si ya se está realizando alguna acción
        if self.mouse_is_over_workspace() or self.camera_active:
            # Desactivamos el espacio de trabajo
            app.workspace_active = False

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
                app.workspace_active = True
                self.entity_select()
            else:
                pass
                # Actualizamos la posición de la luz puntual
                #cam = self.panda3d.camera
                #self.panda3d.plight_node.setPos(cam.get_pos(self.panda3d.render))

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

    def show_view_gizmo(self):
        """
        Agrega un indicador de ejes en la esquina inferior izquierda
        """
        scale = 0.075
        width = self.panda3d.win.getXSize()/100
        height = self.panda3d.win.getYSize()/100

        #self.corner.setPos(width / 2 - 10 * scale, 5, height / 2 - 28 * scale)
        self.corner.setPos(width / 2-1, 5, height / 2 - 2.4)

        print("DEBUG SHOW VIEW CUBE")
        print(height)
        print(height / 2 - 28 * scale)

        # Dibujar por encima de todos los objetos

        for gizmo_geom in self.view_gizmo:
            gizmo_geom.setLightOff(1)
            # gizmo_geom.setBin("fixed", 0)

            # gizmo_geom.set_two_sided(True)

            """
            Tarea pendiente:
            
            Hay que corregir un error por el cual el indicador de ejes no se dubuja por encima de todos los objetos
            pudiendo intersectarse cona las geometrías del modelo
            
            Simplemente es un error visual, no afecta al funcionamiento
            
            axis.setDepthTest(False)
            
            https://discourse.panda3d.org/t/model-always-on-screen/8135/5
            """

            gizmo_geom.setScale(scale)
            # axis.setScale(1)
            gizmo_geom.reparentTo(self.corner)
            #
            gizmo_geom.setPos(0, 0, 0)
            gizmo_geom.setCompass()
            separation = 1
            # gizmo_geom.setShaderInput("showborders", LVecBase4(0))
            # gizmo_geom.setShaderInput("colorborders", LVecBase4(0, 0, 0, 0))
            # gizmo_geom.setShaderInput("separation", LVecBase4(separation, 0, separation, 0))




    def mouse1_btn_released(self):
        mouse_watcher = self.panda3d.mouseWatcherNode
        if mouse_watcher.hasMouse():
            if mouse_watcher.isButtonDown("mouse1"):
                self.mouse_1_status = 1
            else:
                if self.mouse_1_status is 1:
                    self.mouse_1_status = 0
                    return True

        return False



    def entity_select(self):
        if self.panda3d.mouseWatcherNode.hasMouse():
            """traverser = CollisionTraverser("")
            #traverser.show_collisions(render)
            picker_ray = CollisionRay()
            handler = CollisionHandlerQueue()

            picker_node = CollisionNode('mouseRay')
            picker_np = self.panda3d.camera.attachNewNode(picker_node)
            picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
            picker_ray = CollisionRay()
            picker_node.addSolid(picker_ray)
            traverser.addCollider(picker_np, handler)

            picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
            mpos = self.panda3d.mouseWatcherNode.getMouse()
            picker_ray.setFromLens(self.panda3d.camNode, mpos.getX(), mpos.getY())
            traverser.traverse(self.panda3d.render)"""


            self.picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
            mpos = self.panda3d.mouseWatcherNode.getMouse()
            self.picker_ray.setFromLens(self.panda3d.camNode, mpos.getX(), mpos.getY())
            self.traverser.traverse(self.panda3d.render)
            handler = self.handler

            # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
            btn = self.panda3d.mouseWatcherNode

            if handler.getNumEntries() > 0:
                # This is so we get the closest object.
                handler.sortEntries()



                count = handler.getNumEntries()

                for i in range(count):
                    geom_node = handler.getEntry(i).getIntoNodePath()

                    node_ancestor = geom_node.findNetTag('entity_id')
                    select_hidden = node_ancestor.getPythonTag("select_hidden")

                    if not node_ancestor.isHidden() or select_hidden:

                        #entity = node_ancestor.findNetTag('entity_id')
                        if not node_ancestor.isEmpty() and node_ancestor.hasTag("entity_id"):

                            # print("entity selected: {}".format(entity.getTag("entity_id")))

                            entity_id = node_ancestor.getTag("entity_id")
                            entity_type = node_ancestor.getTag("entity_type")
                            # print(entity_type)
                            model = app.model_reg

                            category_type = model.get(entity_type, dict())
                            entity = category_type.get(entity_id, None)

                            # print(entity)
                            #if btn.isButtonDown("mouse1"):
                            if self.mouse1_btn_released():
                                entity.on_click()
                                if entity.is_editable:
                                    prop_editor = app.main_ui.prop_editor
                                    prop_editor.add_to_selection(entity)
                            elif entity.is_selectable:
                                status_bar = app.main_ui.status_bar
                                status_bar.entity_read(entity)

                            break
                else:
                    status_bar = app.main_ui.status_bar
                    status_bar.entity_read()
                    #print("Hay {} entidades sin geometria visible bajo el mouse".format(handler.getNumEntries()))
            else:
                #if btn.isButtonDown("mouse1"):
                if self.mouse1_btn_released():
                    entities = app.model_reg.get("View", {})

                    if entities is None or len(entities) is 0:
                        tr = Transaction("Create")
                        tr.start("Create View")
                        View()
                        tr.commit()

                    entities = app.model_reg.get("View")
                    entity = list(entities.values())[0]
                    prop_editor = app.main_ui.prop_editor

                    prop_editor.add_to_selection(entity)
                else:
                    status_bar = app.main_ui.status_bar
                    status_bar.entity_read()




def get_mouse_3d_coords_task():
    # Obtenemos la ubicación absoluta de la camara y su dirección
    base = app.get_show_base()

    if base.mouseWatcherNode.has_mouse():
        camera_vect = base.camera.getQuat(base.render).getForward()
        camera_pos = base.camera.get_pos(base.render)

        """

        Para determinar la posición origen del rayo se mueve un objeto cursor enparentado a la camara, 
        estableciendo su posición realtiva a esta en funcion de la ubicacion del mouse

        """
        width = base.win.getXSize()
        height = base.win.getYSize()

        mouse_data = base.win.getPointer(0)
        mouse_pos = mouse_data.getX(), mouse_data.getY()

        cursor_x = (mouse_pos[0] - width / 2) / 100
        cursor_y = (height / 2 - mouse_pos[1]) / 100

        app.cursor.set_pos(cursor_x, 2, cursor_y)
        cursor_pos = app.cursor.get_pos(base.render)

        """
        El siguiente código calcula la intersección entre el plano de trabajo y la recta de acción del mouse

        from https://stackoverflow.com/a/39424162

        """
        epsilon = 1e-6
        # Define plane
        plane_normal = np.array(app.work_plane_vect)
        plane_point = np.array(app.work_plane_point)  # Any point on the plane

        # Define ray
        ray_direction = np.array(camera_vect)
        ray_point = np.array(cursor_pos)  # Any point along the ray

        ndotu = plane_normal.dot(ray_direction)
        if abs(ndotu) < epsilon:
            # No se encuentra intersección
            app.work_plane_mouse = [None, None, None]
        else:
            # Se encuentra intersección
            w = ray_point - plane_point
            si = -plane_normal.dot(w) / ndotu
            psi = w + si * ray_direction + plane_point

            app.work_plane_mouse = psi

    return app.work_plane_mouse
