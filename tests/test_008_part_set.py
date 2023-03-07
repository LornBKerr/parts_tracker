import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal, ElementSet
from test_setup_elements import (
    close_database,
    create_parts_table,
    database_name,
    open_database,
)

from elements import Part, PartSet


def load_parts_table(dbref):
    columns = ["record_id", "part_number", "source", "description", "remarks"]
    value_set = [
        [
            "1786",
            "X081",
            "Local Purchase",
            "Rivet, Pop,1/8",
            "",
        ],
        ["1787", "X080", "None", "Fenders, Rear", ""],
        ["1788", "X079", "None", "O-Ring Gasket, 1/4 ID, 3/8 ID", ""],
        ["1789", "453-721", "Moss USA", "Dashboard", ""],
        ["1790", "15-112-BL", "Victoria British", "Radio Back Panel", ""],
        ["1791", "472-078", "Moss USA", "Radio Blanking Plate Set", ""],
        ["1792", "12-1124", "Victoria British", "Screw	Radio Console", ""],
        ["1793", "12-5304", "Victoria British", "Nut, Spire, Radio Console", ""],
        ["1794", "281-050", "Moss USA", "Grommet, 1 x 5/16	Choke Cable", ""],
        [
            "1795",
            "282-385",
            "Moss USA",
            "Grommet, 9/16x 3/16",
            "License Plate",
        ],
        ["1796", "324-655", "None", "Washer, Flat, 3/8 ID, 1 1/4 OD, 1/8 Thick", ""],
    ]
    sql_query = {"type": "INSERT", "table": "parts"}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(columns):
            entries[columns[i]] = values[i]
            i += 1
        sql = dbref.sql_query_from_array(sql_query, entries)
        dbref.sql_query(sql, entries)


def test_08_01_constr(open_database):
    dbref = open_database
    create_parts_table(dbref)
    part_set = PartSet(dbref)
    assert isinstance(part_set, PartSet)
    assert isinstance(part_set, ElementSet)
    close_database(dbref)


def test_08_02_get_dbref(open_database):
    dbref = open_database
    create_parts_table(dbref)
    part_set = PartSet(dbref)
    assert part_set.get_dbref() == dbref
    close_database(dbref)


def test_08_03_get_table(open_database):
    dbref = open_database
    create_parts_table(dbref)
    part_set = PartSet(dbref)
    assert part_set.get_table() == "parts"
    close_database(dbref)


def test_08_04_set_table(open_database):
    dbref = open_database
    create_parts_table(dbref)
    part_set = PartSet(dbref)
    part_set.set_table("items")
    assert part_set.get_table() == "items"
    close_database(dbref)


def test_08_05_get_property_set(open_database):
    dbref = open_database
    create_parts_table(dbref)
    part_set = PartSet(dbref)
    assert isinstance(part_set.get_property_set(), list)
    close_database(dbref)


def test_08_06_set_property_set_none(open_database):
    dbref = open_database
    create_parts_table(dbref)
    part_set = PartSet(dbref)
    assert isinstance(part_set.get_property_set(), list)
    part_set.set_property_set(None)
    assert isinstance(part_set.get_property_set(), list)
    assert len(part_set.get_property_set()) == 0
    close_database(dbref)


def test_08_07_all_rows_empty(open_database):
    dbref = open_database
    create_parts_table(dbref)
    part_set = PartSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + part_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    assert count == part_set.get_number_elements()
    assert part_set.get_number_elements() == 0
    close_database(dbref)


def test_08_08_selected_rows(open_database):
    dbref = open_database
    create_parts_table(dbref)
    load_parts_table(dbref)
    part_set = PartSet(dbref, "source", "Victoria British")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + part_set.get_table()
        + " WHERE source = 'Victoria British'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    assert count == 3
    close_database(dbref)


def test_02_09_ordered_selected_rows(open_database):
    dbref = open_database
    create_parts_table(dbref)
    load_parts_table(dbref)
    part_set = PartSet(dbref, "part_number", "BTB1108")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + part_set.get_table()
        + " WHERE part_number = 'BTB1108'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    selected_set = part_set.get_property_set()
    assert count == len(selected_set)
    for counter in range(0, count - 2):
        item1 = selected_set[counter]
        item2 = selected_set[counter + 1]
        assert item1.get_assembly() < item2.get_assembly()
    close_database(dbref)


def test_02_10_selected_rows_limit(open_database):
    dbref = open_database
    create_parts_table(dbref)
    load_parts_table(dbref)
    limit = 5
    part_set = PartSet(dbref, None, None, "record_id", limit)
    for part in part_set:
        print(part.get_properties())
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == 1786
    close_database(dbref)


def test_02_11_selected_rows_limit_offset(open_database):
    dbref = open_database
    create_parts_table(dbref)
    load_parts_table(dbref)
    limit = 5
    offset = 2
    part_set = PartSet(dbref, None, None, "record_id", limit, offset)
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == 1788
    close_database(dbref)


def test_02_12_iterator(open_database):
    dbref = open_database
    create_parts_table(dbref)
    load_parts_table(dbref)
    limit = 5
    part_set = PartSet(dbref, None, None, "record_id", limit)
    i = 1
    for item in part_set:
        assert item.get_record_id() == 1786 + i - 1
        i += 1
    close_database(dbref)


# end test_08_part_set.py
