"""
Test the Item class.

File:       test_005_item.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2024 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Element
from test_data import item_value_set
from test_setup import filesystem, parts_file_close, parts_file_create

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Item
from pages import table_definition

parts_filename = "parts_test.parts"
item_values = {
    "record_id": item_value_set[0][0],
    "part_number": item_value_set[0][1],
    "assembly": item_value_set[0][2],
    "quantity": item_value_set[0][3],
    "condition": item_value_set[0][4],
    "installed": item_value_set[0][5],
    "box": item_value_set[0][6],
    "remarks": item_value_set[0][7],
}


def base_setup(filesystem):
    filename = filesystem + "/" + parts_filename
    parts_file = parts_file_create(filename, table_definition)
    item = Item(parts_file)
    return (item, parts_file)


def test_005_01_constr(filesystem):
    """
    Item Extends Element.

    Check the types of class variables and default values.
    """
    item, parts_file = base_setup(filesystem)
    assert isinstance(item, Item)
    assert isinstance(item, Element)
    # default values.
    assert isinstance(item.defaults, dict)
    assert len(item.defaults) == 8
    assert item.defaults["record_id"] == 0
    assert item.defaults["part_number"] == ""
    assert item.defaults["assembly"] == ""
    assert item.defaults["quantity"] == 0
    assert item.defaults["condition"] == ""
    assert item.defaults["installed"] == False
    assert item.defaults["remarks"] == ""
    assert item.defaults["box"] == 0
    parts_file_close(parts_file)


def test_005_02_get_datafile(filesystem):
    """Item needs correct database."""
    item, parts_file = base_setup(filesystem)
    assert item.get_datafile() == parts_file
    parts_file_close(parts_file)


def test_005_03_get_table(filesystem):
    """Item needs the database table 'items'."""
    item, parts_file = base_setup(filesystem)
    assert item.get_table() == "items"
    parts_file_close(parts_file)


def test_005_04_get_set_part_number(filesystem):
    """
    Get and set the part_number property.

    The property 'part_number' is required and is a string between 1 and
    30 characters long.
    """
    item, parts_file = base_setup(filesystem)
    defaults = item.get_initial_values()
    item._set_property("part_number", item_values["part_number"])
    assert item_values["part_number"] == item.get_part_number()
    item._set_property("part_number", None)
    assert item.defaults["part_number"] == item.get_part_number()
    result = item.set_part_number(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = item.set_part_number(item_values["part_number"])
    assert result["valid"]
    assert result["entry"] == item_values["part_number"]
    assert result["entry"] == item.get_part_number()
    parts_file_close(parts_file)


def test_005_05_get_set_assembly(filesystem):
    """
    Get and set the assembly property.

    The property 'assembly' is required and is a string between 1 and
    15 characters long. It is forced to all uppercase.
    """
    item, parts_file = base_setup(filesystem)
    defaults = item.get_initial_values()
    item._set_property("assembly", item_values["assembly"])
    assert item_values["assembly"] == item.get_assembly()
    item._set_property("assembly", None)
    assert defaults["assembly"] == item.get_assembly()
    result = item.set_assembly(None)
    assert not result["valid"]
    assert result["entry"] is None
    result = item.set_assembly(item_values["assembly"])
    assert result["valid"]
    assert result["entry"] == item_values["assembly"]
    assert result["entry"] == item.get_assembly()
    parts_file_close(parts_file)


def test_005_06_get_set_quantity(filesystem):
    """
    Get and set the quantity property.

    The property 'quantity' is required and is a integer between 0 and
    999.
    """
    item, parts_file = base_setup(filesystem)
    defaults = item.get_initial_values()
    item._set_property("quantity", item_values["quantity"])
    assert item_values["quantity"] == item.get_quantity()
    item._set_property("quantity", None)
    assert defaults["quantity"] == item.get_quantity()
    result = item.set_quantity(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = item.set_quantity(-1)
    assert not result["valid"]
    assert result["entry"] == -1
    result = item.set_quantity(item_values["quantity"])
    assert result["valid"]
    assert result["entry"] == item_values["quantity"]
    assert result["entry"] == item.get_quantity()
    parts_file_close(parts_file)


def test_005_07_get_set_condition(filesystem):
    """
    Get and set the condition property.

    The property 'condition' is required and is a string selected from
    one of the values held in the "condtions' database table.
    """
    item, parts_file = base_setup(filesystem)
    defaults = item.get_initial_values()
    item._set_property("condition", item_values["condition"])
    assert item_values["condition"] == item.get_condition()
    item._set_property("condition", None)
    assert defaults["condition"] == item.get_condition()
    result = item.set_condition(None)
    assert not result["valid"]
    assert result["entry"] is None
    result = item.set_condition(item_values["condition"])
    assert result["valid"]
    assert result["entry"] == item_values["condition"]
    assert result["entry"] == item.get_condition()
    parts_file_close(parts_file)


def test_005_08_get_set_installed(filesystem):
    """
    Get and set the installed property.

    The property 'installed' is required and is a boolean value. If the
    item is installed in the car, it is True, otherwise False.
    """
    item, parts_file = base_setup(filesystem)
    defaults = item.get_initial_values()
    item._set_property("installed", item_values["installed"])
    assert item_values["installed"] == item.get_installed()
    item._set_property("installed", None)
    assert defaults["installed"] == item.get_installed()
    result = item.set_installed(None)
    assert not result["valid"]
    assert result["entry"] == 0
    result = item.set_installed(3)
    assert not result["valid"]
    assert result["entry"] == 0
    result = item.set_installed(item_values["installed"])
    assert result["valid"]
    assert result["entry"] == item_values["installed"]
    assert result["entry"] == item.get_installed()
    parts_file_close(parts_file)


def test_005_09_get_set_box(filesystem):
    """
    Get and set the storage box property.

    The property 'box' is required and is an integer value. The value is
    zero if the item is installed in the car or stored as a stand-alone
    item not in storage box.If it is stored in a box,then the values can
    be between 1 and 99.
    """
    item, parts_file = base_setup(filesystem)
    defaults = item.get_initial_values()
    item._set_property("box", item_values["box"])
    assert item_values["box"] == item.get_box()
    item._set_property("box", None)
    assert defaults["box"] == item.get_box()
    result = item.set_box(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = item.set_box(-1)
    assert not result["valid"]
    assert result["entry"] == -1
    result = item.set_box(item_values["box"])
    assert result["valid"]
    assert result["entry"] == item_values["box"]
    assert result["entry"] == item.get_box()
    parts_file_close(parts_file)


def test_005_10_get_default_property_values(filesystem):
    """
    Check the default values.

    With no properties given to constructor, the initial values should
    be the default values.
    """
    item, parts_file = base_setup(filesystem)
    defaults = item.get_initial_values()
    assert item.get_record_id() == defaults["record_id"]
    assert item.get_remarks() == defaults["remarks"]
    assert item.get_part_number() == defaults["part_number"]
    assert item.get_assembly() == defaults["assembly"]
    assert item.get_quantity() == defaults["quantity"]
    assert item.get_condition() == defaults["condition"]
    assert item.get_installed() == defaults["installed"]
    assert item.get_box() == defaults["box"]
    parts_file_close(parts_file)


def test_005_11_set_properties_from_dict(filesystem):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    item, parts_file = base_setup(filesystem)
    item.set_properties(item_values)
    assert item_values["record_id"] == item.get_record_id()
    assert item_values["part_number"] == item.get_part_number()
    assert item_values["assembly"] == item.get_assembly()
    assert item_values["quantity"] == item.get_quantity()
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    parts_file_close(parts_file)


def test_005_12_item_get_properties_size(filesystem):
    """
    Check the size of the properties dict.

    There should be 8 members.
    """
    item, parts_file = base_setup(filesystem)
    assert len(item.get_properties()) == len(item_values)
    parts_file_close(parts_file)


def test_005_13_item_from_partial_dict(filesystem):
    """
    Initialize a new Item with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    item, parts_file = base_setup(filesystem)
    assembly = item_values["assembly"]
    del item_values["assembly"]
    item = Item(parts_file, item_values)
    item_values["assembly"] = assembly
    assert item_values["record_id"] == item.get_record_id()
    assert item_values["part_number"] == item.get_part_number()
    assert item.get_assembly() == ""
    assert item_values["quantity"] == item.get_quantity()
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    parts_file_close(parts_file)


def test_001_14_get_properties_from_database(filesystem):
    """
    Access the database for the item properties.

    Add an item to the database, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    item, parts_file = base_setup(filesystem)
    item = Item(parts_file, item_values)
    record_id = item.add()
    assert record_id == 1
    assert record_id == item.get_record_id()

    item = Item(parts_file, record_id)
    assert not item.get_record_id() == item_values["record_id"]
    assert item.get_record_id() == 1
    assert item.get_part_number() == item_values["part_number"]
    assert item.get_assembly() == item_values["assembly"]
    assert item.get_quantity() == item_values["quantity"]
    assert item.get_condition() == item_values["condition"]
    assert item.get_installed() == item_values["installed"]
    assert item.get_remarks() == item_values["remarks"]
    assert item.get_box() == item_values["box"]

    parts_file_close(parts_file)
