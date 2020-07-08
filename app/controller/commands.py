from kivy.app import App

command_list = dict()


def command(name, shortcut=None):
    """Esta funcion decorador registra comando para ser usado en la consola del programa,
    recibiendo como parametros el nombre y la tecla de ejecución abreviada"""

    global command_list

    def wrapper(function):
        global command_list

        command_list.update({name: {"name": name, "shortcut": shortcut, "command": function}})

        return function

    return wrapper
