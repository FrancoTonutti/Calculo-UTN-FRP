from setuptools import setup
import kivy.tools.packaging.pyinstaller_hooks as kivy_hooks

setup(
    name="CalculoUTN",
    options={
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
            ],
            'console_apps': {
                'CalculoUTN': 'main.py',
            },
            'platforms': [
                'win_amd64'
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
                'kivy._clock',
                'kivy.weakmethod'

            ],
            'include_modules': [] + kivy_hooks.get_deps_all()['hiddenimports'] + list(set(
                kivy_hooks.get_factory_modules() + kivy_hooks.kivy_modules

                ))
        }
    }
)
