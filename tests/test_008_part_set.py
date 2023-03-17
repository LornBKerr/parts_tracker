import os
import sys

import pytest
from lbk_library import Dbal, ElementSet

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import db_close, db_create, db_open, load_parts_table

from elements import Part, PartSet


def test_08_01_constr(db_create):
    dbref = db_create
    part_set = PartSet(dbref)
    assert isinstance(part_set, PartSet)
    assert isinstance(part_set, ElementSet)
    db_close(dbref)


def test_08_02_get_dbref(db_create):
    dbref = db_create
    part_set = PartSet(dbref)
    assert part_set.get_dbref() == dbref
    db_close(dbref)


def test_08_03_get_table(db_create):
    dbref = db_create
    part_set = PartSet(dbref)
    assert part_set.get_table() == "parts"
    db_close(dbref)


def test_08_04_set_table(db_create):
    dbref = db_create
    part_set = PartSet(dbref)
    part_set.set_table("items")
    assert part_set.get_table() == "items"
    db_close(dbref)


def test_08_05_get_property_set(db_create):
    dbref = db_create
    part_set = PartSet(dbref)
    assert isinstance(part_set.get_property_set(), list)
    db_close(dbref)


def test_08_06_set_property_set_none(db_create):
    dbref = db_create
    part_set = PartSet(dbref)
    assert isinstance(part_set.get_property_set(), list)
    part_set.set_property_set(None)
    assert isinstance(part_set.get_property_set(), list)
    assert len(part_set.get_property_set()) == 0
    db_close(dbref)


def test_08_07_all_rows_empty(db_create):
    dbref = db_create
    part_set = PartSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + part_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(part_set.get_property_set())
    assert count == part_set.get_number_elements()
    assert part_set.get_number_elements() == 0
    db_close(dbref)


def test_08_08_selected_rows(db_create):
    dbref = db_create
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
    db_close(dbref)


def test_02_09_ordered_selected_rows(db_create):
    dbref = db_create
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
    db_close(dbref)


def test_02_10_selected_rows_limit(db_create):
    dbref = db_create
    load_parts_table(dbref)
    limit = 5
    part_set = PartSet(dbref, None, None, "record_id", limit)
    for part in part_set:
        print(part.get_properties())
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == 1786
    db_close(dbref)


def test_02_11_selected_rows_limit_offset(db_create):
    dbref = db_create
    load_parts_table(dbref)
    limit = 5
    offset = 2
    part_set = PartSet(dbref, None, None, "record_id", limit, offset)
    assert limit == len(part_set.get_property_set())
    assert part_set.get_property_set()[0].get_record_id() == 1788
    db_close(dbref)


def test_02_12_iterator(db_create):
    dbref = db_create
    load_parts_table(dbref)
    limit = 5
    part_set = PartSet(dbref, None, None, "record_id", limit)
    i = 1
    for item in part_set:
        assert item.get_record_id() == 1786 + i - 1
        i += 1
    db_close(dbref)
