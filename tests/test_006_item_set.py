"""
Test the ItemSet class.

File:       test_006_item_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import ElementSet
from test_data import item_columns, item_value_set
from test_setup import (
    filesystem,
    load_parts_file_table,
    parts_file_close,
    parts_file_create,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Item, ItemSet
from pages import table_definition

parts_filename = "parts_test.parts"


def base_setup(filesystem):
    filename = filesystem + "/" + parts_filename
    parts_file = parts_file_create(filename, table_definition)
    item_set = ItemSet(parts_file)
    return (item_set, parts_file)


def test_006_01_constructor(filesystem):
    """
    ItemSet Extends ElementSet.

    The 'table' must be "items" and 'parts_file' needs to be the
    initializing parts_file.
    """
    item_set, parts_file = base_setup(filesystem)
    assert isinstance(item_set, ItemSet)
    assert isinstance(item_set, ElementSet)
    assert item_set.get_table() == "items"
    assert item_set.get_datafile() == parts_file
    parts_file_close(parts_file)


def test_006_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Items'", is empty when set to
    None or when the table is empty.
    """
    item_set, parts_file = base_setup(filesystem)
    assert isinstance(item_set.get_property_set(), list)
    item_set.set_property_set(None)
    assert isinstance(item_set.get_property_set(), list)
    assert len(item_set.get_property_set()) == 0
    count_result = parts_file.sql_query("SELECT COUNT(*) FROM " + item_set.get_table())
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    assert count == item_set.get_number_elements()
    parts_file_close(parts_file)


def test_006_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items.
    """
    item_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "items", item_columns, item_value_set)
    item_set = ItemSet(parts_file, "part_number", "BTB1108")
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM "
        + item_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    parts_file_close(parts_file)


def test_006_04_ordered_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by assembly.
    """
    item_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "items", item_columns, item_value_set)
    item_set = ItemSet(parts_file, "part_number", "BTB1108", "assembly")
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM "
        + item_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    selected_set = item_set.get_property_set()
    assert count == len(selected_set)
    for counter in range(0, count - 2):
        item1 = selected_set[counter]
        item2 = selected_set[counter + 1]
        assert item1.get_assembly() < item2.get_assembly()
    parts_file_close(parts_file)


def test_006_05_selected_rows_limit(filesystem):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit'.
    """
    item_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "items", item_columns, item_value_set)
    limit = 5
    item_set = ItemSet(parts_file, None, None, "record_id", limit)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 1
    parts_file_close(parts_file)


def test_006_06_selected_rows_limit_offset(filesystem):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    item_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "items", item_columns, item_value_set)
    limit = 5
    offset = 2
    item_set = ItemSet(parts_file, None, None, "record_id", limit, offset)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 3
    parts_file_close(parts_file)
