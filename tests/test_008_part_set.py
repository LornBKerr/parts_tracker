"""
Test the PartSet class.

File:       test_008_part_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.1
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
from test_data import part_columns, part_value_set

from elements import PartSet
from pages import table_definition

file_version = "1.0.1"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Changed all test funtions to have 'tmp_path' as parameter instead of 'filesystem' and as parameter to filesystem in the body.",
}

parts_filename = "parts_test.parts"


def base_setup(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    part_set = PartSet(parts_file)
    return (part_set, parts_file)


def test_008_01_constr(tmp_path):
    """
    PartSet Extends ElementSet.

    The 'table' must be "parts" and 'parts_file' needs to be the
    initializing parts_file.
    """
    part_set, parts_file = base_setup(tmp_path)
    assert isinstance(part_set, PartSet)
    assert isinstance(part_set, ElementSet)
    assert part_set.get_table() == "parts"
    assert part_set.get_datafile() == parts_file
    datafile_close(parts_file)


def test_008_02_set_property_set_empty(tmp_path):
    """
    The 'property_set', a list of 'Parts', is empty when set to
    None or when the table is empty.
    """
    part_set, parts_file = base_setup(tmp_path)
    assert isinstance(part_set.get_property_set(), list)
    part_set.set_property_set(None)
    assert isinstance(part_set.get_property_set(), list)
    assert len(part_set.get_property_set()) == 0
    count_result = parts_file.sql_query("SELECT COUNT(*) FROM " + part_set.get_table())
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    assert count == part_set.get_number_elements()
    datafile_close(parts_file)


def test_008_03_selected_rows(tmp_path):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Parts.
    """
    part_set, parts_file = base_setup(tmp_path)
    load_datafile_table(parts_file, "parts", part_columns, part_value_set)
    part_set = PartSet(parts_file, "source", 2)
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM " + part_set.get_table() + " WHERE source = 2"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    datafile_close(parts_file)


def test_008_4_selected_rows_limit(tmp_path):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit'.
    """
    part_set, parts_file = base_setup(tmp_path)
    load_datafile_table(parts_file, "parts", part_columns, part_value_set)
    limit = 5
    part_set = PartSet(parts_file, None, None, "record_id", limit)
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == part_value_set[0][0]
    datafile_close(parts_file)


def test_008_05_selected_rows_limit_offset(tmp_path):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    part_set, parts_file = base_setup(tmp_path)
    load_datafile_table(parts_file, "parts", part_columns, part_value_set)
    limit = 5
    offset = 2
    part_set = PartSet(parts_file, None, None, "record_id", limit, offset)
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == part_value_set[2][0]
    datafile_close(parts_file)
