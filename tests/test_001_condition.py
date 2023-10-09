"""
Test the Condition class.

File:       test_001_condition.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal
from test_setup import (
    condition_columns,
    condition_value_set,
    db_close,
    db_create,
    db_open,
    filesystem,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Condition

condition_values = {"record_id": 1, "condition": "Usable"}


def test_001_01_constr(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    assert type(condition) == Condition
    db_close(dbref)


def test_001_02_get_table(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    assert condition.get_table() == "conditions"
    db_close(dbref)


def test_001_03_get_dbref(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    assert condition.get_dbref() == dbref
    db_close(dbref)


def test_001_04_get_set_condition(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    defaults = condition.get_initial_values()
    condition._set_property("condition", condition_values["condition"])
    assert condition.get_condition() == condition_values["condition"]
    condition._set_property("condition", None)
    assert condition.defaults["condition"] == condition.get_condition()
    result = condition.set_condition(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = condition.set_condition(condition_values["condition"])
    assert result["valid"]
    assert result["entry"] == condition_values["condition"]
    assert result["entry"] == condition.get_condition()
    db_close(dbref)


def test_001_05_get_properties_type(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    data = condition.get_properties()
    assert type(data) == dict
    db_close(dbref)


def test_001_06_get_default_property_values(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    defaults = condition.get_initial_values()
    assert condition.get_record_id() == defaults["record_id"]
    assert condition.get_condition() == defaults["condition"]
    db_close(dbref)


def test_001_07_set_properties_from_dict(filesystem):
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    condition.set_properties(condition_values)
    assert condition_values["record_id"] == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()
    db_close(dbref)


def test_001_08_get_properties_size(filesystem):
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref)
    data = condition.get_properties()
    assert len(data) == 2
    db_close(dbref)


def test_001_09_condition_from_dict(filesystem):
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    assert condition_values["record_id"] == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()
    db_close(dbref)


def test_001_10_item_from__partial_dict(filesystem):
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    values = {"record_id": 15}
    condition = Condition(dbref, values)
    assert values["record_id"] == condition.get_record_id()
    assert "" == condition.get_condition()
    db_close(dbref)


def test_001_11_add(filesystem):
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    condition = Condition(dbref, condition_values)
    record_id = condition.add()
    assert record_id == 1
    assert record_id == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()
    db_close(dbref)


def test_001_12_read_db(filesystem):
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    condition = Condition(dbref)
    condition.set_properties(condition_values)
    record_id = condition.add()
    assert record_id == 1
    # read db for existing part
    condition2 = Condition(dbref, record_id)
    assert record_id == condition2.get_record_id()
    assert condition_values["condition"] == condition2.get_condition()
    # read db for non-existing part
    condition3 = Condition(dbref, 5)
    assert isinstance(condition3.get_properties(), dict)
    assert len(condition3.get_properties()) == len(condition_values)
    # Try direct read thru Element
    condition2.set_properties(condition2.get_properties_from_db(None, None))
    assert isinstance(condition2.get_properties(), dict)
    assert len(condition2.get_properties()) == 0
    db_close(dbref)


def test_001_13_update(filesystem):
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    condition = Condition(dbref)
    condition.set_properties(condition_values)
    record_id = condition.add()
    assert record_id == 1
    assert condition_values["condition"] == condition.get_condition()
    # update condition
    condition.set_condition("British Wiring")
    result = condition.update()
    assert result
    assert condition.get_properties() is not None
    assert record_id == condition.get_record_id()
    assert not condition_values["condition"] == condition.get_condition()
    assert "British Wiring" == condition.get_condition()
    db_close(dbref)


def test_001_14_delete(filesystem):
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    condition = Condition(dbref)
    condition.set_properties(condition_values)
    record_id = condition.add()
    # delete part
    result = condition.delete()
    assert result
    # make sure it is really gone
    condition2 = Condition(dbref, condition_values["record_id"])
    assert isinstance(condition2.get_properties(), dict)
    assert len(condition2.get_properties()) == len(condition_values)
    db_close(dbref)
