"""
Test the OrderLineSet class.

File:       test_010_order_line_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import Dbal, ElementSet

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import (
    db_close,
    db_create,
    db_open,
    filesystem,
    load_db_table,
    order_line_columns,
    order_line_value_set,
)

from elements import OrderLine, OrderLineSet


def test_010_01_constr(filesystem):
    """
    OrderLineSet Extends ElementSet.

    The 'table' must be "order_lines" and 'dbref' needs to be the
    initializing dbref.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    order_line_set = OrderLineSet(dbref)
    assert isinstance(order_line_set, OrderLineSet)
    assert isinstance(order_line_set, ElementSet)
    assert order_line_set.get_table() == "order_lines"
    assert order_line_set.get_dbref() == dbref
    db_close(dbref)


def test_010_02_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Parts'", is empty when set to
    None or when the table is empty.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    order_line_set = OrderLineSet(dbref)
    assert isinstance(order_line_set.get_property_set(), list)
    order_line_set.set_property_set(None)
    assert isinstance(order_line_set.get_property_set(), list)
    assert len(order_line_set.get_property_set()) == 0
    count_result = dbref.sql_query("SELECT COUNT(*) FROM " + order_line_set.get_table())
    count = dbref.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_line_set.get_property_set())
    assert count == order_line_set.get_number_elements()
    db_close(dbref)


def test_010_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'OrderLinesarts', should contain the
    requested subset of OrderLines.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "order_lines", order_line_columns, order_line_value_set)
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


def test_008_4_selected_rows_limit(filesystem):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit'.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "order_lines", order_line_columns, order_line_value_set)
    limit = 5
    order_line_set = OrderLineSet(dbref, None, None, "record_id", limit)
    assert limit == len(order_line_set.get_property_set())
    assert (
        order_line_set.get_property_set()[0].get_record_id()
        == order_line_value_set[0][0]
    )
    db_close(dbref)


def test_008_05_selected_rows_limit_offset(filesystem):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    fs_base = filesystem
    dbref = db_create(fs_base)
    load_db_table(dbref, "order_lines", order_line_columns, order_line_value_set)
    limit = 5
    offset = 2
    order_line_set = OrderLineSet(dbref, None, None, "record_id", limit, offset)
    assert limit == len(order_line_set.get_property_set())
    assert (
        order_line_set.get_property_set()[0].get_record_id()
        == order_line_value_set[2][0]
    )
    db_close(dbref)
