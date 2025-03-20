"""
Test the Condition class.

File:       test_001_condition.py
Author:     Lorn B Kerr
Copyright:  (c) 2023, 2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.1
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Element
from lbk_library.testing_support import datafile_close, datafile_create, filesystem
from test_data import condition_value_set

from elements import Condition
from pages import table_definition

file_version = "1.0.1"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Changed all test funtions to have 'tmp_path' as parameter instead of 'filesystem' and as parameter to filesystem in the body.",
}

parts_filename = "parts_test.parts"

condition_values = {
    "record_id": condition_value_set[0][0],
    "condition": condition_value_set[0][1],
}


def base_setup(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    condition = Condition(parts_file)
    return (condition, parts_file)


def test_001_01_constr(tmp_path):
    """
    Condition Extends Element.

    Default values should be a dict of record_id = 0, condition = "".
    """
    condition, parts_file = base_setup(tmp_path)
    # Condition class structure.
    assert isinstance(condition, Condition)
    assert isinstance(condition, Element)
    # default values.
    assert isinstance(condition._defaults, dict)
    assert len(condition._defaults) == 2
    assert condition._defaults["record_id"] == 0
    assert condition._defaults["condition"] == ""
    datafile_close(parts_file)


def test_001_02_get_parts_file(tmp_path):
    """Condition needs correct parts_file."""
    condition, parts_file = base_setup(tmp_path)
    assert condition.get_datafile() == parts_file
    datafile_close(parts_file)


def test_001_03_get_table(tmp_path):
    """Condition needs the parts_file table 'conditions'."""
    condition, parts_file = base_setup(tmp_path)
    assert condition.get_table() == "conditions"
    datafile_close(parts_file)


def test_001_04_get_set_condition(tmp_path):
    """
    Get and set the condition property.

    The property 'condition' is required and is a text value held in the
    parts_file.

    The property 'record_id' is handled in the Element' base class.
    """
    condition, parts_file = base_setup(tmp_path)
    defaults = condition.get_initial_values()
    condition._set_property("condition", condition_value_set[0][1])
    assert condition.get_condition() == condition_value_set[0][1]
    condition._set_property("condition", None)
    assert condition._defaults["condition"] == condition.get_condition()
    result = condition.set_condition(None)
    assert not result["valid"]
    assert result["entry"] is None
    result = condition.set_condition(condition_value_set[0][1])
    assert result["valid"]
    assert result["entry"] == condition_value_set[0][1]
    assert result["entry"] == condition.get_condition()
    datafile_close(parts_file)


def test_001_05_get_default_property_values(tmp_path):
    """
    Check the default values.

    With no properties given to consturcr, the initial values should be
    the default values.
    """
    condition, parts_file = base_setup(tmp_path)
    defaults = condition.get_initial_values()
    assert condition.get_record_id() == defaults["record_id"]
    assert condition.get_condition() == defaults["condition"]
    datafile_close(parts_file)


def test_001_06_set_properties_from_dict(tmp_path):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    condition, parts_file = base_setup(tmp_path)
    set_results = condition.set_properties(condition_values)
    assert condition_values["record_id"] == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()
    assert len(set_results) == 2
    assert set_results["condition"]["entry"] == condition_values["condition"]
    assert set_results["condition"]["valid"]
    assert set_results["condition"]["msg"] == ""
    datafile_close(parts_file)


def test_001_07_get_properties(tmp_path):
    """
    Check the size of the properties dict.

    There should be two members.
    """
    condition, parts_file = base_setup(tmp_path)
    data = condition.get_properties()
    assert len(data) == 2
    assert data["record_id"] == 0
    assert data["condition"] == ""
    datafile_close(parts_file)


def test_001_08_condition_from_dict(tmp_path):
    """
    Initialize a new Condition with a dict of values.

    The resulting properties should match the input values.
    """
    condition, parts_file = base_setup(tmp_path)
    condition = Condition(parts_file, condition_values)
    assert condition_values["record_id"] == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()
    datafile_close(parts_file)


def test_001_09_item_from_partial_dict(tmp_path):
    """
    Initialize a new Condition with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    condition, parts_file = base_setup(tmp_path)
    condition = Condition(parts_file, condition_values)
    values = {"record_id": 15}
    condition = Condition(parts_file, values)
    assert values["record_id"] == condition.get_record_id()
    assert "" == condition.get_condition()
    datafile_close(parts_file)


def test_001_10_get_properties_from_parts_file(tmp_path):
    """
    Access the parts_file for the condition properties.

    Add a condition to the parts_file, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    condition, parts_file = base_setup(tmp_path)
    condition = Condition(parts_file, condition_values)
    record_id = condition.add()
    assert record_id == 1
    assert record_id == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()

    condition = Condition(parts_file, record_id)
    assert record_id == condition.get_record_id()
    assert condition_values["condition"] == condition.get_condition()
    datafile_close(parts_file)
