""""
Example:
https://thinkmoult.com/using-ifcopenshell-parse-ifc-files-python.html

http://academy.ifcopenshell.org/creating-a-simple-wall-with-property-set-and-quantity-information/
"""
from app import app
from app.controller.console import command
import ifc_tools

import tkinter as tk
from tkinter import filedialog


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Imports only for IDE type hints
    pass

import time
import tempfile
import ifcopenshell

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.


@command(name="save", shortcut="s")
def save():
    print("----------------------------------------------------")
    print("save()")
    root = tk.Tk()
    root.withdraw()

    filename = "myifc.ifc"

    filename = filedialog.asksaveasfile(defaultextension=".ifc", filetypes=[('ifc', '.ifc'),])
    if filename is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        print("cancel save as")
        return
    print(filename)




    temp_filename = ifc_tools.create_temp_ifc()

    # Obtain references to instances defined in template
    ifcfile = ifcopenshell.open(temp_filename)
    owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
    project = ifcfile.by_type("IfcProject")[0]
    context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]
    ifcfile.context = context
    # IFC hierarchy creation
    site_placement = ifc_tools.create_ifclocalplacement(ifcfile)
    site = ifcfile.createIfcSite(ifc_tools.create_guid(), owner_history, "Site", None, None, site_placement, None, None,
                                 "ELEMENT", None, None, None, None, None)

    building_placement = ifc_tools.create_ifclocalplacement(ifcfile, relative_to=site_placement)
    building = ifcfile.createIfcBuilding(ifc_tools.create_guid(), owner_history, 'Building', None, None,
                                         building_placement, None,
                                         None, "ELEMENT", None, None, None)

    storey_placement = ifc_tools.create_ifclocalplacement(ifcfile, relative_to=building_placement)
    ifcfile.storey_placement = storey_placement
    elevation = 0.0
    building_storey = ifcfile.createIfcBuildingStorey(ifc_tools.create_guid(), owner_history, 'Storey', None, None,
                                                      storey_placement, None, None, "ELEMENT", elevation)

    container_storey = ifcfile.createIfcRelAggregates(ifc_tools.create_guid(), owner_history, "Building Container",
                                                      None,
                                                      building, [building_storey])
    container_site = ifcfile.createIfcRelAggregates(ifc_tools.create_guid(), owner_history, "Site Container", None,
                                                    site,
                                                    [building])
    container_project = ifcfile.createIfcRelAggregates(ifc_tools.create_guid(), owner_history, "Project Container",
                                                       None, project,
                                                       [site])

    model = app.model_reg

    ifc_bars = []
    ifc_ent = None
    for entity_bar in model.get_bars():

        ifc_ent = entity_bar.generate_ifc(ifcfile)
        ifc_bars += [ifc_ent]

    print("debugggg")
    print(type([ifc_ent]))
    print(type(list(ifc_ent)))
    print(len(ifc_bars))

    # Relate the window and wall to the building storey
    ifcfile.createIfcRelContainedInSpatialStructure(ifc_tools.create_guid(), owner_history,
                                                    "Building Storey Container", None,
                                                    ifc_bars, building_storey)

    # Write the contents of the file to disk
    ifcfile.write(filename.name)


@command(name="save_ifc", shortcut="s")
def save_ifc():
    print("----------------------------------------------------")
    print("save()")
    filename = "myifc.ifc"
    temp_filename = create_temp_ifc()

    # Obtain references to instances defined in template
    ifcfile = ifcopenshell.open(temp_filename)
    owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
    project = ifcfile.by_type("IfcProject")[0]
    context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]
    ifcfile.context = context
    # IFC hierarchy creation
    site_placement = ifc_tools.create_ifclocalplacement(ifcfile)
    site = ifcfile.createIfcSite(ifc_tools.create_guid(), owner_history, "Site", None, None, site_placement, None, None,
                                 "ELEMENT", None, None, None, None, None)

    building_placement = ifc_tools.create_ifclocalplacement(ifcfile, relative_to=site_placement)
    building = ifcfile.createIfcBuilding(ifc_tools.create_guid(), owner_history, 'Building', None, None, building_placement, None,
                                         None, "ELEMENT", None, None, None)

    storey_placement = ifc_tools.create_ifclocalplacement(ifcfile, relative_to=building_placement)
    ifcfile.storey_placement = storey_placement
    elevation = 0.0
    building_storey = ifcfile.createIfcBuildingStorey(ifc_tools.create_guid(), owner_history, 'Storey', None, None,
                                                      storey_placement, None, None, "ELEMENT", elevation)

    container_storey = ifcfile.createIfcRelAggregates(ifc_tools.create_guid(), owner_history, "Building Container", None,
                                                      building, [building_storey])
    container_site = ifcfile.createIfcRelAggregates(ifc_tools.create_guid(), owner_history, "Site Container", None, site,
                                                    [building])
    container_project = ifcfile.createIfcRelAggregates(ifc_tools.create_guid(), owner_history, "Project Container", None, project,
                                                       [site])

    # Wall creation: Define the wall shape as a polyline axis and an extruded area solid
    wall_placement = ifc_tools.create_ifclocalplacement(ifcfile, relative_to=storey_placement)
    polyline = ifc_tools.create_ifcpolyline(ifcfile, [(0.0, 0.0, 0.0), (5.0, 0.0, 0.0)])
    axis_representation = ifcfile.createIfcShapeRepresentation(context, "Axis", "Curve2D", [polyline])

    extrusion_placement = ifc_tools.create_ifcaxis2placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))
    point_list_extrusion_area = [(0.0, -0.1, 0.0), (5.0, -0.1, 0.0), (5.0, 0.1, 0.0), (0.0, 0.1, 0.0), (0.0, -0.1, 0.0)]
    solid = ifc_tools.create_ifcextrudedareasolid(ifcfile, point_list_extrusion_area, extrusion_placement, (0.0, 0.0, 1.0), 3.0)
    body_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [solid])

    product_shape = ifcfile.createIfcProductDefinitionShape(None, None, [axis_representation, body_representation])

    wall = ifcfile.createIfcWallStandardCase(ifc_tools.create_guid(), owner_history, "Wall", "An awesome wall", None,
                                             wall_placement, product_shape, None)
    """
    Creamos una entidad con el comando create_entity
    Los argumentos que se pueden usar están definidos en el archivo 'ifcopenshell/express/DocAttribute.csv'
    
    Los posibles tipos de entidad están en el archivo 'ifcopenshell/express/DocEntity.csv'
    
    
    """

    product_shape = ifcfile.createIfcProductDefinitionShape(None, None, [axis_representation, body_representation])
    placement = ifc_tools.create_ifclocalplacement(ifcfile, relative_to=storey_placement, point=(0., 2., 0.), dir1=(0., 1., 1.))
    polyline = ifc_tools.create_ifcpolyline(ifcfile, [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)])
    axis_representation = ifcfile.create_entity(type="IfcShapeRepresentation",
                                                ContextOfItems=context,
                                                RepresentationIdentifier="Axis",
                                                RepresentationType="Curve2D",
                                                Items=[polyline])

    extrusion_placement = ifc_tools.create_ifcaxis2placement(ifcfile, (0.0, 0.0, 0.0))
    point_list_extrusion_area = [(0.0, -0.1, 0.0),
                                 (1.5, -0.1, 0.0),
                                 (1.5, 0.1, 0.0),
                                 (0.0, 0.1, 0.0),
                                 (0.0, -0.1, 0.0)]
    solid = ifc_tools.create_ifcextrudedareasolid(ifcfile, point_list_extrusion_area, extrusion_placement, (0.0, 0.0, 1.0), 3.0)

    body_representation = ifcfile.createIfcShapeRepresentation(ContextOfItems=context,
                                                               RepresentationIdentifier="Body",
                                                               RepresentationType="SweptSolid",
                                                               Items=[solid])

    product_shape = ifcfile.createIfcProductDefinitionShape(Representations=[axis_representation, body_representation])

    pilar = ifcfile.create_entity(type="IfcColumn",
                                  GlobalId=ifc_tools.create_guid(),
                                  OwnerHistory=owner_history,
                                  Name="Mi Columna",
                                  Description="Soy una columna",
                                  ObjectPlacement=placement,
                                  Representation=product_shape
                                  )

    #pilar["GlobalId"] = create_guid()
    #pilar["OwnerHistory"] = owner_history
    #pilar["Name"] = "Mi Columna"
    #pilar["Description"] = "Soy una columna"


    print("pilar")

    #print(pilar)
    ##print(wall)
    #print(wall.__dict__)
    print(wall.__dict__)

    # Define and associate the wall material
    material = ifcfile.createIfcMaterial("wall material")
    material_layer = ifcfile.createIfcMaterialLayer(material, 0.2, None)
    material_layer_set = ifcfile.createIfcMaterialLayerSet([material_layer], None)
    material_layer_set_usage = ifcfile.createIfcMaterialLayerSetUsage(material_layer_set, "AXIS2", "POSITIVE", -0.1)
    ifcfile.createIfcRelAssociatesMaterial(ifc_tools.create_guid(), owner_history, RelatedObjects=[wall, pilar],
                                           RelatingMaterial=material_layer_set_usage)

    # Create and assign property set
    property_values = [
        ifcfile.createIfcPropertySingleValue("Reference", "Reference",
                                             ifcfile.create_entity("IfcText", "Describe the Reference"), None),
        ifcfile.createIfcPropertySingleValue("IsExternal", "IsExternal", ifcfile.create_entity("IfcBoolean", True),
                                             None),
        ifcfile.createIfcPropertySingleValue("ThermalTransmittance", "ThermalTransmittance",
                                             ifcfile.create_entity("IfcReal", 2.569), None),
        ifcfile.createIfcPropertySingleValue("IntValue", "IntValue", ifcfile.create_entity("IfcInteger", 2), None)
    ]
    property_set = ifcfile.createIfcPropertySet(ifc_tools.create_guid(), owner_history, "Pset_WallCommon", None, property_values)
    ifcfile.createIfcRelDefinesByProperties(ifc_tools.create_guid(), owner_history, None, None, [wall], property_set)

    # Add quantity information
    quantity_values = [
        ifcfile.createIfcQuantityLength("Length", "Length of the wall", None, 5.0),
        ifcfile.createIfcQuantityArea("Area", "Area of the front face", None, 5.0 * solid.Depth),
        ifcfile.createIfcQuantityVolume("Volume", "Volume of the wall", None,
                                        5.0 * solid.Depth * material_layer.LayerThickness)
    ]
    element_quantity = ifcfile.createIfcElementQuantity(ifc_tools.create_guid(), owner_history, "BaseQuantities", None, None,
                                                        quantity_values)
    ifcfile.createIfcRelDefinesByProperties(ifc_tools.create_guid(), owner_history, None, None, [wall], element_quantity)

    # Create and associate an opening for the window in the wall
    opening_placement = ifc_tools.create_ifclocalplacement(ifcfile, (0.5, 0.0, 1.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0),
                                                           wall_placement)
    opening_extrusion_placement = ifc_tools.create_ifcaxis2placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))
    point_list_opening_extrusion_area = [(0.0, -0.1, 0.0), (3.0, -0.1, 0.0), (3.0, 0.1, 0.0), (0.0, 0.1, 0.0),
                                         (0.0, -0.1, 0.0)]
    opening_solid = ifc_tools.create_ifcextrudedareasolid(ifcfile, point_list_opening_extrusion_area, opening_extrusion_placement,
                                                          (0.0, 0.0, 1.0), 1.0)
    opening_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [opening_solid])
    opening_shape = ifcfile.createIfcProductDefinitionShape(None, None, [opening_representation])
    opening_element = ifcfile.createIfcOpeningElement(ifc_tools.create_guid(), owner_history, "Opening", "An awesome opening",
                                                      None, opening_placement, opening_shape, None)
    ifcfile.createIfcRelVoidsElement(ifc_tools.create_guid(), owner_history, None, None, wall, opening_element)

    # Create a simplified representation for the Window
    window_placement = ifc_tools.create_ifclocalplacement(ifcfile,
                                                          (0.0, 0.0, 0.0),
                                                          (0.0, 0.0, 1.0),
                                                          (1.0, 0.0, 0.0),
                                                          opening_placement)
    window_extrusion_placement = ifc_tools.create_ifcaxis2placement(ifcfile,
                                                                    (0.0, 0.0, 0.0),
                                                                    (0.0, 0.0, 1.0),
                                                                    (1.0, 0.0, 0.0))
    point_list_window_extrusion_area = [(0.0, -0.01, 0.0), (3.0, -0.01, 0.0), (3.0, 0.01, 0.0), (0.0, 0.01, 0.0),
                                        (0.0, -0.01, 0.0)]
    window_solid = ifc_tools.create_ifcextrudedareasolid(ifcfile,
                                                         point_list_window_extrusion_area,
                                                         window_extrusion_placement,
                                                         (0.0, 0.0, 1.0),
                                                         1.0)
    window_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [window_solid])
    window_shape = ifcfile.createIfcProductDefinitionShape(None, None, [window_representation])
    window = ifcfile.createIfcWindow(ifc_tools.create_guid(), owner_history, "Window", "An awesome window", None,
                                     window_placement, window_shape, None, None)

    # Relate the window to the opening element
    ifcfile.createIfcRelFillsElement(ifc_tools.create_guid(), owner_history, None, None, opening_element, window)

    # Relate the window and wall to the building storey
    ifcfile.createIfcRelContainedInSpatialStructure(ifc_tools.create_guid(), owner_history, "Building Storey Container", None,
                                                    [wall, window, pilar], building_storey)

    # Write the contents of the file to disk
    ifcfile.write(filename)


def create_temp_ifc() -> str:
    filename = "hello_wall.ifc"
    timestamp = time.time()
    timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
    creator = "Kianwee Chen"
    organization = "NUS"
    application, application_version = "IfcOpenShell", "0.5"
    project_globalid, project_name = ifc_tools.create_guid(), "Hello Wall"

    # A template IFC file to quickly populate entity instances for an IfcProject with its dependencies
    template = """ISO-10303-21;
        HEADER;
        FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
        FILE_NAME('%(filename)s','%(timestring)s',('%(creator)s'),('%(organization)s'),'%(application)s','%(application)s','');
        FILE_SCHEMA(('IFC2X3'));
        ENDSEC;
        DATA;
        #1=IFCPERSON($,$,'%(creator)s',$,$,$,$,$);
        #2=IFCORGANIZATION($,'%(organization)s',$,$,$);
        #3=IFCPERSONANDORGANIZATION(#1,#2,$);
        #4=IFCAPPLICATION(#2,'%(application_version)s','%(application)s','');
        #5=IFCOWNERHISTORY(#3,#4,$,.ADDED.,$,#3,#4,%(timestamp)s);
        #6=IFCDIRECTION((1.,0.,0.));
        #7=IFCDIRECTION((0.,0.,1.));
        #8=IFCCARTESIANPOINT((0.,0.,0.));
        #9=IFCAXIS2PLACEMENT3D(#8,#7,#6);
        #10=IFCDIRECTION((0.,1.,0.));
        #11=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#9,#10);
        #12=IFCDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);
        #13=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
        #14=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
        #15=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
        #16=IFCSIUNIT(*,.PLANEANGLEUNIT.,$,.RADIAN.);
        #17=IFCMEASUREWITHUNIT(IFCPLANEANGLEMEASURE(0.017453292519943295),#16);
        #18=IFCCONVERSIONBASEDUNIT(#12,.PLANEANGLEUNIT.,'DEGREE',#17);
        #19=IFCUNITASSIGNMENT((#13,#14,#15,#18));
        #20=IFCPROJECT('%(project_globalid)s',#5,'%(project_name)s',$,$,$,$,(#11),#19);
        ENDSEC;
        END-ISO-10303-21;
        """ % locals()
    # Write the template to a temporary file
    temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
    data = template.encode()
    print(temp_filename)
    with open(temp_filename, "wb") as f:
        f.write(data)



    return temp_filename
