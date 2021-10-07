from app import app
import pint
ureg = app.ureg

unit_settings = {
    "load": "kN",
}


@ureg.wraps(None, 'MPa')
def convert_to_MPa(value):
    return value


@ureg.wraps(None, 'kN')
def convert_to_kN(value):
    return value
