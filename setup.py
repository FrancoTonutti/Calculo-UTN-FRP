from setuptools import setup

"""
Comando para compilar:

python setup.py bdist_apps
"""

setup(
    name="CalculoUTN",
    options={
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.prc',
                '**/*.ttf',
                '**/*.cur',
            ],
            'gui_apps': {
                'CalculoUTN_testgui': 'main.py',
            },
            'platforms': [
                'win_amd64'
            ],
            'log_filename': '$USER_APPDATA/CalculoUTN_testgui/output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'Pillow',
                'numpy',

            ],
        }
    }
)
