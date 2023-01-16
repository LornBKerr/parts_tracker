"""
Test the Part class.

File:       item.py
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

from elements import Item, Part

# **********************************************************************
# Test setups
# **********************************************************************

database = "parts_test.db"


def close_database(dbref):
    dbref.sql_close()


@pytest.fixture
def open_database(tmpdir):
    path = tmpdir.join(database)
    dbref = Dbal()
    # valid connection
    dbref.sql_connect(path)
    return dbref


def create_parts_table(dbref):
    dbref.sql_query("DROP TABLE IF EXISTS 'parts'")
    create_table = (
        'CREATE TABLE IF NOT EXISTS "parts"'
        + ' ("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
        + ' "part_number" TEXT NOT NULL,'
        + ' "source" TEXT DEFAULT NULL,'
        + ' "description" TEXT NOT NULL,'
        + ' "remarks" TEXT DEFAULT NULL );'
    )
    result = dbref.sql_query(create_table)


# used for testing part.get_total_quantity
def create_items_table(dbref):
    dbref.sql_query("DROP TABLE IF EXISTS 'items'")
    create_table = (
        'CREATE TABLE IF NOT EXISTS "items"'
        + '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        + ' "part_number" TEXT NOT NULL,'
        + ' "assembly" TEXT NOT NULL,'
        + ' "quantity" INTEGER NOT NULL,'
        + ' "condition" TEXT NOT NULL,'
        + ' "installed" INTEGER NOT NULL DEFAULT 0,'
        + ' "box" INTEGER DEFAULT NULL,'
        + ' "remarks" TEXT DEFAULT NULL)'
    )
    dbref.sql_query(create_table)


# used for testing part.get_total_quantity
# set item values from array of values
item_values = dict(
    {
        "record_id": 0,
        "part_number": "13215",
        "assembly": "P",
        "quantity": 4,
        "condition": "New",
        "installed": 1,
        "remarks": "test",
        "box": 5,
    }
)

# set part values from array of values
part_values = dict(
    {
        "record_id": 9876,
        "part_number": "13215",
        "source": "Moss",
        "description": "bolt",
        "remarks": "From local source",
    }
)

# **********************************************************************
# End Test setups
# **********************************************************************

# **********************************************************************
# Begin Tests
# **********************************************************************
def test_03_01_constr(open_database):
    dbref = open_database
    part = Part(dbref)
    assert type(part) == Part
    close_database(dbref)


def test_03_02_get_table(open_database):
    dbref = open_database
    part = Part(dbref)
    assert part.get_table() == "parts"
    close_database(dbref)


def test_03_03_get_dbref(open_database):
    dbref = open_database
    part = Part(dbref)
    assert part.get_dbref() == dbref
    close_database(dbref)


def test_03_04_get_set_part_number(open_database):
    dbref = open_database
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
    close_database(dbref)


def test_03_05_get_set_source(open_database):
    dbref = open_database
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
    close_database(dbref)


def test_03_06_get_set_description(open_database):
    dbref = open_database
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
    close_database(dbref)


def test_03_07_get_properties_type(open_database):
    dbref = open_database
    part = Part(dbref)
    assert isinstance(part.get_properties(), dict)
    close_database(dbref)


def test_03_08_item_get_default_property_values(open_database):
    dbref = open_database
    part = Part(dbref)
    defaults = part.get_initial_values()
    assert part.get_part_number() == defaults["part_number"]
    assert part.get_source() == defaults["source"]
    assert part.get_description() == defaults["description"]
    close_database(dbref)


def test_03_09_set_properties_from_dict(open_database):
    # set Part from array
    dbref = open_database
    part = Part(dbref)
    part.set_properties(part_values)
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert part_values["description"] == part.get_description()
    close_database(dbref)


def test_03_10_get_properties_size(open_database):
    dbref = open_database
    part = Part(dbref)
    assert len(part.get_properties()) == len(part_values)
    close_database(dbref)


def test_03_11_part_from_dict(open_database):
    # set Part from array
    dbref = open_database
    part = Part(dbref, part_values)
    assert part_values["record_id"] == part.get_record_id()
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert part_values["description"] == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    close_database(dbref)


def test_03_12_part_from_partial_dict(open_database):
    dbref = open_database
    del part_values["source"]
    part = Part(dbref, part_values)
    assert part_values["record_id"] == part.get_record_id()
    assert part_values["part_number"] == part.get_part_number()
    assert "" == part.get_source()
    assert part_values["description"] == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    close_database(dbref)


def test_03_13_bad_column_name(open_database):
    dbref = open_database
    part = Part(dbref, None, "a_column")
    defaults = part.get_initial_values()
    assert part.get_record_id() == defaults["record_id"]
    assert part.get_part_number() == defaults["part_number"]
    assert part.get_source() == defaults["source"]
    assert part.get_description() == defaults["description"]
    assert part.get_remarks() == defaults["remarks"]
    close_database(dbref)


def test_03_14_part_add(open_database):
    dbref = open_database
    create_parts_table(dbref)
    part = Part(dbref, part_values)
    record_id = part.add()
    assert record_id == 1
    assert record_id == part.get_record_id()
    assert part_values["part_number"] == part.get_part_number()
    assert part_values["source"] == part.get_source()
    assert part_values["description"] == part.get_description()
    assert part_values["remarks"] == part.get_remarks()
    close_database(dbref)


def test_03_15_part_read_db(open_database):
    dbref = open_database
    create_parts_table(dbref)
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
    close_database(dbref)


def test_03_16_part_update(open_database):
    dbref = open_database
    create_parts_table(dbref)
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
    close_database(dbref)


def test_03_17_part_delete(open_database):
    dbref = open_database
    create_parts_table(dbref)
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


def test_03_17_get_total_quantity(open_database):
    dbref = open_database
    create_parts_table(dbref)
    # create items table with 4 entries, three with current part number
    create_items_table(dbref)
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
    close_database(dbref)


# end test_03_elements_part.py
