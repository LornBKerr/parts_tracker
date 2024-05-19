"""
Test the orders list_page class.

File:       test_203_orders_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from lbk_library.testing_support import datafile_close, datafile_create, filesystem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
from test_setup import load_all_datafile_tables, order_value_set

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from dialogs import OrderDialog
from elements import Order, OrderSet
from pages import OrdersListPage, table_definition

parts_filename = "parts_test.parts"


def setup_page(qtbot, filesystem):
    """Initialize  parts list page for testing"""
    filename = filesystem + "/" + parts_filename
    parts_file = datafile_create(filename, table_definition)
    load_all_datafile_tables(parts_file)
    table = QTableWidget()
    page = OrdersListPage(table, parts_file)
    qtbot.addWidget(table)
    return (parts_file, table, page)


def test_203_01_class_type(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)
    assert isinstance(page, OrdersListPage)
    assert page.get_parts_file() == parts_file
    assert type(page.table) == QTableWidget
    assert page.table == table
    datafile_close(parts_file)


def test_203_02_get_number_lines(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)
    order_number = "06-015"
    count_result = parts_file.sql_query(
        "SELECT COUNT(*) FROM order_lines WHERE order_number = '06-015'"
    )
    count = parts_file.sql_fetchrow(count_result)["COUNT(*)"]
    assert page.get_number_lines("06-015") == count
    datafile_close(parts_file)


def test_203_03_set_table_headers(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)
    page.table.clear()
    page.table.setColumnCount(0)
    assert page.table.columnCount() == 0

    page.set_table_headers()
    assert page.table.columnCount() == len(page.COLUMN_NAMES)
    header = page.table.horizontalHeader()
    for i in range(1, len(page.COLUMN_NAMES) - 1):
        assert (
            header.model().headerData(i, header.orientation()) == page.COLUMN_NAMES[i]
        )
        assert page.table.columnWidth(i) > header.minimumSectionSize()
    datafile_close(parts_file)


def test_203_04_update_table(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)

    order_set = OrderSet(parts_file, None, None, "order_number")
    initial_num_parts = page.table.rowCount()
    Order(parts_file, order_value_set[0][1], "order_number").delete()
    Order(parts_file, order_value_set[1][1], "order_number").delete()
    page.update_table()
    assert page.table.rowCount() < initial_num_parts
    assert (initial_num_parts - page.table.rowCount()) == 2
    assert not page.table.findItems(order_value_set[0][1], Qt.MatchExactly)
    assert not page.table.findItems(order_value_set[1][1], Qt.MatchExactly)
    datafile_close(parts_file)


def test_203_05_clear_table(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)
    page.clear_table()
    assert page.table.rowCount() == 0
    datafile_close(parts_file)


def test_203_06_action_order_clicked(qtbot, filesystem):
    parts_file, table, page = setup_page(qtbot, filesystem)
    order_item = page.table.itemAt(0, 0)
    dialog = page.action_order_clicked(order_item)
    assert type(dialog) == OrderDialog
    datafile_close(parts_file)
