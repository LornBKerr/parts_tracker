"""
Test the ItemSet class.

File:       test_010_order_line_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal, ElementSet

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import db_close, db_create, db_open, load_order_lines_table

from elements import OrderLine, OrderLineSet


def test_010_01_constr(db_create):
    dbref = db_create
    order_line_set = OrderLineSet(dbref)
    assert isinstance(order_line_set, OrderLineSet)
    assert isinstance(order_line_set, ElementSet)
    db_close(dbref)


def test_010_02_get_dbref(db_create):
    dbref = db_create
    order_line_set = OrderLineSet(dbref)
    assert order_line_set.get_dbref() == dbref
    db_close(dbref)


def test_010_03_get_table(db_create):
    dbref = db_create
    order_line_set = OrderLineSet(dbref)
    assert order_line_set.get_table() == "order_lines"
    db_close(dbref)


def test_010_04_set_table(db_create):
    dbref = db_create
    order_line_set = OrderLineSet(dbref)
    order_line_set.set_table("order_lines")
    assert order_line_set.get_table() == "order_lines"
    db_close(dbref)


def test_010_05_get_property_set(db_create):
    dbref = db_create
    order_line_set = OrderLineSet(dbref)
    assert isinstance(order_line_set.get_property_set(), list)
    db_close(dbref)


def test_010_06_set_property_set_none(db_create):
    dbref = db_create
    order_line_set = OrderLineSet(dbref)
    assert isinstance(order_line_set.get_property_set(), list)
    order_line_set.set_property_set(None)
    assert isinstance(order_line_set.get_property_set(), list)
    assert len(order_line_set.get_property_set()) == 0
    db_close(dbref)


def test_010_07_all_rows_empty(db_create):
    dbref = db_create
    order_line_set = OrderLineSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + order_line_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_line_set.get_property_set())
    assert count == order_line_set.get_number_elements()
    db_close(dbref)


def test_010_08_selected_rows(db_create):
    dbref = db_create
    load_order_lines_table(dbref)
    order_line_set = OrderLineSet(dbref, "order_number", "07-001")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + order_line_set.get_table()
        + " WHERE order_number = '07-001'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    print(order_line_set.get_property_set())
    assert count == len(order_line_set.get_property_set())
    assert count == 2
    db_close(dbref)
