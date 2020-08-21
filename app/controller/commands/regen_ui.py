from app.controller.console import command
from app import app
from app.view.simpleui import update_ui


@command(name="regen_ui")
def regen_ui():
    update_ui()
