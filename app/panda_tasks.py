import numpy as np
from kivy.app import App
from app.model.entity import View


def on_complete_load_task(task):
    app = App.get_running_app()
    if app.root:
        print("on_complete_load")
        panda3d = app.root.panda3D

        panda3d.view_entity = View()

        panda3d.task_mgr.remove("on_complete_load_task")

    return task.cont


def get_mouse_3d_coords_task(task, pandapp=None):
    # Obtenemos la ubicación absoluta de la camara y su dirección

    if pandapp.mouseWatcherNode.has_mouse():
        camera_vect = pandapp.camera.getQuat(pandapp.render).getForward()
        camera_pos = pandapp.camera.get_pos(pandapp.render)

        """
        
        Para determinar la posición origen del rayo se mueve un objeto cursor enparentado a la camara, 
        estableciendo su posición realtiva a esta en funcion de la ubicacion del mouse
        
        """
        width = pandapp.win.getXSize()
        height = pandapp.win.getYSize()

        mouse_data = pandapp.win.getPointer(0)
        mouse_pos = mouse_data.getX(), mouse_data.getY()

        cursor_x = (mouse_pos[0] - width / 2) / 100
        cursor_y = (height / 2 - mouse_pos[1]) / 100

        pandapp.cursor.set_pos(cursor_x, 2, cursor_y)
        cursor_pos = pandapp.cursor.get_pos(pandapp.render)

        """
        El siguiente código calcula la intersección entre el plano de trabajo y la recta de acción del mouse
        
        from https://stackoverflow.com/a/39424162
        
        """
        epsilon = 1e-6
        # Define plane
        plane_normal = np.array(pandapp.work_plane_vect)
        plane_point = np.array(pandapp.work_plane_point)  # Any point on the plane

        # Define ray
        ray_direction = np.array(camera_vect)
        ray_point = np.array(cursor_pos)  # Any point along the ray

        ndotu = plane_normal.dot(ray_direction)
        if abs(ndotu) < epsilon:
            # No se encuentra intersección
            pandapp.work_plane_mouse = [None, None, None]
        else:
            # Se encuentra intersección
            w = ray_point - plane_point
            si = -plane_normal.dot(w) / ndotu
            psi = w + si * ray_direction + plane_point

            pandapp.work_plane_mouse = psi

    return task.cont
