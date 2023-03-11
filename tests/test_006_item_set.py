"""
Test the ItemSet class.

File:       test_006_item_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""
import os
import sys

import pytest
from lbk_library import Dbal, ElementSet

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import (  # create_items_table,
    db_close,
    db_create,
    db_name,
    db_open,
    item_values,
    load_items_table,
)

from elements import Item, ItemSet


def test_006_01_constructor(db_create):
    dbref = db_create
    item_set = ItemSet(dbref)
    assert isinstance(item_set, ItemSet)
    assert isinstance(item_set, ElementSet)
    db_close(dbref)


def test_006_02_get_dbref(db_create):
    dbref = db_create
    item_set = ItemSet(dbref)
    assert item_set.get_dbref() == dbref
    db_close(dbref)


def test_006_03_get_table(db_create):
    dbref = db_create
    item_set = ItemSet(dbref)
    assert item_set.get_table() == "items"
    db_close(dbref)


def test_006_04_set_table(db_create):
    dbref = db_create
    item_set = ItemSet(dbref)
    item_set.set_table("parts")
    assert item_set.get_table() == "parts"
    db_close(dbref)


def test_006_05_get_property_set(db_create):
    dbref = db_create
    item_set = ItemSet(dbref)
    assert isinstance(item_set.get_property_set(), list)
    db_close(dbref)


def test_006_06_set_property_set_none(db_create):
    dbref = db_create
    item_set = ItemSet(dbref)
    assert isinstance(item_set.get_property_set(), list)
    item_set.set_property_set(None)
    assert isinstance(item_set.get_property_set(), list)
    assert len(item_set.get_property_set()) == 0
    db_close(dbref)


def test_006_07_all_rows_empty(db_create):
    dbref = db_create
    item_set = ItemSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + item_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    assert count == item_set.get_number_elements()
    db_close(dbref)


def test_006_08_selected_rows(db_create):
    dbref = db_create
    load_items_table(dbref)
    item_set = ItemSet(dbref, "part_number", "BTB1108")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + item_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    db_close(dbref)


def test_006_09_ordered_selected_rows(db_create):
    dbref = db_create
    load_items_table(dbref)
    item_set = ItemSet(dbref, "part_number", "BTB1108", "assembly")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + item_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    selected_set = item_set.get_property_set()
    assert count == len(selected_set)
    for counter in range(0, count - 2):
        item1 = selected_set[counter]
        item2 = selected_set[counter + 1]
        assert item1.get_assembly() < item2.get_assembly()
    db_close(dbref)


def test_006_10_selected_rows_limit(db_create):
    dbref = db_create
    load_items_table(dbref)
    limit = 5
    item_set = ItemSet(dbref, None, None, "record_id", limit)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 1
    db_close(dbref)


def test_006_11_selected_rows_limit_offset(db_create):
    dbref = db_create
    load_items_table(dbref)
    limit = 5
    offset = 2
    item_set = ItemSet(dbref, None, None, "record_id", limit, offset)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 3
    db_close(dbref)


def test_006_12_iterator(db_create):
    dbref = db_create
    load_items_table(dbref)
    limit = 5
    item_set = ItemSet(dbref, None, None, "record_id", limit)
    i = 1
    for item in item_set:
        assert item.get_record_id() == i
        i += 1
    db_close(dbref)
