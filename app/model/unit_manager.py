from app import app
import pint
ureg = app.ureg

unit_settings = {
    "load": "kN",
    "load_lineal": "(kN) / (m)",
    "specific_weight": "(kN) / (m**3)",
    "stress": "MPa"
}


def default_ureg(unit_type):
    return ureg(unit_settings[unit_type])


@ureg.wraps(None, 'MPa')
def convert_to_MPa(value):
    return value


@ureg.wraps(None, 'kN')
def convert_to_kN(value):
    return value


@ureg.wraps(None, '(kN)/(m**3)')
def convert_to_kN_m3(value):
    return value


@ureg.wraps(None, 'cm')
def convert_to_cm(value):
    return value


@ureg.wraps(None, 'm')
def convert_to_m(value):
    return value


@ureg.wraps(None, 'mm')
def convert_to_mm(value):
    return value
