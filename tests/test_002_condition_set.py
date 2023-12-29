"""
Test the ConditionSet class.

File:       test_002_condition_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal, ElementSet
from test_setup import (
    condition_columns,
    condition_value_set,
    db_close,
    db_create,
    db_open,
    filesystem,
    load_db_table,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import ConditionSet


def test_002_01_constr(filesystem):
    """
    ConditionSet Extends ElementSet.

    The 'table' must be "conditions" and 'dbref' needs to be the
    initializing dbref.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set, ConditionSet)
    assert isinstance(condition_set, ElementSet)
    assert condition_set.get_table() == "conditions"
    assert condition_set.get_dbref() == dbref
    db_close(dbref)


def test_002_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Conmditions'", is empty when set to
    None or when the table is empty.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set.get_property_set(), list)
    condition_set.set_property_set(None)
    assert isinstance(condition_set.get_property_set(), list)
    assert len(condition_set.get_property_set()) == 0
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + condition_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(condition_set.get_property_set())
    assert count == condition_set.get_number_elements()
    db_close(dbref)


def test_002_03_selected_rows(filesystem):
    """
    The 'property_set', a list of Conmditions", should contain the
    requested subset of conditions.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "conditions", condition_columns, condition_value_set)
    condition_set = ConditionSet(dbref, "condition", "Missing")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + condition_set.get_table()
        + " WHERE condition = 'Missing'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(condition_set.get_property_set())
    assert count == 1
    db_close(dbref)
