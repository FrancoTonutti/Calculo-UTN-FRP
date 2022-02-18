from enum import Enum

import pint

from app import app
from app.model.transaction import Transaction

from app.view.interface.color_scheme import *
from app.view.simpleui import SimpleScrolledFrame, SimpleLabel, SimpleButton, \
    SimpleCheckBox, SimpleEntry

from app.view import simpleui
from app.controller.console import command, execute

def create_label_fullsize(text, parent, padding=None, margin=None, alpha=0):
    #font_panda3d, font_pil = draw.draw_get_font()
    #width, height = font_pil.getsize(text)
    #size = [20 + width, 19]

    if padding is None:
        padding = [0, 0, 0, 0]

    if margin is None:
        margin = [0, 0, 0, 0]

    label = SimpleLabel(
        text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
        orginV="bottom",
        text_scale=(12, 12),
        text=text,
        parent=parent,
        sizeHint=[None, None],
        size=[None, None],
        frameColor="C_WHITE",
        alpha=alpha,
        align="left",
        textCenterX=False,
        padding=padding,
        margin=margin

    )

    return label


def create_label(text, parent, padding=None, margin=None, alpha=0, font_size=12):
    font_panda3d, font_pil = draw.draw_get_font(font_size=font_size)
    width, height = font_pil.getsize(text)
    size = [20 + width, 19]

    if padding is None:
        padding = [0, 0, 0, 0]

    if margin is None:
        margin = [0, 0, 0, 0]

    size = [20 + width, height + padding[2] + padding[3]]

    label = SimpleLabel(
        text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
        orginV="bottom",
        position=[0, 0],
        fontSize=font_size,
        text=text,
        parent=parent,
        size=size,
        frameColor="C_WHITE",
        alpha=alpha,
        align="left",
        textCenterX=False,
        padding=padding,
        margin=margin

    )

    return label

def new_button(text, colors=None, command=None, args=None, parent=None, size=None, padding=None, margin=None):
    if args is None:
        args = []
    font_panda3d, font_pil = draw.draw_get_font()
    if colors is None:
        col_rollover = draw.merge_color(COLOR_SEC_DARK, COLOR_MAIN_LIGHT, 0.8)
        colors = [COLOR_SEC_DARK, COLOR_MAIN_LIGHT, col_rollover, COLOR_MAIN_LIGHT]
    if size is None:
        width = font_pil.getsize(text)[0]
        size = [20+width, 25]
    if padding is None:
        padding = [20, 20, 0, 0]

    if margin is None:
        margin = [0, 0, 0, 0]

    btn = SimpleButton(text=text,
                       text_scale=(12, 12),
                       text_font=font_panda3d,
                       text_fg=draw.get_color(COLOR_TEXT_LIGHT, "rgba"),
                       command=command,
                       parent=parent,
                       extraArgs=args,
                       colorList=colors,
                       position=[0, 0],
                       padding=padding,
                       size=size,
                       margin=margin
                       )

    return btn


class Table:
    def __init__(self, titles, parent, model, params, enable_detete=True, ev_set_attr=None, ev_delete_entity=None):
        frame_scrolled = SimpleScrolledFrame(

            position=[0, 0],
            canvasSize=(0, 100, -200, 0),
            parent=parent,
            layout="GridLayout",
            layoutDir="X",
            gridCols=max(len(titles), 1),
            gridRows=2,
            frameColor=scheme_rgba(COLOR_MAIN_LIGHT),
            alpha=1
        )
        self.canvas = frame_scrolled.getCanvas()

        self.frame = frame_scrolled
        self.model = model
        self.params = params
        self.data_fields = list()
        self.titles = titles
        self.ev_set_attr = ev_set_attr
        self.enable_detete = enable_detete
        self.update_table()

        self.ev_delete_entity = ev_delete_entity

    def update_table(self):
        for fields in self.data_fields:
            for field in fields:
                field.destroy()
        self.data_fields.clear()

        if self.enable_detete and self.titles[-1] != "Eliminar":
            self.titles.append("Eliminar")

        if self.frame["gridCols"] != max(len(self.titles), 1):
            self.frame["gridCols"] = max(len(self.titles), 1)

        if isinstance(self.model, str):
            panda3d = app.get_show_base()
            # Obtenemos el registro del modelo
            model_reg = app.model_reg
            entities = model_reg.find_entities(self.model)
            entities = sorted(entities, key=lambda x: x.index)
        else:
            entities = self.model
            entities = sorted(entities, key=lambda x: x.index)

        field_list = list()
        for title in self.titles:
            label = create_label(title, self.canvas)
            field_list.append(label)
        self.data_fields.append(field_list)

        for entity in entities:
            field_list = list()
            for param in self.params:
                field = self.add_field(entity, param, getattr(entity, param))
                field_list.append(field)

            if self.enable_detete:
                close_btn = new_button("x", parent=self.canvas, padding=[5,5,5,5],
                                       command=self.delete_enity, args=[entity])
                field_list.append(close_btn)

            self.data_fields.append(field_list)


        self.frame["gridRows"] = len(self.data_fields)+1
        simpleui.update_ui()

    def delete_enity(self, entity):
        entity.delete()
        self.update_table()

        if self.ev_delete_entity:
            self.ev_delete_entity()

    def entity_set_prop(self, new_value: any, entity, name: str):
        old_value = getattr(entity, name, None)

        if new_value != "" and isinstance(old_value, float):
            new_value = float(new_value)

        if new_value != "" and isinstance(old_value, int):
            new_value = int(new_value)

        if isinstance(old_value, bool):
            if new_value == "True":
                new_value = True
            elif new_value == "False":
                new_value = False

        if old_value == new_value or new_value == "None":
            return None

        if type(old_value) is type(new_value):
            if entity is not None:
                print("atributo establecido {}: {}".format(name, new_value))
                setattr(entity, name, new_value)
                print("verif {}: {}".format(name, getattr(entity, name,
                                                          "undefined")))


                if self.ev_set_attr:
                    self.ev_set_attr()
        else:
            if entity is not None:
                print("El tipo de asignación no corresponde: {},{}->{}".format(
                    name, type(old_value), type(new_value)))

    def add_field(self, entity, prop: str, value=0):
        if isinstance(value, bool):
            entry = SimpleCheckBox(
                position=[0, 0],
                size=[None, 20],
                sizeHint=[0.50, None],
                parent=self.canvas,
                command=self.entity_set_prop,
                extraArgs=[entity, prop],
                value=value,
                frameColor="C_WHITE",
                maxSize=16
            )

        else:

            if entity.is_read_only(prop):
                entry = create_label(str(value), self.canvas)
            else:
                entry = SimpleEntry(
                    text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
                    orginH="center",
                    position=[0, 0],
                    text_scale=(12, 12),
                    width=20,
                    align="left",
                    textCenterX=False,
                    command=self.entity_set_prop,
                    extraArgs=[entity, prop],
                    focusOutCommand=self.entity_set_prop,
                    focusOutExtraArgs=[entity, prop],
                    parent=self.canvas,
                    size=[None, 20],
                    padding=[15, 0, 0, 0],
                    sizeHint=[1, None],
                    frameColor="C_WHITE",
                    alpha=0,
                    initialText=str(value)
                )
        return entry






class PropEditor:
    def __init__(self, parent, width=300, update_event=None):
        self.frame = SimpleScrolledFrame(#position=[0, 0],
                                         canvasSize=(0, width, -100, 0),
                                         size=[None, None],
                                         sizeHint=[None, None],
                                         parent=parent,
                                         frameColor=scheme_rgba(COLOR_SEC_DARK),
                                         alpha=1,
                                         margin=[0, 0, 0, 0],
                                         layout="GridLayout",
                                         layoutDir="X",
                                         gridCols=2,
                                         gridRows=10)

        self.fields = []
        self.entity = None
        self.update_event = update_event


    def add_property(self, prop: str, fieldname: str, value=0):

        label = SimpleLabel(
            text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
            orginV="bottom",
            position=[0, 0],
            text_scale=(12, 12),
            text=fieldname,
            parent=self.frame.getCanvas(),
            size=[None, 20],
            sizeHint=[0.50, None],
            frameColor=scheme_rgba(COLOR_MAIN_LIGHT),
            alpha=1,
            align="left",
            textCenterX=False,
            padding=[10, 0, -3, 3]

        )
        if isinstance(value, bool):
            if self.entity.is_read_only(prop):
                set_text = str(value)
                entry = SimpleLabel(
                    text_fg=scheme_rgba(COLOR_TEXT_LIGHT_FADE),
                    orginH="center",
                    orginV="bottom",
                    position=[0, 0],
                    fontSize=12,
                    text=set_text,
                    parent=self.frame.getCanvas(),
                    size=[None, 20],
                    sizeHint=[0.50, None],
                    frameColor="C_WHITE",
                    alpha=0,
                    align="left",
                    textCenterX=False,
                    padding=[10, 0, -3, 3]

                )
            else:
                entry = SimpleCheckBox(
                    position=[0, 0],
                    size=[None, 20],
                    sizeHint=[0.50, None],
                    parent=self.frame.getCanvas(),
                    command=self.entity_set_prop,
                    extraArgs=[prop],
                    value=value,
                    frameColor="C_WHITE",
                    maxSize=14,
                    alpha=0,
                    colorDisabled=(102/255, 102/255, 102/255, 1),
                    colorEnabled=(82 / 255, 120 / 255, 180 / 255, 1),
                    padding=[10, 0, -3, 3]
                )
        else:
            if self.entity.is_read_only(prop):
                if isinstance(value, pint.quantity.Quantity):
                    set_text = "\1slant\1{}\2".format(format(value, '~'))

                else:
                    set_text = str(value)

                entry = SimpleLabel(
                    text_fg=scheme_rgba(COLOR_TEXT_LIGHT_FADE),
                    orginH="center",
                    orginV="bottom",
                    position=[0, 0],
                    text_scale=(12, 12),
                    text=set_text,
                    parent=self.frame.getCanvas(),
                    size=[None, 20],
                    sizeHint=[0.50, None],
                    frameColor="C_WHITE",
                    alpha=0,
                    align="left",
                    textCenterX=False,
                    padding=[10, 0, -3, 3]

                )

            else:
                initial_value = str(value)
                value_unit = ""
                if isinstance(value, pint.quantity.Quantity):
                    initial_value = str(value.magnitude)
                    value_unit = " [{}]".format(format(value.u, '~'))
                elif isinstance(value, Enum):
                    initial_value = str(value.value)
                    value_unit = " ({})".format(value.name)

                entry = SimpleEntry(
                    text_fg=scheme_rgba(COLOR_TEXT_LIGHT),
                    orginH="center",
                    position=[0, 0],
                    text_scale=(12, 12),
                    width=20,
                    align="left",
                    textCenterX=False,
                    command=self.entity_set_prop,
                    extraArgs=[prop],
                    focusOutCommand=self.entity_set_prop,
                    focusOutExtraArgs=[prop],
                    parent=self.frame.getCanvas(),
                    size=[None, 20],
                    sizeHint=[0.50, None],
                    frameColor="C_WHITE",
                    initialText=initial_value,
                    alpha=0,
                    padding=[10, 0, -3, 3],
                    suffix=value_unit

                )
        self.fields.append([label, entry])

    def entity_set_prop(self, new_value: any, name: str):
        old_value = getattr(self.entity, name, None)
        force_set = False

        if isinstance(old_value, bool):

            if new_value == "True":
                new_value = True
            elif new_value == "False":
                new_value = False
        elif new_value != "" and isinstance(old_value, float) and new_value.isnumeric():
            new_value = float(new_value)

        elif new_value != "" and isinstance(old_value, int) and new_value.isnumeric():
            new_value = int(new_value)

        elif new_value != "" and isinstance(old_value,
                                            pint.quantity.Quantity) and new_value.isnumeric():
            new_value = float(new_value) * app.ureg(str(old_value.units))

        if isinstance(old_value, Enum):
            if new_value.isnumeric():
                try:
                    new_value = type(old_value)(int(new_value))
                except ValueError:
                    new_value = old_value
                    force_set = True

        if old_value == new_value and not force_set:
            return None

        if type(old_value) is type(new_value):
            if self.entity is not None:
                print(
                    "atributo establecido {}: {}".format(name, new_value))
                tr = Transaction()
                tr.start("Edit propery")
                setattr(self.entity, name, new_value)
                tr.commit()
                print("verif {}: {}".format(name,
                                            getattr(self.entity,
                                                    name, "undefined")))

                if isinstance(old_value, Enum):
                    self.entity_read(self.entity)

        else:
            if self.entity is not None:
                print(
                    "El tipo de asignación no corresponde: {},{}->{}".format(
                        name, type(old_value), type(new_value)))

        if self.update_event:
            self.update_event()
        #self.update_list()

    def entity_read(self, entity):

        for label, entry in self.fields:
            if hasattr(entry, "enter_value"):
                if entry['focus'] is True:
                    entry.defocus()

        for label, entry in self.fields:
            label.destroy()
            entry.destroy()

        self.fields.clear()

        self.entity = entity
        if entity:
            for prop in self.entity.get_properties():
                self.add_property(prop, self.entity.prop_name(prop),
                                  getattr(self.entity, prop))

        execute("regen_ui")
