"""
Test the EditStructureDialog class.

File:       test_103_edit_structure_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

# import pytest
# from lbk_library import Dbal, Element
from lbk_library.gui import Dialog
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox

# from pytestqt import qtbot
#
src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import db_close, db_create, db_open, item_value_set, load_all_db_tables

from dialogs import EditStructureDialog
from elements import Item


# dummy function to represent the assembly tree page updating.
def assy_tree_update_tree():
    return


def setup_edit_structure_dialog(qtbot, db_create):
    dbref = db_create
    load_all_db_tables(dbref)
    main = QMainWindow()
    dialog = EditStructureDialog(dbref, None, Dialog.EDIT_ELEMENT)
    qtbot.addWidget(main)
    qtbot.addWidget(dialog)
    return (dbref, main, dialog)


def test_103_01_class_type(qtbot, db_create):
    dbref, main, dialog = setup_edit_structure_dialog(qtbot, db_create)

    assert isinstance(dialog, EditStructureDialog)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)
    db_close(dbref)


def test_103_02_action_cancel(qtbot, db_create):
    dbref, main, dialog = setup_edit_structure_dialog(qtbot, db_create)

    def dialog_closed():
        assert dialog.isHidden()

    dialog.show()
    assert not dialog.isHidden()
    dialog.close_button.click()
    qtbot.waitUntil(dialog_closed)
    assert dialog.closed
    db_close(dbref)


def test_103_03_action_old_assy_changed(qtbot, db_create):
    dbref, main, dialog = setup_edit_structure_dialog(qtbot, db_create)

    test_value = "s"  # valid test: single character using editFinished signal
    dialog.form.old_assy_edit.setText(test_value)
    dialog.form.old_assy_edit.editingFinished.emit()
    assert dialog.form.old_assy_edit.text() == test_value.upper()
    assert dialog.form.old_assy_edit.toolTip() == dialog.TOOLTIPS["old_assy_edit"]
    assert (
        dialog.form.old_assy_edit.toolTip()
        == EditStructureDialog.TOOLTIPS["old_assy_edit"]
    )
    assert not dialog.form.old_assy_edit.error
    assert not dialog.form.old_assy_frame.error

    test_value = "abcdefghijklmno"  # valid test: 15 characters
    dialog.form.old_assy_edit.setText(test_value)
    dialog.form.old_assy_edit.editingFinished.emit()
    assert dialog.form.old_assy_edit.text() == test_value.upper()
    assert dialog.form.old_assy_edit.toolTip() == dialog.TOOLTIPS["old_assy_edit"]
    assert (
        dialog.form.old_assy_edit.toolTip()
        == EditStructureDialog.TOOLTIPS["old_assy_edit"]
    )
    assert not dialog.form.old_assy_edit.error
    assert not dialog.form.old_assy_frame.error

    test_value = "aabcdefghijklmno"  # invalid test: 16 characters
    dialog.form.old_assy_edit.setText(test_value)
    result = dialog.action_old_assy_changed()
    assert not result["valid"]
    assert dialog.form.old_assy_edit.text() == test_value.upper()
    assert result["msg"] in dialog.form.old_assy_edit.toolTip()
    assert dialog.TOOLTIPS["old_assy_edit"] in dialog.form.old_assy_edit.toolTip()
    assert dialog.form.old_assy_edit.error
    assert dialog.form.old_assy_frame.error

    test_value = ""  # invalid test: 0 characters
    test_value = "aabcdefghijklmno"  # invalid test: 16 characters
    dialog.form.old_assy_edit.setText(test_value)
    result = dialog.action_old_assy_changed()
    assert not result["valid"]
    assert dialog.form.old_assy_edit.text() == test_value.upper()
    assert result["msg"] in dialog.form.old_assy_edit.toolTip()
    assert dialog.TOOLTIPS["old_assy_edit"] in dialog.form.old_assy_edit.toolTip()
    assert dialog.form.old_assy_edit.error
    assert dialog.form.old_assy_frame.error


def test_103_04_action_new_assy_changed(qtbot, db_create):
    dbref, main, dialog = setup_edit_structure_dialog(qtbot, db_create)

    test_value = "s"  # valid test: single character using editFinished signal
    dialog.form.new_assy_edit.setText(test_value)
    dialog.form.new_assy_edit.editingFinished.emit()
    assert dialog.form.new_assy_edit.text() == test_value.upper()
    assert dialog.form.new_assy_edit.toolTip() == dialog.TOOLTIPS["new_assy_edit"]
    assert (
        dialog.form.new_assy_edit.toolTip()
        == EditStructureDialog.TOOLTIPS["new_assy_edit"]
    )
    assert not dialog.form.new_assy_edit.error
    assert not dialog.form.new_assy_frame.error

    test_value = "abcdefghijklmno"  # valid test: 15 characters
    dialog.form.new_assy_edit.setText(test_value)
    dialog.form.new_assy_edit.editingFinished.emit()
    assert dialog.form.new_assy_edit.text() == test_value.upper()
    assert dialog.form.new_assy_edit.toolTip() == dialog.TOOLTIPS["new_assy_edit"]
    assert (
        dialog.form.new_assy_edit.toolTip()
        == EditStructureDialog.TOOLTIPS["new_assy_edit"]
    )
    assert not dialog.form.new_assy_edit.error
    assert not dialog.form.new_assy_frame.error

    test_value = "aabcdefghijklmno"  # invalid test: 16 characters
    dialog.form.new_assy_edit.setText(test_value)
    result = dialog.action_new_assy_changed()
    assert not result["valid"]
    assert dialog.form.new_assy_edit.text() == test_value.upper()
    assert result["msg"] in dialog.form.new_assy_edit.toolTip()
    assert dialog.TOOLTIPS["new_assy_edit"] in dialog.form.new_assy_edit.toolTip()
    assert dialog.form.new_assy_edit.error
    assert dialog.form.new_assy_frame.error

    test_value = ""  # invalid test: 0 characters
    test_value = "aabcdefghijklmno"  # invalid test: 16 characters
    dialog.form.new_assy_edit.setText(test_value)
    result = dialog.action_new_assy_changed()
    assert not result["valid"]
    assert dialog.form.new_assy_edit.text() == test_value.upper()
    assert result["msg"] in dialog.form.new_assy_edit.toolTip()
    assert dialog.TOOLTIPS["new_assy_edit"] in dialog.form.new_assy_edit.toolTip()
    assert dialog.form.new_assy_edit.error
    assert dialog.form.new_assy_frame.error


def test_103_05_get_itemset(qtbot, db_create):
    dbref, main, dialog = setup_edit_structure_dialog(qtbot, db_create)

    count = 0  # get expected length
    for item in item_value_set:
        if item[2] >= item_value_set[2][2] and item[2] < item_value_set[2][2] + "ZZZ":
            count += 1

    itemset = dialog.get_itemset(
        item_value_set[2][2], item_value_set[2][2] + "ZZZ", dbref
    )
    assert len(itemset) == count
    for item in itemset:
        assert (
            item.get_assembly() >= item_value_set[2][2]
            and item.get_assembly() < item_value_set[2][2] + "ZZZ"
        )


def test_103_06_change_assembly_ids(qtbot, db_create, mocker):
    dbref, main, dialog = setup_edit_structure_dialog(qtbot, db_create)

    assy_id_1 = "B"
    assy_id_2 = "Z"
    assy_id_3 = "X"
    dialog.form.old_assy_edit.setText(assy_id_1)
    dialog.form.new_assy_edit.setText(assy_id_2)

    orig_itemset = dialog.get_itemset(assy_id_1, assy_id_1 + "ZZZZ", dbref)
    item_set_len = len(orig_itemset)

    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.No
    dialog.change_assembly_ids(assy_tree_update_tree, dbref)
    new_itemset = dialog.get_itemset(assy_id_2, assy_id_2 + "ZZZZ", dbref)
    assert len(orig_itemset) == len(new_itemset)
    for i in range(0, len(new_itemset) - 1):
        new_assy = new_itemset[i].get_assembly()
        old_assy = orig_itemset[i].get_assembly()
        assert old_assy != new_assy
        if len(assy_id_1) == 1 and len(new_assy) == 1:
            assert new_assy == assy_id_2
        else:
            assert new_assy == assy_id_2 + new_assy[len(assy_id_1) :]
    assert dialog.closed

    dialog = EditStructureDialog(dbref, None, Dialog.EDIT_ELEMENT)
    dialog.form.old_assy_edit.setText(assy_id_2)
    dialog.form.new_assy_edit.setText(assy_id_3)
    orig_itemset = dialog.get_itemset(assy_id_2, assy_id_2 + "ZZZZ", dbref)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    number_changed = dialog.change_assembly_ids(assy_tree_update_tree, dbref)
    assert number_changed == len(orig_itemset)
    new_itemset = dialog.get_itemset(assy_id_3, assy_id_3 + "ZZZZ", dbref)
    assert len(orig_itemset) == len(new_itemset)
    for i in range(0, len(new_itemset) - 1):
        new_assy = new_itemset[i].get_assembly()
        old_assy = orig_itemset[i].get_assembly()
        assert old_assy != new_assy
        if len(assy_id_2) == 1 and len(new_assy) == 1:
            assert new_assy == assy_id_3
        else:
            assert new_assy == assy_id_3 + new_assy[len(assy_id_2) :]
    assert not dialog.closed

    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok
    mocker.patch.object(Item, "update")
    Item.update.return_value = False
    dialog = EditStructureDialog(dbref, None, Dialog.EDIT_ELEMENT)
    dialog.form.old_assy_edit.setText(assy_id_3)
    dialog.form.new_assy_edit.setText(assy_id_1)
    orig_itemset = dialog.get_itemset(assy_id_3, assy_id_3 + "ZZZZ", dbref)
    number_changed = dialog.change_assembly_ids(assy_tree_update_tree, dbref)
    assert number_changed == 0


def test_103_07_action_change(qtbot, db_create, mocker):
    dbref, main, dialog = setup_edit_structure_dialog(qtbot, db_create)

    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok

    # same value in both assy edits -> invalid
    dialog.form.old_assy_edit.setText("Q")
    dialog.form.old_assy_edit.editingFinished.emit()
    dialog.form.new_assy_edit.setText("Q")
    dialog.form.new_assy_edit.editingFinished.emit()
    dialog.form.change_button.click()
    assert dialog.old_assy_edit.error
    assert dialog.new_assy_edit.error

    # new assy -> invalid
    dialog.form.old_assy_edit.setText("Q")
    dialog.form.old_assy_edit.editingFinished.emit()
    dialog.form.new_assy_edit.setText("")
    dialog.form.new_assy_edit.editingFinished.emit()
    dialog.form.change_button.click()
    assert not dialog.old_assy_edit.error
    assert dialog.new_assy_edit.error

    # old assy -> invalid
    dialog.form.old_assy_edit.setText("")
    dialog.form.old_assy_edit.editingFinished.emit()
    dialog.form.new_assy_edit.setText("Q")
    dialog.form.new_assy_edit.editingFinished.emit()
    dialog.form.change_button.click()
    assert dialog.old_assy_edit.error
    assert not dialog.new_assy_edit.error

    # move "Q" to 'P', "Q doesn't exist so number of items should be 0
    dialog.form.old_assy_edit.setText("Q")
    dialog.form.old_assy_edit.editingFinished.emit()
    dialog.form.new_assy_edit.setText("p")
    dialog.form.new_assy_edit.editingFinished.emit()
    assert not dialog.old_assy_edit.error
    assert not dialog.new_assy_edit.error
    number_items_changed = dialog.action_change(assy_tree_update_tree, dbref)
    assert number_items_changed == 0

    # move 'B' to 'P', number of items in 'P' should equal number of
    # items in 'B' and 'B' should result in len 0.
    b_len = len(dialog.get_itemset("B", "B" + "ZZZZ", dbref))
    dialog.form.old_assy_edit.setText("B")
    dialog.form.old_assy_edit.editingFinished.emit()
    number_items_changed = dialog.action_change(assy_tree_update_tree, dbref)
    assert number_items_changed == b_len
    assert number_items_changed == len(dialog.get_itemset("P", "P" + "ZZZZ", dbref))
    assert len(dialog.get_itemset("B", "B" + "ZZZZ", dbref)) == 0
