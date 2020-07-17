from setuptools import setup

setup(
    name="CalculoUTN",
    options={
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
            ],
            'gui_apps': {
                'CalculoUTN': 'main.py',
            },
            'platforms': [
                'win_amd64',
                'win32',
            ],
            'log_filename': '$USER_APPDATA/CalculoUTN/output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'Kivy',
                'Pillow',
                'panda3d_kivy',
                'Kivy-Garden',
                'kivy-deps.glew',
                'kivy-deps.sdl2',
                'pywin32',
                'numpy',
            ]
        }
    },
    dependency_links=[
                'https://pypi.org/project/kivy-garden/'
            ]
)
