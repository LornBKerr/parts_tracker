"""
Test the OrderSet class.

File:       test_012_order_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library import ElementSet
from test_data import order_columns, order_value_set
from test_setup import (
    filesystem,
    load_parts_file_table,
    parts_file_close,
    parts_file_create,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from elements import Order, OrderSet
from pages import table_definition

parts_filename = "parts_test.parts"


def base_setup(filesystem):
    filename = filesystem + "/" + parts_filename
    parts_file = parts_file_create(filename, table_definition)
    order_set = OrderSet(parts_file)
    return (order_set, parts_file)


def test_012_01_constr(filesystem):
    """
    OrderSet Extends ElementSet.

    The 'table' must be "orders" and 'parts_file' needs to be the
    initializing parts_file.
    """
    order_set, parts_file = base_setup(filesystem)
    assert isinstance(order_set, OrderSet)
    assert isinstance(order_set, ElementSet)
    assert order_set.get_table() == "orders"
    assert order_set.get_datafile() == parts_file
    parts_file_close(parts_file)


def test_012_02_set_property_set_empty(filesystem):
    """
    The 'property_set', a list of 'Orders'", is empty when set to
    None or when the table is empty.
    """
    order_set, parts_file = base_setup(filesystem)
    assert isinstance(order_set.get_property_set(), list)
    order_set.set_property_set(None)
    assert isinstance(order_set.get_property_set(), list)
    assert len(order_set.get_property_set()) == 0
    count_result = parts_file.sql_query("SELECT COUNT(*) FROM " + order_set.get_table())
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_set.get_property_set())
    assert count == order_set.get_number_elements()
    parts_file_close(parts_file)


def test_012_03_selected_rows(filesystem):
    """
    The 'property_set', a list of 'Orders', should contain the
    requested subset of Orders.
    """
    order_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "orders", order_columns, order_value_set)
    order_set = OrderSet(parts_file, "source", "Ebay")
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM " + order_set.get_table() + " WHERE source = 'Ebay'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_set.get_property_set())
    assert count == 1
    parts_file_close(parts_file)


def test_012_04_selected_rows_limit(filesystem):
    """
    The 'property_set', a list of 'Orders', should contain the
    requested subset of Orders ordered by record_id and the number of
    rows given by 'limit'.
    """
    order_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "orders", order_columns, order_value_set)
    limit = 5
    order_set = OrderSet(parts_file, None, None, "record_id", limit)
    assert limit == len(order_set.get_property_set())
    assert order_set.get_property_set()[0].get_record_id() == order_value_set[0][0]
    parts_file_close(parts_file)


def test_012_05_selected_rows_limit_offset(filesystem):
    """
    The 'property_set', a list of 'Orders', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    order_set, parts_file = base_setup(filesystem)
    load_parts_file_table(parts_file, "orders", order_columns, order_value_set)
    limit = 5
    offset = 2
    order_set = OrderSet(parts_file, None, None, "record_id", limit, offset)
    assert limit == len(order_set.get_property_set())
    assert order_set.get_property_set()[0].get_record_id() == order_value_set[2][0]
    parts_file_close(parts_file)
