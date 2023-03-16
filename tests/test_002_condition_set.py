"""
Test the ConditionSet class.

File:       test_002_condition_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal, ElementSet

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import (
    condition_values,
    db_close,
    db_create,
    db_name,
    db_open,
    load_conditions_table,
)

from elements import ConditionSet


def test_002_01_constr(db_create):
    dbref = db_create
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set, ConditionSet)
    assert isinstance(condition_set, ElementSet)
    db_close(dbref)


def test_02_02_get_dbref(db_create):
    dbref = db_create
    condition_set = ConditionSet(dbref)
    assert condition_set.get_dbref() == dbref
    db_close(dbref)


def test_02_03_get_table(db_create):
    dbref = db_create
    condition_set = ConditionSet(dbref)
    assert condition_set.get_table() == "conditions"
    db_close(dbref)


def test_02_04_set_table(db_create):
    dbref = db_create
    condition_set = ConditionSet(dbref)
    condition_set.set_table("items")
    assert condition_set.get_table() == "items"
    db_close(dbref)


def test_02_05_get_property_set(db_create):
    dbref = db_create
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set.get_property_set(), list)
    db_close(dbref)


def test_02_06_set_property_set_none(db_create):
    dbref = db_create
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set.get_property_set(), list)
    condition_set.set_property_set(None)
    assert isinstance(condition_set.get_property_set(), list)
    assert len(condition_set.get_property_set()) == 0
    db_close(dbref)


def test_02_07_all_rows_empty(db_create):
    dbref = db_create
    conditions_set = ConditionSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + conditions_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(conditions_set.get_property_set())
    assert count == conditions_set.get_number_elements()
    db_close(dbref)


def test_02_08_selected_rows(db_create):
    dbref = db_create
    load_conditions_table(dbref)
    conditions_set = ConditionSet(dbref, "condition", "Missing")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + conditions_set.get_table()
        + " WHERE condition = 'Missing'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(conditions_set.get_property_set())
    assert count == 1
    db_close(dbref)
