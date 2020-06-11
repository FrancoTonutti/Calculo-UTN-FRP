# Cálculo UTN FRP
Software de cálculo y detallado UTN FRP

Se necesita ```panda3d-kivy``` pero con la siguiente correción:

```bash
pip install https://github.com/FrancoTonutti/panda3d-kivy/archive/patch-1.zip
```

Para hacerla de forma manual a la correción, una vez instalado ```panda3d-kivy```, debe dirigirse dentro de su entorno virtual a:

```bash
../Lib/site-packages/panda3d-kivy/core/window.py
```

En la línea 103 encontrará el siguiente código:

```python
self.buttons_down.remove(button)
```
Y debe reemplazarlo por:

```python
self.buttons_down.discard(button)
```
