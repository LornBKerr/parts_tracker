"""
Test the Dialog Support class.

File:       test_101_dialog_support.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
Version     1.1.0
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)


from lbk_library import DataFile as PartsFile
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
    load_datafile_table,
)
from PySide6.QtWidgets import QTableWidget  # QPushButton,
from test_data import (
    order_columns,
    order_line_columns,
    order_line_value_set,
    order_value_set,
    part_columns,
    part_value_set,
)

from dialogs import (  # ; buttons_enable,; ;
    PART_ORDER_COL_NAMES,
    PART_ORDER_COL_WIDTHS,
    fill_order_table_fields,
    set_table_header,
)
from pages import table_definition

file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.1.0": "Revised to match the refactored dialog_support.py file",
}


def test_101_01_part_order_table_constants():
    col_names = PART_ORDER_COL_NAMES
    assert col_names[0] == "Order"
    assert col_names[1] == "Date"
    assert col_names[2] == "Source"
    assert col_names[3] == "Line"
    assert col_names[4] == "Part Number"
    assert col_names[5] == "Cost Each"
    assert col_names[6] == "Quantity"
    assert col_names[7] == "Remarks"

    col_widths = PART_ORDER_COL_WIDTHS
    assert col_widths[0] == 60
    assert col_widths[1] == 100
    assert col_widths[2] == 60
    assert col_widths[3] == 40
    assert col_widths[4] == 120
    assert col_widths[5] == 70
    assert col_widths[6] == 100
    assert col_widths[7] == 1


def test_101_02_set_header_names(qtbot):
    column_names = ["col1", "col2"]
    column_widths = [40, 50]
    parts_file = PartsFile()

    test_table = QTableWidget(2, 7)
    test_table.resize(80, 80)
    qtbot.addWidget(test_table)
    set_table_header(test_table, column_names, column_widths)
    assert test_table.columnCount() == len(column_names)
    assert test_table.columnWidth(0) == column_widths[0]
    assert test_table.columnWidth(1) == column_widths[1]
    assert test_table.horizontalHeaderItem(0).text() == column_names[0]
    assert test_table.horizontalHeaderItem(1).text() == column_names[1]
    set_table_header(test_table, column_names, column_widths, 1)
    assert test_table.columnCount() == len(column_names)
    assert test_table.columnWidth(0) == column_widths[0]
    assert not test_table.columnWidth(1) == column_widths[1]
    assert test_table.horizontalHeaderItem(0).text() == column_names[0]
    assert test_table.horizontalHeaderItem(1).text() == column_names[1]


# def test_101_03_save_buttons_enable(qtbot):
#    button1 = QPushButton()
#    button2 = QPushButton()
#    buttons = [button1, button2]
#    buttons_enable(buttons, False)
#    assert not button1.isEnabled()
#    assert not button2.isEnabled()
#    buttons_enable(buttons, True)
#    assert button1.isEnabled()
#    assert button2.isEnabled()
#    buttons_enable(buttons, False)
#    assert not button1.isEnabled()
#    assert not button2.isEnabled()


def test_101_04_fill_order_table_fields(qtbot, tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + "/test_101_04.parts"
    parts_file = datafile_create(filename, table_definition)
    test_table = QTableWidget(2, 7)
    test_table.resize(80, 80)
    qtbot.addWidget(test_table)
    load_datafile_table(
        parts_file, "order_lines", order_line_columns, order_line_value_set
    )
    load_datafile_table(parts_file, "orders", order_columns, order_value_set)
    load_datafile_table(parts_file, "parts", part_columns, part_value_set)
    fill_order_table_fields(parts_file, part_value_set[0][1], test_table)
    assert test_table.rowCount() == 2
    fill_order_table_fields(parts_file, "", test_table)
    assert test_table.rowCount() == 0
    datafile_close(parts_file)
