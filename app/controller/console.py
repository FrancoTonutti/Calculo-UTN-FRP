from app import app


def command(name: str, shortcut: str = "", args=None):
    """Esta funcion decorador registra un comando para ser usado en la consola del programa,
    recibiendo como parametros el nombre y la tecla de ejecución abreviada"""

    def wrapper(function):
        print("comand_register: {} - {}()".format(name, function.__name__))
        app.commands.update({name: {"name": name, "shortcut": shortcut, "function": function, "args": args}})

        return function

    return wrapper


def execute(command_name: str):
    """Ejecuta el comando de consola indicado"""
    data = app.commands.get(command_name, None)

    if data is not None:
        function = data['function']
        app.console.active_command = command_name
        function()
    else:
        print("Comando no encontrado")
        print("commands:", app.commands)

    return data
