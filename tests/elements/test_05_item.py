"""
Test the Item class.

File:       test_05_item.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal
from test_setup_elements import (
    close_database,
    create_items_table,
    database_name,
    open_database,
)

from elements import Item

# set item values from dict of values
item_values = {
    "record_id": 9876,
    "part_number": "13215",
    "assembly": "P",
    "quantity": 4,
    "condition": "New",
    "installed": 1,
    "remarks": "test",
    "box": 5,
}


def test_05_01_constr(open_database):
    dbref = open_database
    item = Item(dbref)
    assert isinstance(item, Item)
    close_database(dbref)


def test_05_02_get_table(open_database):
    dbref = open_database
    item = Item(dbref)
    assert item.get_table() == "items"
    close_database(dbref)


def test_05_03_get_dbref(open_database):
    dbref = open_database
    item = Item(dbref)
    assert item.get_dbref() == dbref
    close_database(dbref)


def test_05_04_get_set_part_number(open_database):
    dbref = open_database
    item = Item(dbref)
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
    close_database(dbref)


def test_05_05_get_set_assembly(open_database):
    dbref = open_database
    item = Item(dbref)
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
    close_database(dbref)


def test_05_06_get_set_quantity(open_database):
    dbref = open_database
    item = Item(dbref)
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
    close_database(dbref)


def test_05_07_get_set_condition(open_database):
    dbref = open_database
    item = Item(dbref)
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
    close_database(dbref)


def test_05_08_get_set_installed(open_database):
    dbref = open_database
    item = Item(dbref)
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
    close_database(dbref)


def test_05_09_get_set_box(open_database):
    dbref = open_database
    item = Item(dbref)
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
    close_database(dbref)


def test_05_10_get_properties_type(open_database):
    dbref = open_database
    item = Item(dbref)
    data = item.get_properties()
    assert isinstance(data, dict)
    close_database(dbref)


def test_05_11_get_default_property_values(open_database):
    dbref = open_database
    item = Item(dbref)
    defaults = item.get_initial_values()
    assert item.get_remarks() == defaults["remarks"]
    assert item.get_part_number() == defaults["part_number"]
    assert item.get_assembly() == defaults["assembly"]
    assert item.get_quantity() == defaults["quantity"]
    assert item.get_condition() == defaults["condition"]
    assert item.get_installed() == defaults["installed"]
    assert item.get_box() == defaults["box"]
    close_database(dbref)


def test_05_12_set_properties_from_dict(open_database):
    # set Item from array
    dbref = open_database
    item = Item(dbref)
    item.set_properties(item_values)
    assert item_values["record_id"] == item.get_record_id()
    assert item_values["part_number"] == item.get_part_number()
    assert item_values["assembly"] == item.get_assembly()
    assert item_values["quantity"] == item.get_quantity()
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    close_database(dbref)


def test_05_13_item_get_properties_size(open_database):
    dbref = open_database
    item = Item(dbref)
    assert len(item.get_properties()) == len(item_values)
    close_database(dbref)


def test_05_14_item_from_dict(open_database):
    dbref = open_database
    item = Item(dbref, item_values)
    assert item_values["record_id"] == item.get_record_id()
    assert item_values["part_number"] == item.get_part_number()
    assert item_values["assembly"] == item.get_assembly()
    assert item_values["quantity"] == item.get_quantity()
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    close_database(dbref)


def test_05_15_item_from__partial_dict(open_database):
    dbref = open_database
    del item_values["assembly"]
    item = Item(dbref, item_values)
    assert item_values["record_id"] == item.get_record_id()
    assert item_values["part_number"] == item.get_part_number()
    assert "" == item.get_assembly()
    assert item_values["quantity"] == item.get_quantity()
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    close_database(dbref)


def test_05_16_item_add(open_database):
    dbref = open_database
    create_items_table(dbref)
    item = Item(dbref, item_values)
    item_id = item.add()
    assert item_id == 1
    assert item_id == item.get_record_id()
    assert item_values["part_number"] == item.get_part_number()
    assert item_values["assembly"] == item.get_assembly()
    assert item_values["quantity"] == item.get_quantity()
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    close_database(dbref)


def test_05_17_item_read_db(open_database):
    dbref = open_database
    create_items_table(dbref)
    item = Item(dbref)
    item.set_properties(item_values)
    item_id = item.add()
    assert item_id == 1
    # read db for existing item
    item2 = Item(dbref, 1)
    assert not item2 is None
    assert not item2.get_properties() is None
    assert item2.get_record_id() == 1
    assert item_values["part_number"] == item2.get_part_number()
    assert item_values["assembly"] == item2.get_assembly()
    assert item_values["quantity"] == item2.get_quantity()
    assert item_values["condition"] == item2.get_condition()
    assert item_values["installed"] == item2.get_installed()
    assert item_values["remarks"] == item2.get_remarks()
    assert item_values["box"] == item2.get_box()
    # read db for non-existing item
    item3 = Item(dbref, 5)
    assert isinstance(item3.get_properties(), dict)
    assert len(item3.get_properties()) == len(item_values)
    # Try direct read thru Element
    item2.set_properties(item2.get_properties_from_db(None, None))
    assert isinstance(item2.get_properties(), dict)
    assert len(item2.get_properties()) == 0
    close_database(dbref)


def test_05_18_item_update(open_database):
    dbref = open_database
    create_items_table(dbref)
    item = Item(dbref)
    item.set_properties(item_values)
    item_id = item.add()
    assert item_id == 1
    assert item_values["quantity"] == item.get_quantity()
    # update item quantity
    item.set_quantity(6)
    result = item.update()
    assert result
    assert item.get_properties() is not None
    assert item.get_record_id() == 1
    assert item_values["part_number"] == item.get_part_number()
    assert item_values["assembly"] == item.get_assembly()
    assert not item_values["quantity"] == item.get_quantity()
    assert item.get_quantity() == 6
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    close_database(dbref)


def test_05_19_item_delete(open_database):
    dbref = open_database
    create_items_table(dbref)
    item = Item(dbref)
    item.set_properties(item_values)
    item.add()
    # delete item
    result = item.delete()
    assert result
    # make sure it is really gone
    item = Item(dbref, 1)
    assert isinstance(item.get_properties(), dict)
    assert len(item.get_properties()) == 8
    close_database(dbref)


# end test_01_item.py
