from kivy.app import App

command_list = dict()


def command(name: str, shortcut: str = ""):
    """Esta funcion decorador registra un comando para ser usado en la consola del programa,
    recibiendo como parametros el nombre y la tecla de ejecución abreviada"""

    global command_list

    def wrapper(function):
        global command_list
        print("comand_register: {} - {}()".format(name, function.__name__))
        command_list.update({name: {"name": name, "shortcut": shortcut, "function": function}})

        return function

    return wrapper


def execute(command_name: str):
    """Ejecuta el comando de consola indicado"""
    app = App.get_running_app()
    panda3d = app.root.panda3D
    data = panda3d.commands.get(command_name, None)

    if data is not None:
        function = data['function']
        function()
    else:
        print("Comando no encontrado")
