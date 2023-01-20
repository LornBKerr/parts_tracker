"""
Test the source class.

File:       test_03_source.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal
from test_setup_elements import close_database, database_name, open_database

from elements import Source


def create_sources_table(dbref):
    dbref.sql_query("DROP TABLE IF EXISTS 'sources'")
    create_table = 'CREATE TABLE "sources" (record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, source TEXT DEFAULT "")'
    result = dbref.sql_query(create_table)
    return dbref


# set source values from array of values
source_values = dict(
    {
        "record_id": 15,
        "source": "Moss USA",
    }
)


def test_03_01_constr(open_database):
    dbref = open_database
    source = Source(dbref)
    assert type(source) == Source
    close_database(dbref)


def test_03_02_get_table(open_database):
    dbref = open_database
    source = Source(dbref)
    assert source.get_table() == "sources"
    close_database(dbref)


def test_03_03_get_dbref(open_database):
    dbref = open_database
    source = Source(dbref)
    assert source.get_dbref() == dbref
    close_database(dbref)


def test_03_04_set_source(open_database):
    # set empty Source
    dbref = open_database
    source = Source(dbref)
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
    close_database(dbref)


def test_03_05_get_properties_type(open_database):
    dbref = open_database
    source = Source(dbref)
    data = source.get_properties()
    assert type(data) == dict
    close_database(dbref)


def test_03_06_get_default_property_values(open_database):
    dbref = open_database
    source = Source(dbref)
    defaults = source.get_initial_values()
    assert source.get_record_id() == defaults["record_id"]
    assert source.get_source() == defaults["source"]
    close_database(dbref)


def test_03_07_set_properties_from_dict(open_database):
    # set Source from array
    dbref = open_database
    source = Source(dbref)
    source.set_properties(source_values)
    assert source_values["record_id"] == source.get_record_id()
    assert source_values["source"] == source.get_source()
    close_database(dbref)


def test_03_08_get_properties_size(open_database):
    dbref = open_database
    source = Source(dbref)
    data = source.get_properties()
    assert len(data) == 2
    close_database(dbref)


def test_03_09_source_from_dict(open_database):
    dbref = open_database
    source = Source(dbref, source_values)
    assert source_values["record_id"] == source.get_record_id()
    assert source_values["source"] == source.get_source()
    close_database(dbref)


def test_03_10_item_from__partial_dict(open_database):
    dbref = open_database
    values = {"record_id": 15}
    source = Source(dbref, values)
    assert values["record_id"] == source.get_record_id()
    assert "" == source.get_source()
    close_database(dbref)


def test_03_11_add(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source = Source(dbref, source_values)
    record_id = source.add()
    assert record_id == 1
    assert record_id == source.get_record_id()
    assert source_values["source"] == source.get_source()
    close_database(dbref)


def test_03_12_read_db(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source = Source(dbref)
    source.set_properties(source_values)
    record_id = source.add()
    assert record_id == 1
    # read db for existing part
    source2 = Source(dbref, record_id)
    assert record_id == source2.get_record_id()
    assert source_values["source"] == source2.get_source()
    # read db for non-existing part
    source3 = Source(dbref, 5)
    assert isinstance(source3.get_properties(), dict)
    assert len(source3.get_properties()) == len(source_values)
    # Try direct read thru Element
    source2.set_properties(source2.get_properties_from_db(None, None))
    assert isinstance(source2.get_properties(), dict)
    assert len(source2.get_properties()) == 0
    close_database(dbref)


def test_03_13_update(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source = Source(dbref)
    source.set_properties(source_values)
    record_id = source.add()
    assert record_id == 1
    assert source_values["source"] == source.get_source()

    # update source
    source.set_source("British Wiring")
    result = source.update()
    assert result
    assert source.get_properties() is not None
    assert record_id == source.get_record_id()
    assert not source_values["source"] == source.get_source()
    assert "British Wiring" == source.get_source()
    close_database(dbref)


def test_03_14_delete(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source = Source(dbref)
    source.set_properties(source_values)
    record_id = source.add()
    # delete part
    result = source.delete()
    assert result
    # make sure it is really gone
    source2 = Source(dbref, source_values["record_id"])
    assert isinstance(source2.get_properties(), dict)
    assert len(source2.get_properties()) == len(source_values)
    close_database(dbref)
