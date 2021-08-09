from app.controller.commands import bar, calculate, render, regen_ui, wireframe_toggle, load, matricial, save_ifc, \
    material_editor, save, open_file, new_file, load_combinations_ui, analysis_results_ui, remove_diagrams

"""import importlib
import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    importlib.import_module("app.controller.commands."+module[:-3])
del module"""

print("-- All commands loaded --")
