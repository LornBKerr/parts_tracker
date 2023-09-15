"""
Test the BaseDialog class.

File:       test_101_base_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""


import os
import sys

from lbk_library import Dbal
from lbk_library.gui import Dialog
from PyQt5.QtWidgets import QDialog, QMainWindow, QTableWidget, QWidget
from test_setup import (
    db_create,
    db_open,
    dialog_form,
    load_db_table,
    order_columns,
    order_line_columns,
    order_line_value_set,
    order_value_set,
    part_columns,
    part_value_set,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from dialogs import BaseDialog


def test_101_01_class_type(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = BaseDialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    assert isinstance(dialog, BaseDialog)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)


def test_101_02_set_header_names(qtbot):
    column_names = ["col1", "col2"]
    column_widths = [40, 50]
    dbref = Dbal()
    main = QMainWindow()
    dialog = BaseDialog(main, dbref, Dialog.VIEW_ELEMENT)
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


def test_101_03_save_buttons_enable(qtbot, db_create):
    dbref = db_create
    main = QMainWindow()
    dialog = BaseDialog(main, dbref, Dialog.VIEW_ELEMENT)
    dialog.form = dialog_form(dialog)
    dialog.save_buttons_enable(False)
    assert not dialog.form.save_new_button.isEnabled()
    assert not dialog.form.save_done_button.isEnabled()
    dialog.save_buttons_enable(True)
    assert dialog.form.save_new_button.isEnabled()
    assert dialog.form.save_done_button.isEnabled()
    dialog.save_buttons_enable(False)
    assert not dialog.form.save_new_button.isEnabled()
    assert not dialog.form.save_done_button.isEnabled()


def test_101_04_file_order_table_fields(qtbot, db_create):
    dbref = db_create
    main = QMainWindow()
    dialog = BaseDialog(main, dbref, Dialog.VIEW_ELEMENT)
    dialog.form = dialog_form(dialog)
    load_db_table(dbref, "order_lines", order_line_columns, order_line_value_set)
    load_db_table(dbref, "orders", order_columns, order_value_set)
    load_db_table(dbref, "parts", part_columns, part_value_set)
    dialog.fill_order_table_fields(part_value_set[0][1])
    assert dialog.form.order_table.rowCount() == 1
    dialog.fill_order_table_fields("")
    assert dialog.form.order_table.rowCount() == 0
