from setuptools import setup

"""
Comando para compilar:

python setup.py bdist_apps
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
            ],
            'exclude_patterns': [
                'build/**',
                'dist/**',
                'test/**'
            ],
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
                'win_amd64',
                'win32'
            ],
            'package_data_dirs': {
                'numpy': [('numpy.libs/*', '', {'PKG_DATA_MAKE_EXECUTABLE'})]},

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
