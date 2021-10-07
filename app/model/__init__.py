from app.model.entity import Entity
from app.model.node import Node
from app.model.bar import Bar
from app.model.beam import Beam
from app.model.section import Section
from app.model.view import View
from app.model.load import Load
from app.model.diagram import Diagram
from app.model.model_reg import ModelReg
from app.model.material_group import MaterialGroup
from app.model.material import Material
from app.model.view_gizmo import ViewGizmoZone
from app.model.load_type import LoadType
from app.model.load_combination import LoadCombination
from app.model.code_check import CodeCheck
from app.model import model_reg
from app.model import unit_manager


model_reg.class_register = {
    "Entity": Entity,
    "Node": Node,
    "Bar": Bar,
    "Section": Section,
    "View": View,
    "Load": Load,
    "Diagram": Diagram,
    "Material": Material,
    "MaterialGroup": MaterialGroup,
    "ViewGizmoZone": ViewGizmoZone,
    "LoadType": LoadType,
    "LoadCombination": LoadCombination,
    "CodeCheck": CodeCheck
}


