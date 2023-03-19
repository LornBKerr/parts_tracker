"""
Test the OrderSet class.

File:       test_012_order_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal, ElementSet
from test_setup import db_close, db_create, db_open, load_orders_table

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Order, OrderSet


def test_012__01_constr(db_create):
    dbref = db_create
    order_set = OrderSet(dbref)
    assert isinstance(order_set, OrderSet)
    db_close(dbref)


def test_012__02_get_dbref(db_create):
    dbref = db_create
    order_set = OrderSet(dbref)
    assert order_set.get_dbref() == dbref
    db_close(dbref)


def test_012__03_get_table(db_create):
    dbref = db_create
    order_set = OrderSet(dbref)
    assert order_set.get_table() == "orders"
    db_close(dbref)


def test_012__04_set_table(db_create):
    dbref = db_create
    order_set = OrderSet(dbref)
    order_set.set_table("orders")
    assert order_set.get_table() == "orders"
    db_close(dbref)


def test_012__05_get_property_set(db_create):
    dbref = db_create
    order_set = OrderSet(dbref)
    assert isinstance(order_set.get_property_set(), list)
    db_close(dbref)


def test_012__06_set_property_set_none(db_create):
    dbref = db_create
    order_set = OrderSet(dbref)
    assert isinstance(order_set.get_property_set(), list)
    order_set.set_property_set(None)
    assert isinstance(order_set.get_property_set(), list)
    assert len(order_set.get_property_set()) == 0
    db_close(dbref)


def test_012__07_all_rows_empty(db_create):
    dbref = db_create
    order_set = OrderSet(dbref)
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + order_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_set.get_property_set())
    assert count == order_set.get_number_elements()
    db_close(dbref)


def test_012__08_selected_rows(db_create):
    dbref = db_create
    load_orders_table(dbref)
    order_set = OrderSet(dbref, "source", "Local Purchase")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM "
        + order_set.get_table()
        + " WHERE source = 'Local Purchase'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    print("count =", count)
    selected_set = order_set.get_property_set()
    print("collected set =")
    print(selected_set)
    assert count == len(selected_set)
    assert count == 4
    db_close(dbref)
