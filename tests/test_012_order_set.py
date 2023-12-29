"""
Test the OrderSet class.

File:       test_012_order_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal, ElementSet
from test_setup import (
    db_close,
    db_create,
    db_open,
    filesystem,
    load_db_table,
    order_columns,
    order_value_set,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Order, OrderSet


def test_012_01_constr(filesystem):
    """
    OrderSet Extends ElementSet.

    The 'table' must be "orders" and 'dbref' needs to be the
    initializing dbref.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    order_set = OrderSet(dbref)
    assert isinstance(order_set, OrderSet)
    assert isinstance(order_set, ElementSet)
    assert order_set.get_table() == "orders"
    assert order_set.get_dbref() == dbref
    db_close(dbref)


def test_012_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Orders'", is empty when set to
    None or when the table is empty.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    order_set = OrderSet(dbref)
    assert isinstance(order_set.get_property_set(), list)
    order_set.set_property_set(None)
    assert isinstance(order_set.get_property_set(), list)
    assert len(order_set.get_property_set()) == 0
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + order_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_set.get_property_set())
    assert count == order_set.get_number_elements()
    db_close(dbref)


def test_012_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Orders', should contain the
    requested subset of Orders.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "orders", order_columns, order_value_set)
    order_set = OrderSet(dbref, "source", "Ebay")
    count_result = dbref.sql_query(
        "SELECT COUNT(*) FROM " + order_set.get_table() + " WHERE source = 'Ebay'"
    )
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_set.get_property_set())
    assert count == 1
    db_close(dbref)


def test_012_04_selected_rows_limit(filesystem):
    """
    The 'property_set', a list of 'Orders', should contain the
    requested subset of Orders ordered by record_id and the number of
    rows given by 'limit'.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "orders", order_columns, order_value_set)
    limit = 5
    order_set = OrderSet(dbref, None, None, "record_id", limit)
    assert limit == len(order_set.get_property_set())
    assert order_set.get_property_set()[0].get_record_id() == order_value_set[0][0]
    db_close(dbref)


def test_012_05_selected_rows_limit_offset(filesystem):
    """
    The 'property_set', a list of 'Orders', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "orders", order_columns, order_value_set)
    limit = 5
    offset = 2
    order_set = OrderSet(dbref, None, None, "record_id", limit, offset)
    assert limit == len(order_set.get_property_set())
    assert order_set.get_property_set()[0].get_record_id() == order_value_set[2][0]
    db_close(dbref)
