"""
Test the SourceSet class.

File:       test_004_source_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal, ElementSet
from test_setup import (
    db_close,
    db_create,
    db_open,
    load_db_table,
    source_columns,
    source_value_set,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import SourceSet


def test_004_01_constr(db_create):
    dbref = db_create
    source_set = SourceSet(dbref)
    assert isinstance(source_set, SourceSet)
    assert isinstance(source_set, ElementSet)
    db_close(dbref)


def test_004_02_get_dbref(db_create):
    dbref = db_create
    source_set = SourceSet(dbref)
    assert source_set.get_dbref() == dbref
    db_close(dbref)


def test_004_03_get_table(db_create):
    dbref = db_create
    source_set = SourceSet(dbref)
    assert source_set.get_table() == "sources"
    db_close(dbref)


def test_004_04_set_table(db_create):
    dbref = db_create
    source_set = SourceSet(dbref)
    source_set.set_table("items")
    assert source_set.get_table() == "items"
    db_close(dbref)


def test_004_05_get_property_set(db_create):
    dbref = db_create
    source_set = SourceSet(dbref)
    assert isinstance(source_set.get_property_set(), list)
    db_close(dbref)


def test_004_06_set_property_set_none(db_create):
    dbref = db_create
    source_set = SourceSet(dbref)
    assert isinstance(source_set.get_property_set(), list)
    source_set.set_property_set(None)
    assert isinstance(source_set.get_property_set(), list)
    assert len(source_set.get_property_set()) == 0
    db_close(dbref)


def test_004_07_all_rows_empty(db_create):
    dbref = db_create
    sources_set = SourceSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + sources_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(sources_set.get_property_set())
    assert count == sources_set.get_number_elements()
    db_close(dbref)


def test_004_08_selected_rows(db_create):
    dbref = db_create
    load_db_table(dbref, "sources", source_columns, source_value_set)
    sources_set = SourceSet(dbref, "source", "Victoria British")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + sources_set.get_table()
        + " WHERE source = 'Victoria British'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(sources_set.get_property_set())
    assert count == 1
    db_close(dbref)
