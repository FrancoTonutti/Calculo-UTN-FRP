from app.model.entity import Entity
from app.model.node import Node
from app.model.bar import Bar
from app.model.section import Section
from app.model.view import View
from app.model.load import Load
from app.model.diagram import Diagram
from app.model.model_reg import ModelReg
from app.model.material import Material
from app.model.view_gizmo import ViewGizmoZone
from app.model.load_type import LoadType
from app.model import model_reg



model_reg.class_register = {
    "Entity": Entity,
    "Node": Node,
    "Bar": Bar,
    "Section": Section,
    "View": View,
    "Load": Load,
    "Diagram": Diagram,
    "Material": Material,
    "ViewGizmoZone": ViewGizmoZone,
    "LoadType": LoadType
}


