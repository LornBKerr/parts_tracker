"""
Test the BaseDialog class.

File:       test_101_base_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
Version     1.0.0
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import DataFile
from lbk_library.gui import Dialog
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
    load_datafile_table,
)
from PyQt5 import uic  # QtCore,
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QTableWidget,
    QWidget,
)
from test_setup import (
    order_columns,
    order_line_columns,
    order_line_value_set,
    order_value_set,
    part_columns,
    part_value_set,
)

from dialogs import BaseDialog
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


def test_101_01_class_type(qtbot):
    parts_file = DataFile()
    main = QMainWindow()
    dialog = BaseDialog(main, parts_file, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    assert isinstance(dialog, BaseDialog)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)


def test_101_02_set_header_names(qtbot):
    column_names = ["col1", "col2"]
    column_widths = [40, 50]
    parts_file = DataFile()
    main = QMainWindow()
    dialog = BaseDialog(main, parts_file, Dialog.VIEW_ELEMENT)
    test_table = QTableWidget(2, 7, dialog)
    test_table.resize(80, 80)
    qtbot.addWidget(main)
    dialog.set_table_header(test_table, column_names, column_widths)
    assert test_table.columnCount() == len(column_names)
    assert test_table.columnWidth(0) == column_widths[0]
    assert test_table.columnWidth(1) == column_widths[1]
    assert test_table.horizontalHeaderItem(0).text() == column_names[0]
    assert test_table.horizontalHeaderItem(1).text() == column_names[1]
    dialog.set_table_header(test_table, column_names, column_widths, 1)


def test_101_03_save_buttons_enable(qtbot):
    main = QMainWindow()
    dialog = BaseDialog(main, None, Dialog.VIEW_ELEMENT)
    dialog.form = uic.loadUi("tests/base_dialog_test.ui", None)
    dialog.save_buttons_enable(False)
    assert not dialog.form.save_new_button.isEnabled()
    assert not dialog.form.save_done_button.isEnabled()
    dialog.save_buttons_enable(True)
    assert dialog.form.save_new_button.isEnabled()
    assert dialog.form.save_done_button.isEnabled()
    dialog.save_buttons_enable(False)
    assert not dialog.form.save_new_button.isEnabled()
    assert not dialog.form.save_done_button.isEnabled()


def test_101_04_fill_order_table_fields(qtbot, filesystem):
    filename = filesystem + "/test_101_04.parts"
    parts_file = datafile_create(filename, table_definition)
    main = QMainWindow()
    dialog = BaseDialog(main, parts_file, Dialog.VIEW_ELEMENT)
    dialog.form = uic.loadUi("tests/base_dialog_test.ui", None)
    dialog.set_table_header(
        dialog.form.order_table,
        dialog.PART_ORDER_COL_NAMES,
        dialog.PART_ORDER_COL_WIDTHS,
    )
    load_datafile_table(
        parts_file, "order_lines", order_line_columns, order_line_value_set
    )
    load_datafile_table(parts_file, "orders", order_columns, order_value_set)
    load_datafile_table(parts_file, "parts", part_columns, part_value_set)
    dialog.fill_order_table_fields(part_value_set[0][1])
    assert dialog.form.order_table.rowCount() == 2
    dialog.fill_order_table_fields("")
    assert dialog.form.order_table.rowCount() == 0
    datafile_close(parts_file)
