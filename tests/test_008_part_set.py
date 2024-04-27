"""
Test the PartSet class.

File:       test_008_part_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import ElementSet
from test_data import part_columns, part_value_set
from test_setup import (
    filesystem,
    load_parts_file_table,
    parts_file_close,
    parts_file_create,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Part, PartSet
from pages import table_definition

parts_filename = "parts_test.parts"


def base_setup(filesystem):
    filename = filesystem + "/" + parts_filename
    parts_file = parts_file_create(filename, table_definition)
    part_set = PartSet(parts_file)
    return (part_set, parts_file)


def test_008_01_constr(filesystem):
    """
    PartSet Extends ElementSet.

    The 'table' must be "parts" and 'parts_file' needs to be the
    initializing parts_file.
    """
    part_set, parts_file = base_setup(filesystem)
    assert isinstance(part_set, PartSet)
    assert isinstance(part_set, ElementSet)
    assert part_set.get_table() == "parts"
    assert part_set.get_datafile() == parts_file
    parts_file_close(parts_file)


def test_008_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Parts', is empty when set to
    None or when the table is empty.
    """
    part_set, parts_file = base_setup(filesystem)
    assert isinstance(part_set.get_property_set(), list)
    part_set.set_property_set(None)
    assert isinstance(part_set.get_property_set(), list)
    assert len(part_set.get_property_set()) == 0
    count_result = parts_file.sql_query("SELECT COUNT(*) FROM " + part_set.get_table())
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    assert count == part_set.get_number_elements()
    parts_file_close(parts_file)


def test_008_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Parts.
    """
    part_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "parts", part_columns, part_value_set)
    part_set = PartSet(parts_file, "source", "None")
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM " + part_set.get_table() + " WHERE source = 'None'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    assert count == 6
    parts_file_close(parts_file)


def test_008_4_selected_rows_limit(filesystem):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit'.
    """
    part_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "parts", part_columns, part_value_set)
    limit = 5
    part_set = PartSet(parts_file, None, None, "record_id", limit)
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == part_value_set[0][0]
    parts_file_close(parts_file)


def test_008_05_selected_rows_limit_offset(filesystem):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    part_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "parts", part_columns, part_value_set)
    limit = 5
    offset = 2
    part_set = PartSet(parts_file, None, None, "record_id", limit, offset)
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == part_value_set[2][0]
    parts_file_close(parts_file)
