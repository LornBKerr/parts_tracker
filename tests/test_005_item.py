"""
Test the Item class.

File:       test_005_item.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal
from test_setup import db_close, db_create, db_open, item_values


src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)


from elements import Item


def test_005_01_constr(db_open):
    dbref = db_open
    item = Item(dbref)
    assert isinstance(item, Item)
    db_close(dbref)


def test_005_02_get_table(db_open):
    dbref = db_open
    item = Item(dbref)
    assert item.get_table() == "items"
    db_close(dbref)


def test_005_03_get_dbref(db_open):
    dbref = db_open
    item = Item(dbref)
    assert item.get_dbref() == dbref
    db_close(dbref)


def test_005_04_get_set_part_number(db_open):
    dbref = db_open
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
    db_close(dbref)


def test_005_05_get_set_assembly(db_open):
    dbref = db_open
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
    db_close(dbref)


def test_005_06_get_set_quantity(db_open):
    dbref = db_open
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
    db_close(dbref)


def test_005_07_get_set_condition(db_open):
    dbref = db_open
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
    db_close(dbref)


def test_005_08_get_set_installed(db_open):
    dbref = db_open
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
    db_close(dbref)


def test_005_09_get_set_box(db_open):
    dbref = db_open
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
    db_close(dbref)


def test_005_10_get_properties_type(db_open):
    dbref = db_open
    item = Item(dbref)
    data = item.get_properties()
    assert isinstance(data, dict)
    db_close(dbref)


def test_005_11_get_default_property_values(db_open):
    dbref = db_open
    item = Item(dbref)
    defaults = item.get_initial_values()
    assert item.get_remarks() == defaults["remarks"]
    assert item.get_part_number() == defaults["part_number"]
    assert item.get_assembly() == defaults["assembly"]
    assert item.get_quantity() == defaults["quantity"]
    assert item.get_condition() == defaults["condition"]
    assert item.get_installed() == defaults["installed"]
    assert item.get_box() == defaults["box"]
    db_close(dbref)


def test_005_12_set_properties_from_dict(db_open):
    # set Item from array
    dbref = db_open
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
    db_close(dbref)


def test_005_13_item_get_properties_size(db_open):
    dbref = db_open
    item = Item(dbref)
    assert len(item.get_properties()) == len(item_values)
    db_close(dbref)


def test_005_14_item_from_dict(db_open):
    dbref = db_open
    item = Item(dbref, item_values)
    assert item_values["record_id"] == item.get_record_id()
    assert item_values["part_number"] == item.get_part_number()
    assert item_values["assembly"] == item.get_assembly()
    assert item_values["quantity"] == item.get_quantity()
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    db_close(dbref)


def test_005_15_item_from__partial_dict(db_open):
    dbref = db_open
    assembly = item_values["assembly"]
    del item_values["assembly"]
    item = Item(dbref, item_values)
    item_values["assembly"] = assembly
    assert item_values["record_id"] == item.get_record_id()
    assert item_values["part_number"] == item.get_part_number()
    assert "" == item.get_assembly()
    assert item_values["quantity"] == item.get_quantity()
    assert item_values["condition"] == item.get_condition()
    assert item_values["installed"] == item.get_installed()
    assert item_values["remarks"] == item.get_remarks()
    assert item_values["box"] == item.get_box()
    db_close(dbref)


def test_005_16_item_add(db_create):
    dbref = db_create
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
    db_close(dbref)


def test_005_17_item_read_db(db_create):
    dbref = db_create
    item = Item(dbref, item_values)
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
    db_close(dbref)


def test_005_18_item_update(db_create):
    dbref = db_create
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
    db_close(dbref)


def test_005_19_item_delete(db_create):
    dbref = db_create
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
    db_close(dbref)
