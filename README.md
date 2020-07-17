# Cálculo UTN FRP

<p align="center">
  <img src="http://www.frp.utn.edu.ar/info2/wp-content/uploads/2018/03/utn-parana.png">
</p>

Software de cálculo y detallado UTN FRP

Este proyecto surge con bajo la modalidad de beca de servicio en la Universidad Tecnológica Nacional, Facultad Regional Paraná con el objetivo de desarrollar un software de cálculo y detallado de estructuras de hormigón armando. 


<h2>Instalación</h2>
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
