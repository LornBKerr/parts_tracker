"""
Test the ItemSet class.

File:       test_006_item_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import ElementSet
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
    load_datafile_table,
)
from test_data import item_columns, item_value_set

from elements import Item, ItemSet
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}

parts_filename = "parts_test.parts"


def base_setup(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    item_set = ItemSet(parts_file)
    return (item_set, parts_file)


def test_006_01_constructor(tmp_path):
    """
    ItemSet Extends ElementSet.

    The 'table' must be "items" and 'parts_file' needs to be the
    initializing parts_file.
    """
    item_set, parts_file = base_setup(tmp_path)
    assert isinstance(item_set, ItemSet)
    assert isinstance(item_set, ElementSet)
    assert item_set.get_table() == "items"
    assert item_set.get_datafile() == parts_file
    datafile_close(parts_file)


def test_006_02_set_property_set_empty(tmp_path):
    """
    The 'property_set', a list of 'Items'", is empty when set to
    None or when the table is empty.
    """
    item_set, parts_file = base_setup(tmp_path)
    assert isinstance(item_set.get_property_set(), list)
    item_set.set_property_set(None)
    assert isinstance(item_set.get_property_set(), list)
    assert len(item_set.get_property_set()) == 0
    count_result = parts_file.sql_query("SELECT COUNT(*) FROM " + item_set.get_table())
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    assert count == item_set.get_number_elements()
    datafile_close(parts_file)


def test_006_03_selected_rows(tmp_path):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items.
    """
    item_set, parts_file = base_setup(tmp_path)
    load_datafile_table(parts_file, "items", item_columns, item_value_set)
    item_set = ItemSet(parts_file, "part_number", "BTB1108")
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM "
        + item_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    datafile_close(parts_file)


def test_006_04_ordered_selected_rows(tmp_path):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by assembly.
    """
    item_set, parts_file = base_setup(tmp_path)
    load_datafile_table(parts_file, "items", item_columns, item_value_set)
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
    datafile_close(parts_file)


def test_006_05_selected_rows_limit(tmp_path):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit'.
    """
    item_set, parts_file = base_setup(tmp_path)
    load_datafile_table(parts_file, "items", item_columns, item_value_set)
    limit = 5
    item_set = ItemSet(parts_file, None, None, "record_id", limit)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 1
    datafile_close(parts_file)


def test_006_06_selected_rows_limit_offset(tmp_path):
    """
    The 'property_set', a list of 'Items', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    item_set, parts_file = base_setup(tmp_path)
    load_datafile_table(parts_file, "items", item_columns, item_value_set)
    limit = 5
    offset = 2
    item_set = ItemSet(parts_file, None, None, "record_id", limit, offset)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 3
    datafile_close(parts_file)
