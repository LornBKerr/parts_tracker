"""
Test the OrderLineSet class.

File:       test_010_order_line_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import ElementSet
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
    load_datafile_table,
)
from test_data import order_line_columns, order_line_value_set

from elements import OrderLine, OrderLineSet
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}

parts_filename = "parts_test.parts"


def base_setup(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    order_line_set = OrderLineSet(parts_file)
    return (order_line_set, parts_file)


def test_010_01_constr(tmp_path):
    """
    OrderLineSet Extends ElementSet.

    The 'table' must be "order_lines" and 'parts_file' needs to be the
    initializing parts_file.
    """
    order_line_set, parts_file = base_setup(tmp_path)
    assert isinstance(order_line_set, OrderLineSet)
    assert isinstance(order_line_set, ElementSet)
    assert order_line_set.get_table() == "order_lines"
    assert order_line_set.get_datafile() == parts_file
    datafile_close(parts_file)


def test_010_02_property_set_empty(tmp_path):
    """
    The 'property_set', a list of 'Parts'", is empty when set to
    None or when the table is empty.
    """
    order_line_set, parts_file = base_setup(tmp_path)
    assert isinstance(order_line_set.get_property_set(), list)
    order_line_set.set_property_set(None)
    assert isinstance(order_line_set.get_property_set(), list)
    assert len(order_line_set.get_property_set()) == 0
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM " + order_line_set.get_table()
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_line_set.get_property_set())
    assert count == order_line_set.get_number_elements()
    datafile_close(parts_file)


def test_010_03_selected_rows(tmp_path):
    """
    The 'property_set', a list of 'OrderLinesarts', should contain the
    requested subset of OrderLines.
    """
    order_line_set, parts_file = base_setup(tmp_path)
    load_datafile_table(
        parts_file, "order_lines", order_line_columns, order_line_value_set
    )
    order_line_set = OrderLineSet(parts_file, "order_number", "07-001")
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM "
        + order_line_set.get_table()
        + " WHERE order_number = '07-001'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert count == len(order_line_set.get_property_set())
    assert count == 2
    datafile_close(parts_file)


def test_008_4_selected_rows_limit(tmp_path):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit'.
    """
    order_line_set, parts_file = base_setup(tmp_path)
    load_datafile_table(
        parts_file, "order_lines", order_line_columns, order_line_value_set
    )
    limit = 5
    order_line_set = OrderLineSet(parts_file, None, None, "record_id", limit)
    assert limit == len(order_line_set.get_property_set())
    assert (
        order_line_set.get_property_set()[0].get_record_id()
        == order_line_value_set[0][0]
    )
    datafile_close(parts_file)


def test_008_05_selected_rows_limit_offset(tmp_path):
    """
    The 'property_set', a list of 'Parts', should contain the
    requested subset of Items ordered by record_id and the number of
    rows given by 'limit' starting at 'offset' number of records.
    """
    order_line_set, parts_file = base_setup(tmp_path)
    load_datafile_table(
        parts_file, "order_lines", order_line_columns, order_line_value_set
    )
    limit = 5
    offset = 2
    order_line_set = OrderLineSet(parts_file, None, None, "record_id", limit, offset)
    assert limit == len(order_line_set.get_property_set())
    assert (
        order_line_set.get_property_set()[0].get_record_id()
        == order_line_value_set[2][0]
    )
    datafile_close(parts_file)
