import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal, ElementSet
from test_setup_elements import close_database, database_name, open_database

from elements import ConditionSet


def create_conditions_table(dbref):
    dbref.sql_query("DROP TABLE IF EXISTS 'conditions'")
    create_table = 'CREATE TABLE "conditions" (record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, condition TEXT DEFAULT "")'
    result = dbref.sql_query(create_table)
    return dbref


def load_conditions_table(dbref):
    columns = ["record_id", "condition"]
    value_set = [
        [1, "Usable"],
        [2, "Replace"],
        [3, "Rebuild"],
        [4, "Missing"],
        [5, "New"],
        [6, "Unknown"],
    ]
    sql_query = {"type": "INSERT", "table": "conditions"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


def test_02_01_constr(open_database):
    dbref = open_database
    create_conditions_table(dbref)
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set, ConditionSet)
    assert isinstance(condition_set, ElementSet)
    close_database(dbref)


def test_02_02_get_dbref(open_database):
    dbref = open_database
    create_conditions_table(dbref)
    condition_set = ConditionSet(dbref)
    assert condition_set.get_dbref() == dbref
    close_database(dbref)


def test_02_03_get_table(open_database):
    dbref = open_database
    create_conditions_table(dbref)
    condition_set = ConditionSet(dbref)
    assert condition_set.get_table() == "conditions"
    close_database(dbref)


def test_02_04_set_table(open_database):
    dbref = open_database
    create_conditions_table(dbref)
    condition_set = ConditionSet(dbref)
    condition_set.set_table("items")
    assert condition_set.get_table() == "items"
    close_database(dbref)


def test_02_05_get_property_set(open_database):
    dbref = open_database
    create_conditions_table(dbref)
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set.get_property_set(), list)
    close_database(dbref)


def test_02_06_set_property_set_none(open_database):
    dbref = open_database
    create_conditions_table(dbref)
    condition_set = ConditionSet(dbref)
    assert isinstance(condition_set.get_property_set(), list)
    condition_set.set_property_set(None)
    assert isinstance(condition_set.get_property_set(), list)
    assert len(condition_set.get_property_set()) == 0
    close_database(dbref)


def test_02_07_all_rows_empty(open_database):
    dbref = open_database
    create_conditions_table(dbref)
    conditions_set = ConditionSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + conditions_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(conditions_set.get_property_set())
    assert count == conditions_set.get_number_elements()
    close_database(dbref)


def test_02_08_selected_rows(open_database):
    dbref = open_database
    create_conditions_table(dbref)
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
    close_database(dbref)


# end test_02_condition_set
