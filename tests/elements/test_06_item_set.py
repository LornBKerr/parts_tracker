import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal, ElementSet

from elements import Item, ItemSet

from test_setup_elements import (
    database_name, close_database, open_database, create_items_table
)

def load_items_table(dbref):
    columns = [
        "record_id",
        "part_number",
        "assembly",
        "quantity",
        "condition",
        "installed",
        "box",
        "remarks",
    ]
    value_set = [
        ["1", "18V672", "A", "1", "Rebuild", "1", "", ""],
        ["2", "BTB1108", "B", "1", "Usable", "0", "", ""],
        ["3", "X036", "D", "1", "Usable", "0", "", ""],
        ["4", "BTB1108", "CA", "1", "Usable", "0", "", ""],
        ["5", "22H1053", "BB", "1", "Usable", "0", "", ""],
        ["6", "268-090", "BC", "1", "Usable", "1", "", ""],
        ["8", "BTB1108", "BD", "1", "Usable", "1", "", ""],
        ["9", "X055", "EB", "1", "Usable", "1", "", ""],
        ["56", "BULB-1895", "JCIB", "2", "Replace", "1", "", "License Plate Lamp"],
        ["59", "158-520", "JCIA", "2", "Replace", "1", "", ""],
        ["70", "BTB1108", "CX", "1", "Usable", "1", "", ""],
    ]
    sql_query = {"type": "INSERT", "table": "items"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


def test_06_01_constructor(open_database):
    dbref = open_database
    create_items_table(dbref)
    item_set = ItemSet(dbref)
    assert isinstance(item_set, ItemSet)
    assert isinstance(item_set, ElementSet)
    close_database(dbref)


def test_06_02_get_dbref(open_database):
    dbref = open_database
    create_items_table(dbref)
    item_set = ItemSet(dbref)
    assert item_set.get_dbref() == dbref
    close_database(dbref)


def test_06_03_get_table(open_database):
    dbref = open_database
    create_items_table(dbref)
    item_set = ItemSet(dbref)
    assert item_set.get_table() == "items"
    close_database(dbref)


def test_06_04_set_table(open_database):
    dbref = open_database
    create_items_table(dbref)
    item_set = ItemSet(dbref)
    item_set.set_table("parts")
    assert item_set.get_table() == "parts"
    close_database(dbref)


def test_06_05_get_property_set(open_database):
    dbref = open_database
    create_items_table(dbref)
    item_set = ItemSet(dbref)
    assert isinstance(item_set.get_property_set(), list)
    close_database(dbref)


def test_06_06_set_property_set_none(open_database):
    dbref = open_database
    create_items_table(dbref)
    item_set = ItemSet(dbref)
    assert isinstance(item_set.get_property_set(), list)
    item_set.set_property_set(None)
    assert isinstance(item_set.get_property_set(), list)
    assert len(item_set.get_property_set()) == 0
    close_database(dbref)


def test_06_07_all_rows_empty(open_database):
    dbref = open_database
    create_items_table(dbref)
    item_set = ItemSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + item_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    assert count == item_set.get_number_elements()
    close_database(dbref)


def test_06_08_selected_rows(open_database):
    dbref = open_database
    create_items_table(dbref)
    load_items_table(dbref)
    item_set = ItemSet(dbref, "part_number", "BTB1108")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + item_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(item_set.get_property_set())
    close_database(dbref)


def test_06_09_ordered_selected_rows(open_database):
    dbref = open_database
    create_items_table(dbref)
    load_items_table(dbref)
    item_set = ItemSet(dbref, "part_number", "BTB1108", "assembly")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + item_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    selected_set = item_set.get_property_set()
    assert count == len(selected_set)
    for counter in range(0, count - 2):
        item1 = selected_set[counter]
        item2 = selected_set[counter + 1]
        assert item1.get_assembly() < item2.get_assembly()
    close_database(dbref)


def test_06_10_selected_rows_limit(open_database):
    dbref = open_database
    create_items_table(dbref)
    load_items_table(dbref)
    limit = 5
    item_set = ItemSet(dbref, None, None, "record_id", limit)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 1
    close_database(dbref)


def test_06_11_selected_rows_limit_offset(open_database):
    dbref = open_database
    create_items_table(dbref)
    load_items_table(dbref)
    limit = 5
    offset = 2
    item_set = ItemSet(dbref, None, None, "record_id", limit, offset)
    assert limit == len(item_set.get_property_set())
    assert item_set.get_property_set()[0].get_record_id() == 3
    close_database(dbref)


def test_06_12_iterator(open_database):
    dbref = open_database
    create_items_table(dbref)
    load_items_table(dbref)
    limit = 5
    item_set = ItemSet(dbref, None, None, "record_id", limit)
    i = 1
    for item in item_set:
        assert item.get_record_id() == i
        i += 1
    close_database(dbref)


# end test_02_elements_item_set.py
