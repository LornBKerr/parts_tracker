"""
Test the source class.

File:       test_03_source.py
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
from test_data import source_value_set

from elements import Source
from pages import table_definition

file_version = "1.0.1"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Changed all test funtions to have 'tmp_path' as parameter instead of 'filesystem' and as parameter to filesystem in the body.",
}

source_values = {
    "record_id": source_value_set[0][0],
    "source": source_value_set[0][1],
}

parts_filename = "parts_test.parts"


def base_setup(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    source = Source(parts_file)
    return (source, parts_file)


def test_003_01_constr(tmp_path):
    source, parts_file = base_setup(tmp_path)
    assert isinstance(source, Source)
    assert isinstance(source, Element)
    # default values.
    assert isinstance(source._defaults, dict)
    assert len(source._defaults) == 2
    assert source._defaults["record_id"] == 0
    assert source._defaults["source"] == ""
    datafile_close(parts_file)


def test_003_02_get_parts_file(tmp_path):
    """Source needs correct database."""
    source, parts_file = base_setup(tmp_path)
    assert source.get_datafile() == parts_file
    datafile_close(parts_file)


def test_003_03_get_table(tmp_path):
    """Sourcen needs the database table 'sources'."""
    source, parts_file = base_setup(tmp_path)
    assert source.get_table() == "sources"
    datafile_close(parts_file)


def test_003_04_set_source(tmp_path):
    """
    Get and set the source property.

    The property 'source' is required and is a text value held in the
    database.

    The property 'record_id is handled in the Element' base class.
    """
    source, parts_file = base_setup(tmp_path)
    source._set_property("source", source_values["source"])
    assert source_values["source"] == source.get_source()
    source._set_property("source", None)
    assert source._defaults["source"] == source.get_source()
    result = source.set_source(None)
    assert not result["valid"]
    assert result["entry"] is None
    result = source.set_source(source_values["source"])
    assert result["valid"]
    assert result["entry"] == source_values["source"]
    assert result["entry"] == source.get_source()
    datafile_close(parts_file)


def test_003_05_get_default_property_values(tmp_path):
    """
    Check the default values.

    With no properties given to consturcr, the initial values should be
    the default values.
    """
    source, parts_file = base_setup(tmp_path)
    defaults = source.get_initial_values()
    assert source.get_record_id() == defaults["record_id"]
    assert source.get_source() == defaults["source"]
    datafile_close(parts_file)


def test_003_06_set_properties_from_dict(tmp_path):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    source, parts_file = base_setup(tmp_path)
    set_results = source.set_properties(source_values)
    assert source_values["record_id"] == source.get_record_id()
    assert source_values["source"] == source.get_source()
    assert len(set_results) == 2
    assert set_results["source"]["entry"] == source_values["source"]
    assert set_results["source"]["valid"]
    assert set_results["source"]["msg"] == ""
    datafile_close(parts_file)


def test_003_07_get_properties_size(tmp_path):
    """
    Check the size of the properties dict.

    There should be two members.
    """
    source, parts_file = base_setup(tmp_path)
    data = source.get_properties()
    assert len(data) == 2
    datafile_close(parts_file)


def test_003_08_source_from_dict(tmp_path):
    """
    Initialize a new Source with a dict of values.

    The resulting properties should match the input values.
    """
    source, parts_file = base_setup(tmp_path)
    source = Source(parts_file, source_values)
    assert source_values["record_id"] == source.get_record_id()
    assert source_values["source"] == source.get_source()
    datafile_close(parts_file)


def test_003_09_item_from__partial_dict(tmp_path):
    """
    Initialize a new Source with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    source, parts_file = base_setup(tmp_path)
    values = {"record_id": 15}
    source = Source(parts_file, values)
    assert values["record_id"] == source.get_record_id()
    assert "" == source.get_source()
    datafile_close(parts_file)


def test_001_10_get_properties_from_database(tmp_path):
    """
    Access the database for the source properties.

    Add a Source to the database, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    source, parts_file = base_setup(tmp_path)
    source = Source(parts_file, source_values)
    record_id = source.add()
    assert record_id == 1
    assert record_id == source.get_record_id()
    assert source_values["source"] == source.get_source()

    condtion = Source(parts_file, record_id)
    assert record_id == source.get_record_id()
    assert source_values["source"] == source.get_source()

    datafile_close(parts_file)
