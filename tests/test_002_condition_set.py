"""
Test the ConditionSet class.

File:       test_002_condition_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
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
from test_data import condition_columns, condition_value_set

from elements import ConditionSet
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
    condition_set = ConditionSet(parts_file)
    return (condition_set, parts_file)


def test_002_01_constr(tmp_path):
    """
    ConditionSet Extends ElementSet.

    The 'table' must be "conditions" and 'parts_file' needs to be the
    initializing parts_file.
    """
    condition_set, parts_file = base_setup(tmp_path)
    assert isinstance(condition_set, ConditionSet)
    assert isinstance(condition_set, ElementSet)
    assert condition_set.get_table() == "conditions"
    assert condition_set.get_datafile() == parts_file
    datafile_close(parts_file)


def test_002_02_set_property_set_empty(tmp_path):
    """
    The 'property_set', a list of 'Conmditions'", is empty when set to
    None or when the table is empty.
    """
    condition_set, parts_file = base_setup(tmp_path)
    assert isinstance(condition_set.get_property_set(), list)
    condition_set.set_property_set(None)
    assert isinstance(condition_set.get_property_set(), list)
    assert len(condition_set.get_property_set()) == 0
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM " + condition_set.get_table()
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(condition_set.get_property_set())
    assert count == condition_set.get_number_elements()
    datafile_close(parts_file)


def test_002_03_selected_rows(tmp_path):
    """
    The 'property_set', a list of Conmditions", should contain the
    requested subset of conditions.
    """
    condition_set, parts_file = base_setup(tmp_path)
    load_datafile_table(
        parts_file, "conditions", condition_columns, condition_value_set
    )
    condition_set = ConditionSet(parts_file, "condition", "Missing")
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM "
        + condition_set.get_table()
        + " WHERE condition = 'Missing'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(condition_set.get_property_set())
    assert count == 1
    datafile_close(parts_file)
