from panda3d.core import Point3, OrthographicLens, PerspectiveLens, NodePath


class Base:
    show_base = None
    mouse_data = dict()


base = Base()


def show_view_cube(show_base, enabled=True):
    if enabled:
        base.show_base = show_base
        scale = 0.08
        corner = show_base.camera.attachNewNode("corner of screen")
        corner.setPos(-12.8/2+10*scale, 5, -7.2/2+10*scale)
        # axis = show_base.loader.loadModel("zup-axis")
        # axis = show_base.loader.loadModel("models/axis-z-sup2")
        axis = show_base.loader.loadModel("models/custom-axis2")

        # Dibujar por encima de todos los objetos
        """
        axis.setDepthTest(False)
        """
        axis.setBin("fixed", 0)


        """
        Fix bug with:
        https://discourse.panda3d.org/t/model-always-on-screen/8135/5
        
        
        gunRender = NodePath('gunRender')
        base.show_base.camera2 = base.show_base.makeCamera(base.show_base.win, sort=5, clearDepth=True)
        base.show_base.camera2.reparentTo(gunRender)
        base.show_base.camera2.set_y(-50.)

        corner2 = show_base.camera2.attachNewNode("corner of screen2")

        gunModel = show_base.loader.loadModel("models/custom-axis2")
        gunModel.reparentTo(corner2)
        gunModel.setPos(0, 30, -5)
        gunModel.setCompass()
        """



        axis.setScale(scale)
        # axis.setScale(1)
        axis.reparentTo(corner)
        axis.setPos(-5*scale, -5*scale, -5*scale)
        axis.setCompass()


def enable(show_base, enabled=True):
    if enabled:

        base.show_base = show_base
        print("start orbit")
        show_base.disable_mouse()
        camera_control()

    else:
        base.show_base = None


def camera_control():
    if base.show_base is not None:
        base.show_base.winsize = [0, 0]
        print(base.show_base.accept)


        base.show_base.accept("mouse1", add_cube)



        base.show_base.accept("shift-mouse2", start_orbit)
        base.show_base.accept("shift-mouse2-up", end_orbit)

        base.show_base.accept("mouse2", start_pan)
        base.show_base.accept("mouse2-up", end_pan)

        base.show_base.accept("wheel_up", zoom_in)
        base.show_base.accept("wheel_down", zoom_out)

        base.show_base.accept("shift", shift_press)
        base.show_base.accept("shift-up", shift_release)

        base.show_base.accept("1", numpad, extraArgs=[1])
        base.show_base.accept("3", numpad, extraArgs=[3])
        base.show_base.accept("7", numpad, extraArgs=[7])
        base.show_base.accept("9", numpad, extraArgs=[9])

        base.show_base.accept('window-event', windowEventHandler)

        target_pos = Point3(0., 0., 0.)

        base.show_base.cam_target = base.show_base.render.attach_new_node("camera_target")
        base.show_base.cam_target.set_pos(target_pos)
        base.show_base.camera.reparent_to(base.show_base.cam_target)
        base.show_base.camera.set_y(-50.)

        cube = base.show_base.loader.loadModel("models/box")
        scale = 0.1
        cube.setScale(scale, scale, scale)
        cube.setPos(-0.5*scale, -0.5*scale, -0.5*scale)
        cube.reparentTo(base.show_base.cam_target)

        win_props = base.show_base.win.get_properties()
        w, h = win_props.get_x_size(), win_props.get_y_size()
        base.show_base.win.move_pointer(0, w // 2, h // 2)
        base.show_base.turnSpeed = 10.
        base.show_base.accept("escape", base.show_base.userExit)


def add_cube():
    print("add_cube")
    pos = base.show_base.work_plane_mouse
    cube = base.show_base.loader.loadModel("models/box")
    # Reparent the model to render.
    cube.reparentTo(base.show_base.render)
    # Apply scale and position transforms on the model.
    cube.setScale(0.25, 0.25, 0.25)
    cube.setPos(pos[0], pos[1], pos[2])


def windowEventHandler(window=None):
    if window is not None:  # window is none if panda3d is not started
        wp = window.getProperties()
        newsize = [wp.getXSize(), wp.getYSize()]
        if base.show_base.winsize != newsize:
            # resizing the window breaks the filter manager, so I just make a new one
            base.show_base.winsize = newsize
            print("WIN RESIZE!!")
            set_lens(base.show_base, lens_type="OrthographicLens")


def numpad(key):
    print("NUMPAD {}".format(key))
    target = base.show_base.cam_target

    if key is 1:
        target.set_hpr(0, 0, 0.)
    elif key is 3:
        target.set_hpr(90, 0, 0.)
    elif key is 7:
        target.set_hpr(0, -90, 0.)



def shift_press():
    if base.show_base.task_mgr.hasTaskNamed("pan_task"):
        end_pan()
        start_orbit()


def shift_release():
    if base.show_base.task_mgr.hasTaskNamed("orbit_task"):
        end_orbit()
        start_pan()


def start_orbit():
    print("start orbit")

    base.show_base.task_mgr.add(orbit_task, "orbit_task")

    mouse_data = base.show_base.win.getPointer(0)
    mouse_pos = mouse_data.getX(), mouse_data.getY()
    base.mouse_data.update({"last_middle_press": mouse_pos})

    target = base.show_base.cam_target
    base.mouse_data.update({"camera_hpr": (target.get_h(), target.get_p(), 0)})


def end_orbit():
    print("end_orbit")
    mouse_data = base.show_base.win.getPointer(0)
    mouse_pos = mouse_data.getX(), mouse_data.getY()
    base.mouse_data.update({"last_middle_release": mouse_pos})

    base.show_base.task_mgr.remove("orbit_task")


def start_pan():
    print("start pan")

    base.show_base.task_mgr.add(pan_task, "pan_task")
    mouse_data = base.show_base.win.getPointer(0)
    mouse_pos = mouse_data.getX(), mouse_data.getY()
    base.mouse_data.update({"last_middle_press": mouse_pos})
    target = base.show_base.camera
    base.mouse_data.update({"camera_pos": (target.get_x(), target.get_y(), target.get_z())})



def end_pan():
    print("end_pan")

    mouse_data = base.show_base.win.getPointer(0)
    mouse_pos = mouse_data.getX(), mouse_data.getY()
    base.mouse_data.update({"last_middle_release": mouse_pos})

    base.show_base.task_mgr.remove("pan_task")
    base.show_base.task_mgr.remove("orbit_task")



def orbit_task(task):
    """
    Orbit the camera about its target point by offsetting the orientation
    of the target node with the mouse motion.

    """

    if base.show_base.mouseWatcherNode.has_mouse():
        d_h, d_p = base.show_base.mouseWatcherNode.get_mouse() * base.show_base.turnSpeed

        mouse_data = base.show_base.win.getPointer(0)
        mouse_pos = mouse_data.getX(), mouse_data.getY()

        x_diff = base.mouse_data["last_middle_press"][0] - mouse_pos[0]
        y_diff = base.mouse_data["last_middle_press"][1] - mouse_pos[1]

        # print(base.show_base.mouseWatcherNode.get_mouse())

        target = base.show_base.cam_target

        # print(target.get_h())
        # print(target.get_p())

        # target.set_hpr(target.get_h() - d_h, target.get_p() + d_p, 0.)
        new_h = base.mouse_data["camera_hpr"][0] + x_diff / 4
        new_p = base.mouse_data["camera_hpr"][1] + y_diff / 4
        # target.set_hpr(target.get_h() - d_h, -35, 0.)
        target.set_hpr(new_h, new_p, 0.)
        target2 = base.show_base.cam_target
        target2.set_hpr(new_h, new_p, 0.)
    # win_props = base.show_base.win.get_properties()
    # w, h = win_props.get_x_size(), win_props.get_y_size()
    # base.show_base.win.move_pointer(0, w // 2, h // 2)

    return task.cont


def zoom_in():
    target = base.show_base.cam_target
    old_scale = target.getScale()[0]
    new_scale = old_scale - 0.1*old_scale
    new_scale = max(new_scale, 0.1)
    target.setScale(new_scale, new_scale, new_scale)


def zoom_out():
    target = base.show_base.cam_target
    old_scale = target.getScale()[0]
    new_scale = old_scale + 0.1*old_scale
    if new_scale < 100:
        target.setScale(new_scale, new_scale, new_scale)


def pan_task(task):
    """
    Orbit the camera about its target point by offsetting the orientation
    of the target node with the mouse motion.

    """

    if base.show_base.mouseWatcherNode.has_mouse():
        d_h, d_p = base.show_base.mouseWatcherNode.get_mouse() * base.show_base.turnSpeed

        mouse_data = base.show_base.win.getPointer(0)
        mouse_pos = mouse_data.getX(), mouse_data.getY()

        x_diff = base.mouse_data["last_middle_press"][0] - mouse_pos[0]
        y_diff = base.mouse_data["last_middle_press"][1] - mouse_pos[1]

        # print(base.show_base.mouseWatcherNode.get_mouse())

        # Movemos la camara dejando el nodo padre de la camara fijo en el punto de referencia
        target = base.show_base.camera

        # print(target.get_h())
        # print(target.get_p())

        # target.set_hpr(target.get_h() - d_h, target.get_p() + d_p, 0.)
        new_x = base.mouse_data["camera_pos"][0] + x_diff / 150
        new_y = base.mouse_data["camera_pos"][1]
        new_z = base.mouse_data["camera_pos"][2] - y_diff / 150
        # target.set_hpr(target.get_h() - d_h, -35, 0.)
        target.set_pos(new_x, new_y, new_z)

    # win_props = base.show_base.win.get_properties()
    # w, h = win_props.get_x_size(), win_props.get_y_size()
    # base.show_base.win.move_pointer(0, w // 2, h // 2)

    return task.cont


def set_lens(show_base, lens_type="OrthographicLens"):
    width = show_base.win.getXSize()
    height = show_base.win.getYSize()

    if lens_type is "OrthographicLens":
        lens = OrthographicLens()
        lens.setFilmSize(width/100, height/100)
    if lens_type is "PerspectiveLens":
        lens = PerspectiveLens()
        lens.setFilmSize(width/100, height/100)
    else:
        # Default value
        lens = OrthographicLens()
        lens.setFilmSize(width/100, height/100)

    print("new lens {}: {} {}".format(lens_type, width/100, height/100))
    print(lens)
    show_base.cam.node().setLens(lens)
