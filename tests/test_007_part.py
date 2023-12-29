"""
Test the Part class.

File:       test_007_part.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal, Element
from test_setup import (
    db_close,
    db_create,
    db_open,
    filesystem,
    item_columns,
    item_value_set,
    load_db_table,
    part_columns,
    part_value_set,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import ItemSet, Part

part_values = {
    "record_id": 69,
    "part_number": "17005",
    "source": "Fastenal",
    "description": "Bolt, Hex Cap, 1/4-28 x 1.000, Grade 5, Zinc",
    "remarks": "Moss P/N 324-247",
}


def test_007_01_constr(filesystem):
    """
    Part Extends Element.

    Check the types of class variables and default values.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    part = Part(dbref)
    assert isinstance(part, Part)
    assert isinstance(part, Element)
    # default values.
    assert isinstance(part.defaults, dict)
    assert len(part.defaults) == len(part_values)
    assert part.defaults["record_id"] == 0
    assert part.defaults["part_number"] == ""
    assert part.defaults["source"] == ""
    assert part.defaults["description"] == ""
    assert part.defaults["remarks"] == ""
    db_close(dbref)


def test_007_02_get_table(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    part = Part(dbref)
    assert part.get_table() == "parts"
    db_close(dbref)


def test_007_03_get_dbref(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    part = Part(dbref)
    assert part.get_dbref() == dbref
    db_close(dbref)


def test_007_04_get_set_part_number(filesystem):
    """
    Get and set the part_number property.

    The property 'part_number' is required and is a string between 1 and
    30 characters long.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_007_05_get_set_source(filesystem):
    """
    Get and set the source property.

    The property 'source' is required and is a string at least 1
    character long. The allowed source values are held in the 'sources'
    table in the database.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_007_06_get_set_description(filesystem):
    """
    Get and set the description property.

    The property 'description' is required and is a string between 1
    and 255 characters long.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
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


def test_007_07_item_get_default_property_values(filesystem):
    """
    Check the default values.

    With no properties given to consturctor, the initial values should be
    the default values.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    part = Part(dbref)
    defaults = part.get_initial_values()
    assert part.get_record_id() == defaults["record_id"]
    assert part.get_remarks() == defaults["remarks"]
    assert part.get_part_number() == defaults["part_number"]
    assert part.get_source() == defaults["source"]
    assert part.get_description() == defaults["description"]
    db_close(dbref)


def test_007_08_set_properties_from_dict(filesystem):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    part = Part(dbref)
    part.set_properties(part_values)
    assert part_values["record_id"] == part.get_record_id()
    assert part_values["remarks"] == part.get_remarks()
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert part_values["description"] == part.get_description()
    db_close(dbref)


def test_007_09_get_properties_size(filesystem):
    """
    Check the size of the properties dict.

    There should be 5 members.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    part = Part(dbref)
    assert len(part.get_properties()) == len(part_values)
    db_close(dbref)


def test_007_10_part_from_dict(filesystem):
    """
    Initialize a new Item with a dict of values.

    The resulting properties should match the input values.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    part = Part(dbref, part_values)
    assert part_values["record_id"] == part.get_record_id()
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert part_values["description"] == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    db_close(dbref)


def test_007_12_part_from_partial_dict(filesystem):
    """
    Initialize a new Item with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    del part_values["source"]
    part = Part(dbref, part_values)
    assert part_values["record_id"] == part.get_record_id()
    assert part_values["part_number"] == part.get_part_number()
    assert "" == part.get_source()
    assert part_values["description"] == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    db_close(dbref)


def test_007_13_get_total_quantity(filesystem):
    """
    Check the total quantity for a part from the database.

    For the given part_number check that the total quantity reflected
    is the same as he total quantity held in the database table 'items'.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "items", item_columns, item_value_set)
    part = Part(dbref, part_values)
    item_set = ItemSet(dbref, "part_number", part.get_part_number())
    total_quantity = 0
    for item in item_set:
        total_quantity += item.get_quantity()
    # check total quantity used
    assert part.get_total_quantity() == total_quantity
    db_close(dbref)


def test_007_14_correct_column_name(filesystem):
    """
    Check the name of the key column in the database.

    The column name must be one of None, 'record_id', or 'part_number'.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "parts", part_columns, part_value_set)
    part = Part(dbref, part_value_set[0][0], "record_id")
    part.get_record_id() == part_value_set[0][0]
    part.get_part_number() == part_value_set[0][1]
    part = Part(dbref, part_value_set[1][0], "part_number")
    part.get_record_id() == part_value_set[1][0]
    part.get_part_number() == part_value_set[1][1]
    part = Part(dbref, part_value_set[1][0], "description")
    part.get_record_id() == 0
    part.get_part_number() == ""


def test_007_15_get_properties_from_database(filesystem):
    """
    Access the database for the part properties.

    Add an part to the database, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    part = Part(dbref, part_values)
    record_id = part.add()
    assert record_id == 1
    assert record_id == part.get_record_id()

    part = Part(dbref, record_id)
    assert not part.get_record_id() == part_values["record_id"]
    assert part.get_record_id() == 1
    assert part.get_part_number() == part_values["part_number"]
    assert part.get_source() == part_values["source"]
    assert part.get_description() == part_values["description"]
    assert part.get_remarks() == part_values["remarks"]

    db_close(dbref)
