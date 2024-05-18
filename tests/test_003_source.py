"""
Test the source class.

File:       test_03_source.py
Author:     Lorn B Kerr
Copyright:  (c) 2023, 2024 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Element
from lbk_library.testing_support import datafile_close, datafile_create, filesystem
from test_data import source_value_set

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Source
from pages import table_definition

source_values = {"record_id": source_value_set[0][0], "source": source_value_set[0][1]}

parts_filename = "parts_test.parts"


def base_setup(filesystem):
    filename = filesystem + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    source = Source(parts_file)
    return (source, parts_file)


def test_003_01_constr(filesystem):
    source, parts_file = base_setup(filesystem)
    assert isinstance(source, Source)
    assert isinstance(source, Element)
    # default values.
    assert isinstance(source.defaults, dict)
    assert len(source.defaults) == 2
    assert source.defaults["record_id"] == 0
    assert source.defaults["source"] == ""
    datafile_close(parts_file)


def test_003_02_get_parts_file(filesystem):
    """Source needs correct database."""
    source, parts_file = base_setup(filesystem)
    assert source.get_datafile() == parts_file
    datafile_close(parts_file)


def test_003_03_get_table(filesystem):
    """Sourcen needs the database table 'sources'."""
    source, parts_file = base_setup(filesystem)
    assert source.get_table() == "sources"
    datafile_close(parts_file)


def test_003_04_set_source(filesystem):
    """
    Get and set the source property.

    The property 'source' is required and is a text value held in the
    database.

    The property 'record_id is handled in the Element' base class.
    """
    source, parts_file = base_setup(filesystem)
    defaults = source.get_initial_values()
    source._set_property("source", source_values["source"])
    assert source_values["source"] == source.get_source()
    source._set_property("source", None)
    assert source.defaults["source"] == source.get_source()
    result = source.set_source(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = source.set_source(source_values["source"])
    assert result["valid"]
    assert result["entry"] == source_values["source"]
    assert result["entry"] == source.get_source()
    datafile_close(parts_file)


def test_003_05_get_default_property_values(filesystem):
    """
    Check the default values.

    With no properties given to consturcr, the initial values should be
    the default values.
    """
    source, parts_file = base_setup(filesystem)
    defaults = source.get_initial_values()
    assert source.get_record_id() == defaults["record_id"]
    assert source.get_source() == defaults["source"]
    datafile_close(parts_file)


def test_003_06_set_properties_from_dict(filesystem):
    """
    Check the 'set_properties' function.

    The inital values can be set from a dict input.
    """
    source, parts_file = base_setup(filesystem)
    source.set_properties(source_values)
    assert source_values["record_id"] == source.get_record_id()
    assert source_values["source"] == source.get_source()
    datafile_close(parts_file)


def test_003_07_get_properties_size(filesystem):
    """
    Check the size of the properties dict.

    There should be two members.
    """
    source, parts_file = base_setup(filesystem)
    data = source.get_properties()
    assert len(data) == 2
    datafile_close(parts_file)


def test_003_08_source_from_dict(filesystem):
    """
    Initialize a new Source with a dict of values.

    The resulting properties should match the input values.
    """
    source, parts_file = base_setup(filesystem)
    source = Source(parts_file, source_values)
    assert source_values["record_id"] == source.get_record_id()
    assert source_values["source"] == source.get_source()
    datafile_close(parts_file)


def test_003_09_item_from__partial_dict(filesystem):
    """
    Initialize a new Source with a sparse dict of values.

    The resulting properties should mach the input values with the
    missing values replaced with default values.
    """
    source, parts_file = base_setup(filesystem)
    values = {"record_id": 15}
    source = Source(parts_file, values)
    assert values["record_id"] == source.get_record_id()
    assert "" == source.get_source()
    datafile_close(parts_file)


def test_001_10_get_properties_from_database(filesystem):
    """
    Access the database for the source properties.

    Add a Source to the database, then access it with the
    record_id key. The actual read and write funtions are in the
    base class "Element".
    """
    source, parts_file = base_setup(filesystem)
    source = Source(parts_file, source_values)
    record_id = source.add()
    assert record_id == 1
    assert record_id == source.get_record_id()
    assert source_values["source"] == source.get_source()

    condtion = Source(parts_file, record_id)
    assert record_id == source.get_record_id()
    assert source_values["source"] == source.get_source()

    datafile_close(parts_file)
