"""
Test the ItemDialog class.

File:       test_102_item_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from lbk_library import Dbal, Element
from lbk_library.gui import Dialog
from PyQt6.QtWidgets import QDialog, QMainWindow, QMessageBox
from pytestqt import qtbot

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import (
    condition_value_set,
    db_close,
    db_create,
    db_open,
    item_columns,
    item_value_set,
    load_all_db_tables,
    load_db_table,
    long_string,
    part_columns,
    part_value_set,
    test_string,
)

from dialogs import BaseDialog, ItemDialog
from elements import Item, ItemSet, OrderLineSet, Part


def setup_item_dialog(qtbot, db_create):
    dbref = db_create
    load_all_db_tables(dbref)
    main = QMainWindow()
    dialog = ItemDialog(main, dbref, None, Dialog.EDIT_ELEMENT)
    qtbot.addWidget(main)
    return (dbref, main, dialog)


def test_102_01_class_type(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    assert isinstance(dialog, ItemDialog)
    assert isinstance(dialog, BaseDialog)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)


def test_102_02_set_visible_add_edit_elements(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    assert dialog.get_operation() == Dialog.EDIT_ELEMENT
    dialog.set_visible_add_edit_elements()
    assert dialog.form.record_id_combo.isEnabled()
    assert dialog.form.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id"]
    dialog.set_operation(Dialog.ADD_ELEMENT)
    dialog.set_visible_add_edit_elements()
    assert not dialog.form.record_id_combo.isEnabled()
    assert not dialog.form.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id"]
    assert (
        dialog.form.record_id_combo.toolTip()
        == "Item ID will be assigned when Item is saved"
    )


def test_102_03_fill_part_fields(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    dialog.fill_part_fields()
    assert dialog.form.part_number_combo.currentText() == ""
    assert dialog.form.source_text.text() == ""
    assert dialog.form.description_text.text() == ""
    assert dialog.form.remarks_text.text() == ""
    assert dialog.form.total_qty_text.text() == "0"
    dialog.fill_part_fields(part_value_set[0][1])
    assert dialog.form.part_number_combo.currentText() == part_value_set[0][1]
    assert dialog.form.source_text.text() == part_value_set[0][2]
    assert dialog.form.description_text.text() == part_value_set[0][3]
    assert dialog.form.remarks_text.text() == part_value_set[0][4]
    qty = 0
    for item in ItemSet(dbref, "part_number", part_value_set[0][1]):
        qty += item.get_quantity()
    assert dialog.form.total_qty_text.text() == str(qty)


def test_102_04_fill_dialog_fields(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    # no item selected, add item dialog, all selections should be blank.
    dialog = ItemDialog(main, dbref, None, Dialog.ADD_ELEMENT)
    dialog.fill_dialog_fields()
    assert dialog.form.record_id_combo.currentText() == ""
    assert dialog.form.assembly_edit.text() == ""
    assert dialog.form.condition_combo.currentText() == ""
    assert dialog.form.quantity_edit.text() == ""
    assert not dialog.form.installed_chkbox.isChecked()
    assert dialog.form.part_number_combo.currentText() == ""
    assert dialog.form.order_table.rowCount() == 0

    dialog.set_element(Item(dbref, item_value_set[0][0]))
    print("element", dialog.get_element().get_properties())
    dialog.fill_dialog_fields()
    print("condition text", dialog.form.condition_combo.currentText())
    print("condition index", dialog.form.condition_combo.currentIndex())
    print("condition num entries", dialog.form.condition_combo.count())
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[0][0])
    assert dialog.form.assembly_edit.text() == item_value_set[0][2]
    assert dialog.form.condition_combo.currentText() == item_value_set[0][4]
    assert dialog.form.quantity_edit.text() == str(item_value_set[0][3])
    assert dialog.form.installed_chkbox.isChecked() == bool(int(item_value_set[0][5]))
    assert dialog.form.part_number_combo.currentText() == item_value_set[0][1]
    assert dialog.form.remarks_edit.text() == item_value_set[0][7]
    assert dialog.form.order_table.rowCount() == 0


def test_102_05_clear_dialog(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    dialog = ItemDialog(main, dbref, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[0][0])
    dialog.clear_dialog()
    assert dialog.form.record_id_combo.currentText() == ""
    assert dialog.form.assembly_edit.text() == ""


def test_102_06_action_assembly_changed(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    test_value = item_value_set[0][2]
    dialog.form.assembly_edit.setText(test_value)
    result = dialog.action_assembly_changed()
    assert result["valid"]
    assert dialog.form.assembly_edit.text() == test_value.upper()
    assert dialog.form.assembly_edit.toolTip() == dialog.TOOLTIPS["assembly"]
    assert result["is_valid_ind"]

    test_value = ""
    dialog.form.assembly_edit.setText(test_value)
    result = dialog.action_assembly_changed()
    assert not result["valid"]
    assert dialog.form.assembly_edit.text() == test_value
    assert result["msg"] in dialog.form.assembly_edit.toolTip()
    assert dialog.TOOLTIPS["assembly"] in dialog.form.assembly_edit.toolTip()
    assert not result["is_valid_ind"]


def test_102_07_action_condition_changed(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    test_value = condition_value_set[0][1]
    dialog.form.condition_combo.setCurrentText(test_value)
    result = dialog.action_condition_changed()
    assert result["valid"]
    assert dialog.form.condition_combo.currentText() == test_value
    assert dialog.form.condition_combo.toolTip() == dialog.TOOLTIPS["condition"]
    assert result["is_valid_ind"]

    test_value = -1
    dialog.form.condition_combo.setCurrentIndex(test_value)
    result = dialog.action_condition_changed()
    assert not result["valid"]
    assert dialog.form.condition_combo.currentText() == ""
    assert dialog.TOOLTIPS["condition"] in dialog.form.condition_combo.toolTip()
    assert result["msg"] in dialog.form.condition_combo.toolTip()
    assert not result["is_valid_ind"]


def test_102_08_action_quantity_changed(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    test_value = "1"
    dialog.form.quantity_edit.setText(test_value)
    result = dialog.action_quantity_changed()
    assert result["valid"]
    assert dialog.form.quantity_edit.text() == test_value
    assert dialog.form.quantity_edit.text() == "1"
    assert dialog.form.quantity_edit.toolTip() == dialog.TOOLTIPS["quantity"]
    assert result["is_valid_ind"]

    test_value = ""
    dialog.form.quantity_edit.setText(test_value)
    result = dialog.action_quantity_changed()
    assert result["valid"]
    assert dialog.form.quantity_edit.text() == "0"
    assert dialog.form.quantity_edit.toolTip() == dialog.TOOLTIPS["quantity"]
    assert result["is_valid_ind"]

    test_value = "-1"
    dialog.form.quantity_edit.setText(test_value)
    result = dialog.action_quantity_changed()
    assert not result["valid"]
    assert dialog.form.quantity_edit.text() == test_value
    assert result["msg"] in dialog.form.quantity_edit.toolTip()
    assert dialog.TOOLTIPS["quantity"] in dialog.form.quantity_edit.toolTip()
    assert not result["is_valid_ind"]


def test_102_09_action_installed_changed(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    current_state = dialog.form.installed_chkbox.isChecked()
    dialog.form.installed_chkbox.setChecked(not current_state)
    assert not dialog.form.installed_chkbox.isChecked() == current_state

    current_state = dialog.form.installed_chkbox.isChecked()
    dialog.form.installed_chkbox.setChecked(not current_state)
    assert not dialog.form.installed_chkbox.isChecked() == current_state
    result = dialog.action_installed_changed()
    assert result["valid"]
    assert not dialog.form.installed_chkbox.isChecked() == current_state
    assert dialog.form.installed_chkbox.toolTip() == dialog.TOOLTIPS["installed"]


def test_102_10_action_box_changed(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    test_value = "1"
    dialog.form.storage_box_edit.setText(test_value)
    result = dialog.action_box_changed()
    assert result["valid"]
    assert dialog.form.storage_box_edit.text() == test_value
    assert dialog.form.storage_box_edit.toolTip() == dialog.TOOLTIPS["box"]
    assert result["is_valid_ind"]

    test_value = ""
    dialog.form.storage_box_edit.setText(test_value)
    assert dialog.form.storage_box_edit.text() == ""
    result = dialog.action_box_changed()
    assert result["valid"]
    assert dialog.form.storage_box_edit.text() == test_value
    assert dialog.form.storage_box_edit.toolTip() == dialog.TOOLTIPS["box"]
    assert result["is_valid_ind"]

    test_value = "10000"
    dialog.form.storage_box_edit.setText(test_value)
    result = dialog.action_box_changed()
    assert not result["valid"]
    assert dialog.form.storage_box_edit.text() == test_value
    assert result["msg"] in dialog.form.storage_box_edit.toolTip()
    assert dialog.TOOLTIPS["box"] in dialog.form.storage_box_edit.toolTip()
    assert not result["is_valid_ind"]


def test_102_11_action_remarks_changed(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    dialog.form.remarks_edit.setText(test_string)
    result = dialog.action_remarks_changed()
    assert result["valid"]
    assert dialog.form.remarks_edit.text() == test_string
    assert dialog.form.remarks_edit.toolTip() == dialog.TOOLTIPS["remarks"]
    assert result["is_valid_ind"]

    # text fields have a default upper limit of 255 characters set in the
    # validation class.
    dialog.form.remarks_edit.setText(long_string)
    result = dialog.action_remarks_changed()
    assert not result["valid"]
    assert dialog.form.remarks_edit.text() == long_string
    assert result["msg"] in dialog.form.remarks_edit.toolTip()
    assert dialog.TOOLTIPS["remarks"] in dialog.form.remarks_edit.toolTip()


def test_102_12_action_part_number_changed(qtbot, db_create):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    part = Part(dbref, part_value_set[1][1], "part_number")
    dialog.form.part_number_combo.setCurrentText(part_value_set[1][1])
    assert dialog.form.part_number_combo.currentText() == part.get_part_number()
    result = dialog.action_part_number_changed()
    assert result["entry"] == part.get_part_number()
    assert dialog.form.source_text.text() == part.get_source()
    assert dialog.form.description_text.text() == part.get_description()
    assert dialog.form.remarks_text.text() == part.get_remarks()
    assert dialog.form.total_qty_text.text() == str(part.get_total_quantity())
    assert (
        dialog.form.order_table.rowCount()
        == OrderLineSet(
            dbref, "part_number", part_value_set[1][1]
        ).get_number_elements()
    )
    assert result["valid"]
    assert dialog.form.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number"]
    assert result["is_valid_ind"]

    part = Part(dbref, part_value_set[0][1], "part_number")
    dialog.form.part_number_combo.setCurrentText(part_value_set[0][1])
    assert dialog.form.part_number_combo.currentText() == part.get_part_number()
    result = dialog.action_part_number_changed()
    assert result["entry"] == part.get_part_number()
    assert dialog.form.source_text.text() == part.get_source()
    assert dialog.form.description_text.text() == part.get_description()
    assert dialog.form.remarks_text.text() == part.get_remarks()
    assert dialog.form.total_qty_text.text() == str(part.get_total_quantity())
    assert (
        dialog.form.order_table.rowCount()
        == OrderLineSet(
            dbref, "part_number", part_value_set[0][1]
        ).get_number_elements()
    )
    assert result["valid"]
    assert dialog.form.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number"]
    assert result["is_valid_ind"]

    part = Part(dbref)
    dialog.form.part_number_combo.setCurrentIndex(-1)
    assert dialog.form.part_number_combo.currentText() == part.get_part_number()
    result = dialog.action_part_number_changed()
    assert result["entry"] == part.get_part_number()
    assert dialog.form.source_text.text() == part.get_source()
    assert dialog.form.description_text.text() == part.get_description()
    assert dialog.form.remarks_text.text() == part.get_remarks()
    assert dialog.form.total_qty_text.text() == str(part.get_total_quantity())
    assert dialog.form.order_table.rowCount() == 0
    assert not result["valid"]
    assert dialog.TOOLTIPS["part_number"] in dialog.form.part_number_combo.toolTip()
    assert result["msg"] in dialog.form.part_number_combo.toolTip()
    assert not result["is_valid_ind"]


def test_102_13_action_delete(qtbot, db_create, mocker):
    # Note: message box entries not checked.
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)

    dialog = ItemDialog(main, dbref, 193, Dialog.EDIT_ELEMENT)
    assert dialog.form.assembly_edit.text() == "AABD"
    itemset_size = ItemSet(dbref).get_number_elements()
    dialog.form.delete_button.click()
    assert dialog.form.assembly_edit.text() == ""
    new_itemset_size = ItemSet(dbref).get_number_elements()
    assert itemset_size - new_itemset_size == 1

    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok
    # element invalid
    itemset_size = ItemSet(dbref).get_number_elements()
    dialog = ItemDialog(main, dbref, None, Dialog.EDIT_ELEMENT)
    dialog.action_delete()
    new_itemset_size = ItemSet(dbref).get_number_elements()
    assert itemset_size == new_itemset_size


def test_102_14_action_save(qtbot, db_create, mocker):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok

    itemset_size = ItemSet(dbref).get_number_elements()
    return_value = dialog.action_save(Dialog.SAVE_DONE)
    assert return_value == 1
    new_itemset_size = ItemSet(dbref).get_number_elements()
    assert itemset_size == new_itemset_size

    dialog = ItemDialog(main, dbref, 193, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    assert save_code == 0  # item saved successfully
    itemset_size = ItemSet(dbref).get_number_elements()
    assert itemset_size == new_itemset_size
    dialog.form.record_id_combo.setCurrentIndex(-1)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    new_itemset_size = ItemSet(dbref).get_number_elements()
    assert new_itemset_size - itemset_size == 1

    dialog = ItemDialog(main, dbref, 193, Dialog.EDIT_ELEMENT)
    itemset_size = ItemSet(dbref).get_number_elements()
    assert itemset_size == new_itemset_size
    dialog.form.record_id_combo.setCurrentIndex(-1)
    save_code = dialog.action_save(Dialog.SAVE_NEW)
    new_itemset_size = ItemSet(dbref).get_number_elements()
    assert new_itemset_size - itemset_size == 1
    assert dialog.form.record_id_combo.currentText() == ""
    assert dialog.form.assembly_edit.text() == ""

    dialog = ItemDialog(main, dbref, 193, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(10)
    assert save_code == 2  # bad save command code


def test_102_15a_action_record_id_changed(qtbot, db_create, mocker):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with no changes to current item
    dialog = ItemDialog(main, dbref, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    assert dialog.form.record_id_combo.currentText() == item_value_set[0][0]
    dialog.form.record_id_combo.setCurrentText(item_value_set[1][0])
    dialog.action_record_id_changed()
    assert dialog.form.record_id_combo.currentText() == item_value_set[1][0]
    assert dialog.form.assembly_edit.text() == item_value_set[1][2]


def test_102_15b_action_record_id_changed(qtbot, db_create, mocker):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with changes to current item
    # A. Click 'Yes' button
    dialog = ItemDialog(main, dbref, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    dialog.form.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_changed()
    print(dialog.form.assembly_edit.text())
    dialog.form.record_id_combo.setCurrentText(item_value_set[2][0])
    dialog.action_record_id_changed()
    # form should have new item; spot check the asembly and condition
    assert dialog.form.record_id_combo.currentText() == item_value_set[2][0]
    assert dialog.form.assembly_edit.text() == item_value_set[2][2]
    assert dialog.form.assembly_edit.text() == item_value_set[2][2]
    assert dialog.form.condition_combo.currentText() == item_value_set[2][4]
    # check tha old item was saved with new value
    item = Item(dbref, item_value_set[0][0])
    assert item.get_assembly() == item_value_set[1][2]


def test_102_15c_action_record_id_changed(qtbot, db_create, mocker):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with changes to current item
    # C. Click 'No' button, do not save the changed item, load new item
    dialog = ItemDialog(main, dbref, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.No
    dialog.form.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_changed()
    dialog.form.record_id_combo.setCurrentText(item_value_set[2][0])
    dialog.action_record_id_changed()
    # form should have new item; spot check the asembly and condition
    assert dialog.form.record_id_combo.currentText() == item_value_set[2][0]
    assert dialog.form.assembly_edit.text() == item_value_set[2][2]
    assert dialog.form.condition_combo.currentText() == item_value_set[2][4]


def test_102_15d_action_record_id_changed(qtbot, db_create, mocker):
    dbref, main, dialog = setup_item_dialog(qtbot, db_create)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with changes to current item
    # D. Click 'Cancel' button, do not save the changed item, restore old record id
    dialog = ItemDialog(main, dbref, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Cancel
    dialog.form.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_changed()
    dialog.form.record_id_combo.setCurrentText(item_value_set[2][0])
    dialog.action_record_id_changed()
    # form should have old item number
    assert dialog.form.record_id_combo.currentText() == item_value_set[0][0]
    assert dialog.form.assembly_edit.text() == item_value_set[1][2]
