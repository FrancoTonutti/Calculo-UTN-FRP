from app.model.entity import Entity, Test2
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
from app.model.profile_sections import ProfileSection
from app.model.profile_sections import ProfileSectionI
from app.model.code_checks import CodeCheckCIRSOC201
from .rebar_set import RebarSet
from .rebar_layer import RebarLayer

from app.model import model_reg
from app.model import unit_manager

from .level import Level
from .mouse_event_handler import MouseEventHandler

model_reg.class_register = {
    "Entity": Entity,
    "Level": Level,
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
    "CodeCheck": CodeCheck,
    "ProfileSection": ProfileSection,
    "ProfileSectionI": ProfileSectionI,
    "CodeCheckCIRSOC201": CodeCheckCIRSOC201,
    "RebarLayer": RebarLayer,
    "RebarSet": RebarSet,
    "Test2": Test2
}

#model_reg.ModelReg.class_register = model_reg.class_register

print("CLASS REGISTER CREATED")

model_reg.keys_priority = ["View", "Level", "Node", "Section", "MaterialGroup", "Material", "Bar", "RebarLayer", "RebarSet", "LoadType", "Load", "Diagram"]


