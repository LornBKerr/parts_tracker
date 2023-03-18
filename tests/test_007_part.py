"""
Test the Part class.

File:       test_007_part.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal
from test_setup import db_close, db_create, db_open, item_values, part_values

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Item, Part


def test_007_01_constr(db_open):
    dbref = db_open
    part = Part(dbref)
    assert type(part) == Part
    db_close(dbref)


def test_007_02_get_table(db_open):
    dbref = db_open
    part = Part(dbref)
    assert part.get_table() == "parts"
    db_close(dbref)


def test_007_03_get_dbref(db_open):
    dbref = db_open
    part = Part(dbref)
    assert part.get_dbref() == dbref
    db_close(dbref)


def test_007_04_get_set_part_number(db_open):
    dbref = db_open
    part = Part(dbref)
    defaults = part.get_initial_values()
    part._set_property("part_number", part_values["part_number"])
    assert part_values["part_number"] == part.get_part_number()
    part._set_property("part_number", None)
    assert part.defaults["part_number"] == part.get_part_number()
    result = part.set_part_number(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = part.set_part_number(part_values["part_number"])
    assert result["valid"]
    assert result["entry"] == part_values["part_number"]
    assert result["entry"] == part.get_part_number()
    db_close(dbref)


def test_007_05_get_set_source(db_open):
    dbref = db_open
    part = Part(dbref)
    defaults = part.get_initial_values()
    part._set_property("source", part_values["source"])
    assert part_values["source"] == part.get_source()
    part._set_property("source", None)
    assert part.defaults["source"] == part.get_source()
    result = part.set_source(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = part.set_source(part_values["source"])
    assert result["valid"]
    assert result["entry"] == part_values["source"]
    assert result["entry"] == part.get_source()
    db_close(dbref)


def test_007_06_get_set_description(db_open):
    dbref = db_open
    part = Part(dbref)
    defaults = part.get_initial_values()
    part._set_property("description", part_values["description"])
    assert part_values["description"] == part.get_description()
    part._set_property("description", None)
    assert part.defaults["description"] == part.get_description()
    result = part.set_description(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = part.set_description(part_values["description"])
    assert result["valid"]
    assert result["entry"] == part_values["description"]
    assert result["entry"] == part.get_description()
    db_close(dbref)


def test_007_07_get_properties_type(db_open):
    dbref = db_open
    part = Part(dbref)
    assert isinstance(part.get_properties(), dict)
    db_close(dbref)


def test_007_08_item_get_default_property_values(db_open):
    dbref = db_open
    part = Part(dbref)
    defaults = part.get_initial_values()
    assert part.get_part_number() == defaults["part_number"]
    assert part.get_source() == defaults["source"]
    assert part.get_description() == defaults["description"]
    db_close(dbref)


def test_007_09_set_properties_from_dict(db_open):
    # set Part from array
    dbref = db_open
    part = Part(dbref)
    part.set_properties(part_values)
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert part_values["description"] == part.get_description()
    db_close(dbref)


def test_007_10_get_properties_size(db_open):
    dbref = db_open
    part = Part(dbref)
    assert len(part.get_properties()) == len(part_values)
    db_close(dbref)


def test_007_11_part_from_dict(db_open):
    # set Part from array
    dbref = db_open
    part = Part(dbref, part_values)
    assert part_values["record_id"] == part.get_record_id()
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert part_values["description"] == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    db_close(dbref)


def test_007_12_part_from_partial_dict(db_open):
    dbref = db_open
    del part_values["source"]
    part = Part(dbref, part_values)
    assert part_values["record_id"] == part.get_record_id()
    assert part_values["part_number"] == part.get_part_number()
    assert "" == part.get_source()
    assert part_values["description"] == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    db_close(dbref)


def test_007_13_bad_column_name(db_open):
    dbref = db_open
    part = Part(dbref, None, "a_column")
    defaults = part.get_initial_values()
    assert part.get_record_id() == defaults["record_id"]
    assert part.get_part_number() == defaults["part_number"]
    assert part.get_source() == defaults["source"]
    assert part.get_description() == defaults["description"]
    assert part.get_remarks() == defaults["remarks"]
    db_close(dbref)


def test_007_14_part_add(db_create):
    dbref = db_create
    part = Part(dbref, part_values)
    record_id = part.add()
    assert record_id == 1
    assert record_id == part.get_record_id()
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert part_values["description"] == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    db_close(dbref)


def test_007_15_part_read_db(db_create):
    dbref = db_create
    part = Part(dbref)
    part.set_properties(part_values)
    record_id = part.add()
    assert record_id == 1
    # read db for existing part
    part2 = Part(dbref, 1)
    assert not part2 is None
    assert not part2.get_properties() is None
    assert record_id == part2.get_record_id()
    assert part_values["part_number"] == part2.get_part_number()
    assert part_values["source"] == part2.get_source()
    assert part_values["description"] == part2.get_description()
    assert part_values["remarks"] == part2.get_remarks()
    # read db for non-existing part
    part3 = Part(dbref, 5)
    assert len(part3.get_properties()) == len(part_values)
    # Try direct read thru Element
    part2.set_properties(part2.get_properties_from_db(None, None))
    assert len(part2.get_properties()) == 0
    db_close(dbref)


def test_007_16_part_update(db_create):
    dbref = db_create
    part = Part(dbref)
    part.set_properties(part_values)
    record_id = part.add()
    assert record_id == 1
    assert part_values["description"] == part.get_description()
    # update part description
    part.set_description("Bolt, #10")
    result = part.update()
    assert result
    assert part.get_properties() is not None
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert not part_values["description"] == part.get_description()
    assert "Bolt, #10" == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    db_close(dbref)


def test_007_17_part_delete(db_create):
    dbref = db_create
    part = Part(dbref)
    part.set_properties(part_values)
    record_id = part.add()
    assert record_id
    # delete part
    result = part.delete()
    assert result
    # make sure it is really gone
    part = Part(dbref, part_values["part_number"])
    assert isinstance(part.get_properties(), dict)
    assert len(part.get_properties()) == len(part_values)


def test_007_17_get_total_quantity(db_create):
    dbref = db_create
    # create items table with 4 entries, three with current part number
    assert dbref
    item = Item(dbref, item_values)
    item.add()
    total_quantity = item.get_quantity()
    item_values["quantity"] = 2
    item_values["assembly"] = "R"
    item = Item(dbref, item_values)
    item.add()
    total_quantity += item.get_quantity()
    item_values["quantity"] = 3
    item_values["assembly"] = "RA"
    item_values["part_number"] = "326-735"
    item = Item(dbref, item_values)
    item.add()
    item_values["quantity"] = 7
    item_values["assembly"] = "PA"
    item_values["part_number"] = "13215"
    item = Item(dbref, item_values)
    item.add()
    total_quantity += item.get_quantity()
    # check total quantity used
    part = Part(dbref)
    part.set_properties(part_values)
    record_id = part.add()
    assert record_id
    quantity = part.get_total_quantity()
    assert quantity == total_quantity
    db_close(dbref)


# end test_007_part.py
