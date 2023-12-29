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
from lbk_library import Dbal, Element
from test_setup import db_close, db_create, db_open, filesystem

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Condition

condition_values = {"record_id": 1, "condition": "Usable"}


def test_001_01_constr(filesystem):
    """
    Condition Extends Element.

    Default values should be a dict of record_id = 0, condition = "".
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    # Condition class structure.
    assert isinstance(condition, Condition)
    assert isinstance(condition, Element)
    # default values.
    assert isinstance(condition.defaults, dict)
    assert len(condition.defaults) == 2
    assert condition.defaults["record_id"] == 0
    assert condition.defaults["condition"] == ""

    db_close(dbref)


def test_001_02_get_dbref(filesystem):
    """Condition needs correct database."""
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    assert condition.get_dbref() == dbref
    db_close(dbref)


def test_001_03_get_table(filesystem):
    """Condition needs the database table 'conditions'."""
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    assert condition.get_table() == "conditions"
    db_close(dbref)


def test_001_04_get_set_condition(filesystem):
    """
    Get and set the condition property.

    The property 'condition' is required and is a text value held in the
    database.

    The property 'record_id is handled in the Element' base class.
    """
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


def test_001_05_get_default_property_values(filesystem):
    """
    Check the default values.

    With no properties given to consturcr, the initial values should be
    the default values.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    defaults = condition.get_initial_values()
    assert condition.get_record_id() == defaults["record_id"]
    assert condition.get_condition() == defaults["condition"]
    db_close(dbref)


def test_001_06_set_properties_from_dict(filesystem):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    fs_base = filesystem
    dbref = db_open(fs_base)
    condition = Condition(dbref)
    condition.set_properties(condition_values)
    assert condition_values["record_id"] == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()
    db_close(dbref)


def test_001_07_get_properties_size(filesystem):
    """
    Check the size of the properties dict.

    There should be two members.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref)
    data = condition.get_properties()
    assert len(data) == 2
    db_close(dbref)


def test_001_08_condition_from_dict(filesystem):
    """
    Initialize a new Condition with a dict of values.

    The resulting properties should match the input values.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    assert condition_values["record_id"] == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()
    db_close(dbref)


def test_001_09_item_from_partial_dict(filesystem):
    """
    Initialize a new Condition with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    values = {"record_id": 15}
    condition = Condition(dbref, values)
    assert values["record_id"] == condition.get_record_id()
    assert "" == condition.get_condition()
    db_close(dbref)


def test_001_10_get_properties_from_database(filesystem):
    """
    Access the database for the condition properties.

    Add a condition to the database, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    condition = Condition(dbref, condition_values)
    record_id = condition.add()
    assert record_id == 1
    assert record_id == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()

    condition = Condition(dbref, record_id)
    assert record_id == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()

    db_close(dbref)
