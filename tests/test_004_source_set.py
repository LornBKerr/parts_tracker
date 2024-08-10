"""
Test the SourceSet class.

File:       test_004_source_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
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
from test_data import source_columns, source_value_set

from elements import SourceSet
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}

parts_filename = "parts_test.parts"


def base_setup(filesystem):
    filename = filesystem + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    source_set = SourceSet(parts_file)
    return (source_set, parts_file)


def test_004_01_constr(filesystem):
    """
    SourceSet Extends ElementSet.

    The 'table' must be "conditions" and 'parts_file' needs to be the
    initializing parts_file.
    """
    source_set, parts_file = base_setup(filesystem)
    assert isinstance(source_set, SourceSet)
    assert isinstance(source_set, ElementSet)
    assert source_set.get_table() == "sources"
    assert source_set.get_datafile() == parts_file
    datafile_close(parts_file)


def test_004_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Sources', is empty when set to
    None or when the table is empty.
    """
    source_set, parts_file = base_setup(filesystem)
    assert isinstance(source_set.get_property_set(), list)
    source_set.set_property_set(None)
    assert isinstance(source_set.get_property_set(), list)
    assert len(source_set.get_property_set()) == 0
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM " + source_set.get_table()
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(source_set.get_property_set())
    assert count == source_set.get_number_elements()
    datafile_close(parts_file)


def test_004_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Sources', should contain the
    requested subset of conditions.
    """
    source_set, parts_file = base_setup(filesystem)
    load_datafile_table(parts_file, "sources", source_columns, source_value_set)
    source_set = SourceSet(parts_file, "source", "British Car Parts")
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM "
        + source_set.get_table()
        + " WHERE source = 'British Car Parts'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(source_set.get_property_set())
    assert count == 1
    datafile_close(parts_file)
