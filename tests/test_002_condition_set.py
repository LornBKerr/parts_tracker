"""
Test the ConditionSet class.

File:       test_002_condition_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import ElementSet
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
    load_datafile_table,
)
from test_data import condition_columns, condition_value_set

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import ConditionSet
from pages import table_definition

parts_filename = "parts_test.parts"


def base_setup(filesystem):
    filename = filesystem + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    condition_set = ConditionSet(parts_file)
    return (condition_set, parts_file)


def test_002_01_constr(filesystem):
    """
    ConditionSet Extends ElementSet.

    The 'table' must be "conditions" and 'parts_file' needs to be the
    initializing parts_file.
    """
    condition_set, parts_file = base_setup(filesystem)
    assert isinstance(condition_set, ConditionSet)
    assert isinstance(condition_set, ElementSet)
    assert condition_set.get_table() == "conditions"
    assert condition_set.get_datafile() == parts_file
    datafile_close(parts_file)


def test_002_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Conmditions'", is empty when set to
    None or when the table is empty.
    """
    condition_set, parts_file = base_setup(filesystem)
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


def test_002_03_selected_rows(filesystem):
    """
    The 'property_set', a list of Conmditions", should contain the
    requested subset of conditions.
    """
    condition_set, parts_file = base_setup(filesystem)
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
