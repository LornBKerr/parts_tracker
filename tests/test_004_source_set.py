import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal, ElementSet
from test_setup_elements import close_database, database_name, open_database

from elements import SourceSet


def create_sources_table(dbref):
    dbref.sql_query("DROP TABLE IF EXISTS 'sources'")
    create_table = 'CREATE TABLE "sources" (record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, source TEXT DEFAULT "")'
    result = dbref.sql_query(create_table)
    return dbref


def load_sources_table(dbref):
    columns = ["record_id", "source"]
    value_set = [
        [1, "Moss USA"],
        [2, "Victoria British"],
        [3, "B-Hive"],
        [4, "Moss Europe"],
        [5, "Roadster Factory"],
        [6, "McMaster-Carr"],
        [7, "None"],
        [8, "Fastenal"],
        [9, "British Parts Northwest"],
        [10, "Ebay"],
        [11, "Advanced Auto Wire"],
        [12, "Little British Car Co"],
        [13, "Strapping Lad Suspension"],
        [14, "Local Purchase"],
        [15, "Tire Rack"],
    ]
    sql_query = {"type": "INSERT", "table": "sources"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


def test_04_01_constr(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source_set = SourceSet(dbref)
    assert isinstance(source_set, SourceSet)
    assert isinstance(source_set, ElementSet)
    close_database(dbref)


def test_04_02_get_dbref(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source_set = SourceSet(dbref)
    assert source_set.get_dbref() == dbref
    close_database(dbref)


def test_04_03_get_table(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source_set = SourceSet(dbref)
    assert source_set.get_table() == "sources"
    close_database(dbref)


def test_04_04_set_table(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source_set = SourceSet(dbref)
    source_set.set_table("items")
    assert source_set.get_table() == "items"
    close_database(dbref)


def test_04_05_get_property_set(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source_set = SourceSet(dbref)
    assert isinstance(source_set.get_property_set(), list)
    close_database(dbref)


def test_04_06_set_property_set_none(open_database):
    dbref = open_database
    create_sources_table(dbref)
    source_set = SourceSet(dbref)
    assert isinstance(source_set.get_property_set(), list)
    source_set.set_property_set(None)
    assert isinstance(source_set.get_property_set(), list)
    assert len(source_set.get_property_set()) == 0
    close_database(dbref)


def test_04_07_all_rows_empty(open_database):
    dbref = open_database
    create_sources_table(dbref)
    sources_set = SourceSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + sources_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(sources_set.get_property_set())
    assert count == sources_set.get_number_elements()
    close_database(dbref)


def test_04_08_selected_rows(open_database):
    dbref = open_database
    create_sources_table(dbref)
    load_sources_table(dbref)
    sources_set = SourceSet(dbref, "source", "Victoria British")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + sources_set.get_table()
        + " WHERE source = 'Victoria British'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(sources_set.get_property_set())
    assert count == 1
    close_database(dbref)


# end test_02_source_set
