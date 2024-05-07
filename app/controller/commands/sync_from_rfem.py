import time
from typing import List

from RFEM.enums import ObjectTypes

from app.model import Load, Line, MouseEventHandler, Node, Bar, Section, \
    SectionType, ProfileShapeHollowRect
from direct.task.Task import TaskManager
from app import app

from panda3d.core import LineSegs, NodePath
import numpy as np

from app.controller.console import command, execute
import pint

from app.model import unit_manager
from app.model.entity_reference import EntityReference
from app.model.events import EventListener
from app.model.level import Level
from app.model.transaction import TM, Transaction
from app.view.interface.properties import PropEditorModes


from RFEM.enums import MemberSectionDistributionType, \
    MemberRotationSpecificationType, NodalSupportType, \
    SurfaceLoadDistributionDirection, SurfaceLoadDirection, ObjectTypes
from RFEM.initModel import Model, Calculate_all
from RFEM.BasicObjects.node import Node as RFEM_Node
from RFEM.BasicObjects.line import Line as RFEM_Line
from RFEM.BasicObjects.material import Material as RFEM_Material
from RFEM.BasicObjects.section import Section as RFEM_Section
from RFEM.BasicObjects.member import Member as RFEM_Member
from RFEM.BasicObjects.surface import Surface as RFEM_Surface
from RFEM.TypesForNodes.nodalSupport import NodalSupport
from RFEM.enums import MemberType


@command(name="sync_from_rfem")
def sync_from_rfem():

    tr = Transaction()
    tr.start("Sync RFEM")

    Model(new_model=False, model_name="deck conjunto v3")
    service = Model.clientModel.service
    Model.clientModel.service.begin_modification()

    z = 0

    status_bar = app.main_ui.status_bar
    status_bar.set_status_hint("Sincronizando")

    #section = Section.last_section

    #print("SECCION----{}".format(section.__str__()))
    """node_start = Node(0, 0)
    node_start.hide()
    node_end = Node(1, 0)
    node_end.hide()
    new_line = Line(node_start, node_end)
    new_line.hide()

    node_start.is_selectable = False
    node_end.is_selectable = False
    new_line.is_selectable = False"""

    prop_editor = app.main_ui.prop_editor
    prop_editor.deselect_all()
    #prop_editor.set_mode(PropEditorModes.CREATE)
    #prop_editor.entity_read(new_line)

    #handler = MouseEventHandler()

    #events = EventListener()
    #cache = {"handler": handler, "new_line": new_line, "start": node_start, "end": node_end, "step": 0, "events": events, "on_select": None}
    cache = {"service": service}
    #events.add_listener("onselect", on_select, args=[cache])

    app.console.start_command(sync_task, "Sync RFEM", cache)


node_pos_cache = {}
section_names = {}


def get_section_name(service, number):
    global section_names
    number = str(number)

    if number not in section_names.keys():
        section = service.get_section(number)
        name = section.name
        comment = section.comment

        if name is None:
            name = "RSECTION_{}".format(number)
        section_names.update({number: {"name": name, "comment": comment}})

    return section_names.get(number)


def get_node_pos(service, number):
    global node_pos_cache
    number = str(number)

    if number not in node_pos_cache.keys():
        node = service.get_node(number)

        x = node.global_coordinate_1
        y = node.global_coordinate_2
        z = node.global_coordinate_3

        ret = [x, y, z]
        node_pos_cache.update({number: [x, y, z]})
    else:
        ret = node_pos_cache.get(number)

    if ret is None:
        a = number not in section_names.keys()
        b = service.get_node(number)
        print("\n\n")
        print(ret)
        print(b)
        raise Exception("none check {}".format(a))

    return ret


eccentricity_data = {}


def get_eccentricity(service, number):
    global eccentricity_data
    number = str(number)

    if number not in eccentricity_data.keys():
        try:
            ecc = service.get_member_eccentricity(number)
            #print(number)

            if ecc.specification_type == "TYPE_RELATIVE":
                ecc_data = {
                    "specification_type": ecc.specification_type,
                    "vertical_section_alignment": ecc.vertical_section_alignment,
                    "horizontal_section_alignment": ecc.horizontal_section_alignment,
                }
            else:
                ecc_data = {
                    "specification_type": ecc.specification_type,
                    "coordinate_system": ecc.coordinate_system,
                    "offset_x": ecc.offset_x,
                    "offset_y": ecc.offset_y,
                    "offset_z": ecc.offset_z,
                }
            eccentricity_data.update({number: ecc_data})
        except Exception as ex:

            print(type(number))
            print(ecc)
            raise Exception(ex)

    return eccentricity_data.get(number)


def sync_task(task, cache: dict):
    tr = TM.get_root_transaction()
    active_tr = TM.get_active_transaction()
    if tr.name == "Sync RFEM":
        panda3d = app.get_show_base()
        prop_editor = app.main_ui.prop_editor
        status_bar = app.main_ui.status_bar

        #active_tr.disable_register()
        #active_tr.enable_register()

        # service = cache.get("service")
        service = Model.clientModel.service

        node_numbers = service.get_all_object_numbers(ObjectTypes.E_OBJECT_TYPE_NODE.name)
        node_numbers = node_numbers.split(" ")
        totals = len(node_numbers)
        i = 1
        check_abort = True

        node_mapping = {}

        for node_number in node_numbers:
            # continue
            start_time = time.time()

            rfem_node = service.get_node(node_number)
            x = rfem_node.global_coordinate_1
            y = rfem_node.global_coordinate_2
            z = rfem_node.global_coordinate_3

            node = Node(x, -y, -z)
            node.set_external_id_mapping("RFEM", node_number)

            node_mapping.update({str(node_number): node})


            end_time = time.time()
            time_elapsed = (end_time - start_time)
            print("Avance: {} / {} deltatime: {}\r".format(i, totals, time_elapsed), end="")

            i += 1
            if time_elapsed > 1:
                if check_abort:
                    raise Exception("La operacion consumio {} s".format(time_elapsed))

        ###################################################

        member_numbers = service.get_all_object_numbers(
            ObjectTypes.E_OBJECT_TYPE_MEMBER.name)
        member_numbers = member_numbers.split(" ")
        totals = len(member_numbers)
        i = 1
        check_abort = True

        member_mapping = {}

        for member_number in member_numbers:
            # continue
            start_time = time.time()

            rfem_member = service.get_member(member_number)

            section_comment = None
            # print(member)
            if hasattr(rfem_member, "section_start"):
                section_data = get_section_name(service, rfem_member.section_start)
                rfem_section_name = section_data.get("name")
                section_comment = section_data.get("comment")


            else:
                rfem_section_name = None

            ecc_start = None

            if hasattr(rfem_member, "member_eccentricity_start"):

                ecc_number = rfem_member.member_eccentricity_start
                ecc_number = int(ecc_number)
                if ecc_number > 0:
                    ecc_start = get_eccentricity(service, ecc_number)

            ecc_end = None

            if hasattr(rfem_member, "member_eccentricity_end"):

                ecc_number = rfem_member.member_eccentricity_end
                ecc_number = int(ecc_number)
                if ecc_number > 0:
                    ecc_end = get_eccentricity(service, ecc_number)

            # print(section)
            node_start = node_mapping.get(str(rfem_member.node_start))
            node_end = node_mapping.get(str(rfem_member.node_end))

            section = Section.last_section

            if rfem_section_name:
                stype = None
                print(rfem_section_name)

                if rfem_section_name.startswith("SHS"):
                    # Ex: SHS 100/2.5/5/2.5/H
                    rfem_section_name = rfem_section_name.replace(" ", "/")
                    stype, b, t, r0, ri, _ = rfem_section_name.split("/")
                    h = b
                if rfem_section_name.startswith("RHS"):
                    # Ex: RHS 100/50/2/4/2/H
                    rfem_section_name = rfem_section_name.replace(" ", "/")
                    stype, h, b, t, r0, ri, _ = rfem_section_name.split("/")



                if stype == "SHS" or stype == "RHS":
                    model = app.model_reg

                    section_types: List[SectionType] = model.find_entities("SectionType")
                    selected_section_type = None
                    for section_type in section_types:
                        if section_type.name == stype:
                            selected_section_type = section_type
                            #print("Found Section Type {}".format(stype))
                            break
                    else:
                        #print("Create Section Type {}".format(stype))
                        selected_section_type = SectionType(stype)
                        shapes = selected_section_type.valid_values_shape()
                        for shape in shapes:
                            if isinstance(shape, ProfileShapeHollowRect):
                                selected_section_type.shape = shape

                    if selected_section_type:  # type: SectionType
                        sec_name = "{}x{}x{}mm".format(
                            int(float(h)*1000),
                            int(float(b)*1000),
                            round(float(t)*1000)
                        )
                        section_list: List[Section] = selected_section_type.get_sections()
                        found_section = None
                        for sec in section_list:
                            if sec.name == sec_name:
                                found_section = sec
                                break
                            #sec.geometry

                        if found_section:
                            section = found_section
                        else:
                            section = Section(sec_name, selected_section_type,
                                    {"b": "{} mm".format(round(float(b)*1000, 2)),
                                              "h": "{} mm".format(round(float(h)*1000, 2)),
                                              "t": "{} mm".format(round(float(t)*1000, 2))})





            if node_start is None:
                print("None node start")
                print(rfem_member.node_start)

            if node_end is None:
                print("None node end")
                print(rfem_member.node_end)

            bar = Bar(node_start, node_end, section)

            data_element = {
                # "rfem_type": "member"
                "rfem_id": rfem_member.id_for_export_import,
                "rfem_number": member_number,
                "rotation": rfem_member.rotation_angle,
                "start": get_node_pos(service, rfem_member.node_start),
                "end": get_node_pos(service, rfem_member.node_end),
                "section": section,
                "ecc_start": ecc_start,
                "ecc_end": ecc_end,
                "section_comment": section_comment
            }




            #member = Node(x, y, -z)
            #member.set_external_id_mapping("RFEM", member_number)

            #node_mapping.update({member_number: member})

            end_time = time.time()
            time_elapsed = (end_time - start_time)
            print("Avance: {} / {} deltatime: {}\r".format(i, totals,
                                                           time_elapsed),
                  end="")

            i += 1
            if time_elapsed > 1:
                if check_abort:
                    raise Exception(
                        "La operacion consumio {} s".format(time_elapsed))

        return sync_rfem_end(task)
    else:
        print("ROOT TRANSACTION ERROR")
        cache.clear()
        return sync_rfem_end(task)


def sync_rfem_end(task):
    status_bar = app.main_ui.status_bar
    status_bar.set_status_hint("")
    prop_editor = app.main_ui.prop_editor
    prop_editor.set_mode(PropEditorModes.EDIT)

    Model.clientModel.service.finish_modification()
    return task.done
