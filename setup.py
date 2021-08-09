from setuptools import setup

"""
Comando para compilar:

>python setup.py bdist_apps

Si cambia la versión de panda3d, es necesario borrar las carpetas "build" y "dist" antes de hacer una nueva compilación.

Pasos manuales luego de la compilación:

1- Dirigirse a la instalación de la versión de python que se está usando, 
como por ejemplo: "C:/Panda3D-1.10.8-x64/python", y copiar la carpeta "tcl" a la carpeta de su distribución, debe quedar
algo así : “build/win_amd64/tcl”

"""

setup(
    name="CalculoUTN",
    version='0.0.1',
    options={
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.prc',
                '**/*.ttf',
                '**/*.cur',
                '**/*.ico',
                '**/*.ico',
                '**/*.vert',
                '**/*.frag',
                '**/*.sha',
                'ifcopenshell/_ifcopenshell_wrapper.pyd',
                '**/tcl/**',
                '**/*.tcl',
            ],
            'exclude_patterns': [
                'build/**',
                'dist/**',
                'test/**'
            ],
            'rename_paths': {'ifcopenshell/_ifcopenshell_wrapper.pyd': '_ifcopenshell_wrapper.pyd'},
            'gui_apps': {
                'CalculoUTN': 'main.py',
            },
            "icons": {
                "CalculoUTN": [
                    "data/icons/icon16.png",
                    "data/icons/icon32.png",
                    "data/icons/icon48.png",
                    "data/icons/icon128.png",
                    "data/icons/icon256.png",
                ]
            },
            'platforms': [
                'win_amd64', 'win32'
            ],
            'package_data_dirs': {
                'numpy': [('numpy.libs/*', '', {'PKG_DATA_MAKE_EXECUTABLE'})],
                'win32': [('pywin32_system32/*', '', {}), ('win32/*.pyd', '', {})],
            },
            'log_filename': '$USER_APPDATA/CalculoUTN_testgui/output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'Pillow',
                'numpy',
                'tkinter',
                'tcl'
            ],
        }
    }
)

