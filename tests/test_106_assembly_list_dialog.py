"""
Test the AssemblyListDialog class.

File:       test_104_assembly_list_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""


# import os
# import sys
#
# import pytest
#
## from lbk_library import Dbal, Element
# from lbk_library.gui import Dialog
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox

#
##
## from pytestqt import qtbot
#
# src_path = os.path.join(os.path.realpath("."), "src")
# if src_path not in sys.path:
#    sys.path.append(src_path)
#
from test_setup import (
    build_test_config,
    db_close,
    db_create,
    db_open,
    filesystem,
    item_value_set,
    load_all_db_tables,
)

from dialogs import AssemblyListDialog, BaseDialog


# from elements import Item
#
#
### dummy function to represent the assembly tree page updating.
## def assy_tree_update_tree():
##    return
#
#
def setup_assembly_dialog(qtbot, db_create, filesystem):
    base_dir = file_system
    print(base_dir)
    dbref = db_create
    load_all_db_tables(dbref)
    main = QMainWindow()
    dialog = AssemblyListDialog(main, dbref, build_test_config())
    qtbot.addWidget(main)
    return (dbref, main, dialog)


def test_104_01_class_type(qtbot, db_create):
    dbref, main, dialog = setup_assembly_dialog(qtbot, db_create)


#    assert isinstance(dialog, AssemblyListDialog)
#    assert isinstance(dialog, BaseDialog)
#    assert isinstance(dialog, Dialog)
#    assert isinstance(dialog, QDialog)
#    db_close(dbref)
#
#
# def test_104_02_check_boxes_initial_conditon(qtbot, db_create):
#    dbref, main, dialog = setup_assembly_dialog(qtbot, db_create)
#
#    assert not dialog.form.xlsx_check_box.isEnabled()
#    assert dialog.form.csv_check_box.isChecked()
#
#
# def test_104_03_initial_location(qtbot, db_create):
#    dbref, main, dialog = setup_assembly_dialog(qtbot, db_create)
#
#    print(dialog.config)
#    assert 0
#
# def test_104_04_action_cancel(qtbot, db_create):
#    dbref, main, dialog = setup_assembly_dialog(qtbot, db_create)
#
#    def dialog_closed():
#        assert dialog.isHidden()
#
#    dialog.show()
#    assert not dialog.isHidden()
#    dialog.form.cancel_button.click()
#    qtbot.waitUntil(dialog_closed)
#    assert dialog.isHidden()
#    db_close(dbref)
#
#
# def test_104_05_action_start_changed(qtbot, db_create):
#    dbref, main, dialog = setup_assembly_dialog(qtbot, db_create)
#
#    # verify initial value is blank
#    assert dialog._start == ''
#    dialog.form.start_edit.editingFinished.emit()
#    assert dialog._start == ''
#    test_value = 'a'
#    dialog.form.start_edit.setText(test_value)
#    dialog.form.start_edit.editingFinished.emit()
#    assert dialog._start == test_value.upper()
#    assert dialog.form.start_edit.toolTip() == dialog.TOOLTIPS['start_assy']
#
#
# def test_104_06_action_end_changed(qtbot, db_create):
#    dbref, main, dialog = setup_assembly_dialog(qtbot, db_create)
#
#    # verify initial value is blank
#    assert dialog._end == ''
#    dialog.form.end_edit.editingFinished.emit()
#    assert dialog._end == ''
#    test_value = 'a'
#    dialog.form.end_edit.setText(test_value)
#    dialog.form.end_edit.editingFinished.emit()
#    assert dialog._end == test_value.upper()
#    assert dialog.form.end_edit.toolTip() == dialog.TOOLTIPS['end_assy']
#
#
#
