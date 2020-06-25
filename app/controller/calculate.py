from kivy.app import App


def start_analysis():
    print("----------------------------------------------------")
    print("start_analysis()")

    # Accede a la interfaz de kivy para obtener la información de panda3d
    app = App.get_running_app()
    panda3d = app.root.panda3D
    # Obtenemos el registro del modelo
    model_reg = panda3d.model_reg

    # Recorremos la lista de barras e imprimimos en consola las posiciones de inicio y fin de cada barra
    bar_list = model_reg.get("Bar", [])
    i = 1
    for bar in bar_list:
        print("Barra {}".format(i))
        print(bar.start.position)
        print(bar.end.position)
        i += 1

    print("Done")
    print("----------------------------------------------------")

    return None
