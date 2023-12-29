"""
Test the ItemSet class.

File:       test_006_item_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal, ElementSet
from test_setup import (
    db_close,
    db_create,
    db_open,
    filesystem,
    item_columns,
    item_value_set,
    load_db_table,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Item, ItemSet


def test_006_01_constructor(filesystem):
    """
    ItemSet Extends ElementSet.

    The 'table' must be "items" and 'dbref' needs to be the
    initializing dbref.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    item_set = ItemSet(dbref)
    assert isinstance(item_set, ItemSet)
    assert isinstance(item_set, ElementSet)
    assert item_set.get_table() == "items"
    assert item_set.get_dbref() == dbref
    db_close(dbref)


def test_006_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Items'", is empty when set to
    None or when the table is empty.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    item_set = ItemSet(dbref)
    assert isinstance(item_set.get_property_set(), list)
    item_set.set_property_set(None)
    assert isinstance(item_set.get_property_set(), list)
    assert len(item_set.get_property_set()) == 0
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + item_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    assert count == item_set.get_number_elements()
    db_close(dbref)


def test_006_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "items", item_columns, item_value_set)
    item_set = ItemSet(dbref, "part_number", "BTB1108")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + item_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    db_close(dbref)


def test_006_04_ordered_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by assembly.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "items", item_columns, item_value_set)
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


def test_006_05_selected_rows_limit(filesystem):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit'.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "items", item_columns, item_value_set)
    limit = 5
    item_set = ItemSet(dbref, None, None, "record_id", limit)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 1
    db_close(dbref)


def test_006_06_selected_rows_limit_offset(filesystem):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "items", item_columns, item_value_set)
    limit = 5
    offset = 2
    item_set = ItemSet(dbref, None, None, "record_id", limit, offset)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 3
    db_close(dbref)
