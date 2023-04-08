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
from lbk_library import Dbal
from test_setup import db_close, db_create, db_open

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Source

source_values = {"record_id": 15, "source": "Moss USA"}


def test_003_01_constr(db_open):
    dbref = db_open
    source = Source(dbref)
    assert type(source) == Source
    db_close(dbref)


def test_003_02_get_table(db_open):
    dbref = db_open
    source = Source(dbref)
    assert source.get_table() == "sources"
    db_close(dbref)


def test_003_03_get_dbref(db_open):
    dbref = db_open
    source = Source(dbref)
    assert source.get_dbref() == dbref
    db_close(dbref)


def test_003_04_set_source(db_open):
    # set empty Source
    dbref = db_open
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
    db_close(dbref)


def test_003_05_get_properties_type(db_open):
    dbref = db_open
    source = Source(dbref)
    data = source.get_properties()
    assert type(data) == dict
    db_close(dbref)


def test_003_06_get_default_property_values(db_open):
    dbref = db_open
    source = Source(dbref)
    defaults = source.get_initial_values()
    assert source.get_record_id() == defaults["record_id"]
    assert source.get_source() == defaults["source"]
    db_close(dbref)


def test_003_07_set_properties_from_dict(db_open):
    # set Source from array
    dbref = db_open
    source = Source(dbref)
    source.set_properties(source_values)
    assert source_values["record_id"] == source.get_record_id()
    assert source_values["source"] == source.get_source()
    db_close(dbref)


def test_003_08_get_properties_size(db_open):
    dbref = db_open
    source = Source(dbref)
    data = source.get_properties()
    assert len(data) == 2
    db_close(dbref)


def test_003_09_source_from_dict(db_open):
    dbref = db_open
    source = Source(dbref, source_values)
    assert source_values["record_id"] == source.get_record_id()
    assert source_values["source"] == source.get_source()
    db_close(dbref)


def test_003_10_item_from__partial_dict(db_open):
    dbref = db_open
    values = {"record_id": 15}
    source = Source(dbref, values)
    assert values["record_id"] == source.get_record_id()
    assert "" == source.get_source()
    db_close(dbref)


def test_003_11_add(db_create):
    dbref = db_create
    source = Source(dbref, source_values)
    record_id = source.add()
    assert record_id == 1
    assert record_id == source.get_record_id()
    assert source_values["source"] == source.get_source()
    db_close(dbref)


def test_003_12_read_db(db_create):
    dbref = db_create
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
    db_close(dbref)


def test_003_13_update(db_create):
    dbref = db_create
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
    db_close(dbref)


def test_003_14_delete(db_create):
    dbref = db_create
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
    db_close(dbref)
