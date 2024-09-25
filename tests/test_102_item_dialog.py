"""
Test the ItemDialog class.

File:       test_102_item_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import DataFile, Element
from lbk_library.gui import Dialog, ErrorFrame
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
    long_string,
    test_string,
)
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox
from test_setup import (
    condition_value_set,
    datafile_name,
    item_value_set,
    load_all_datafile_tables,
    part_value_set,
    source_value_set,
)

from dialogs import BaseDialog, ItemDialog
from elements import (
    Condition,
    ConditionSet,
    Item,
    ItemSet,
    OrderLineSet,
    Part,
    PartSet,
    Source,
)
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


def setup_item_dialog(qtbot, filesystem):
    filename = filesystem + "/" + datafile_name
    datafile = datafile_create(filename, table_definition)
    load_all_datafile_tables(datafile)
    main = QMainWindow()
    dialog = ItemDialog(main, datafile, None, Dialog.EDIT_ELEMENT)
    qtbot.addWidget(main)
    return (datafile, main, dialog)


def test_102_01_class_type(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    assert isinstance(dialog, ItemDialog)
    assert isinstance(dialog, BaseDialog)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)
    datafile_close(datafile)


def test_102_02_set_error_frames(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    dialog.set_error_frames()
    assert isinstance(dialog.form.assembly_edit.error_frame, ErrorFrame)
    assert isinstance(dialog.form.condition_combo.error_frame, ErrorFrame)
    assert isinstance(dialog.form.part_number_combo.error_frame, ErrorFrame)
    assert isinstance(dialog.form.quantity_edit.error_frame, ErrorFrame)
    assert isinstance(dialog.form.record_id_combo.error_frame, ErrorFrame)
    assert isinstance(dialog.form.storage_box_edit.error_frame, ErrorFrame)


def test_102_03_set_visible_add_edit_elements(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    assert dialog.get_operation() == Dialog.EDIT_ELEMENT
    dialog.set_visible_add_edit_elements()
    assert dialog.form.record_id_combo.isEnabled()
    assert dialog.form.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id"]
    dialog.set_operation(Dialog.ADD_ELEMENT)
    dialog.set_visible_add_edit_elements()
    assert not dialog.form.record_id_combo.isEnabled()
    assert not dialog.form.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id"]
    assert dialog.form.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id_tbd"]


def test_102_04_fill_part_fields(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)
    dialog.set_combo_box_selections(
        dialog.form.part_number_combo,
        PartSet(datafile).build_option_list("part_number"),
        None,
    )

    dialog.fill_part_fields()
    assert dialog.form.part_number_combo.currentText() == ""
    assert dialog.form.source_text.text() == ""
    assert dialog.form.description_text.text() == ""
    assert dialog.form.remarks_text.text() == ""
    assert dialog.form.total_qty_text.text() == "0"
    dialog.fill_part_fields(part_value_set[0][1])
    assert dialog.form.part_number_combo.currentText() == part_value_set[0][1]
    assert (
        dialog.form.source_text.text() == source_value_set[part_value_set[0][2] - 1][1]
    )
    assert dialog.form.description_text.text() == part_value_set[0][3]
    assert dialog.form.remarks_text.text() == part_value_set[0][4]
    qty = 0
    for item in ItemSet(datafile, "part_number", part_value_set[0][1]):
        qty += item.get_quantity()
    assert dialog.form.total_qty_text.text() == str(qty)


def test_102_05_fill_dialog_fields(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    # no item selected, add item dialog, all selections should be blank.
    dialog = ItemDialog(main, datafile, None, Dialog.ADD_ELEMENT)
    dialog.fill_dialog_fields()
    assert dialog.form.record_id_combo.currentText() == ""
    assert dialog.form.assembly_edit.text() == ""
    assert dialog.form.condition_combo.currentText() == ""
    assert dialog.form.quantity_edit.text() == ""
    assert not dialog.form.installed_chkbox.isChecked()
    assert dialog.form.part_number_combo.currentText() == ""
    assert dialog.form.order_table.rowCount() == 0

    dialog.set_element(Item(datafile, item_value_set[0][0]))
    dialog.fill_dialog_fields()
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[0][0])
    assert dialog.form.assembly_edit.text() == item_value_set[0][2]
    assert dialog.form.condition_combo.currentText() == "New"
    assert dialog.form.quantity_edit.text() == str(item_value_set[0][3])
    assert dialog.form.installed_chkbox.isChecked() == bool(int(item_value_set[0][5]))
    assert dialog.form.part_number_combo.currentText() == item_value_set[0][1]
    assert dialog.form.remarks_edit.text() == item_value_set[0][7]
    assert dialog.form.order_table.rowCount() == 0


def test_102_06_clear_dialog(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    dialog = ItemDialog(main, datafile, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[0][0])
    dialog.clear_dialog()
    assert dialog.form.record_id_combo.currentText() == ""
    assert dialog.form.assembly_edit.text() == ""


def test_102_04_action_assembly_edit(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    test_value = item_value_set[0][2]
    dialog.form.assembly_edit.setText(test_value)
    dialog.form.assembly_edit.editingFinished.emit()
    assert not dialog.form.assembly_edit.error
    assert dialog.form.assembly_edit.text() == test_value.upper()
    assert dialog.form.assembly_edit.toolTip() == dialog.TOOLTIPS["assembly"]

    test_value = ""
    dialog.form.assembly_edit.setText(test_value)
    result = dialog.action_assembly_edit()

    assert dialog.form.assembly_edit.error
    assert not result["valid"]
    assert dialog.form.assembly_edit.text() == test_value
    assert result["msg"] in dialog.form.assembly_edit.toolTip()
    assert dialog.TOOLTIPS["assembly"] in dialog.form.assembly_edit.toolTip()
    assert dialog.form.assembly_edit.error


def test_102_05_action_condition_combo(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)
    dialog.set_combo_box_selections(
        dialog.form.condition_combo,
        ConditionSet(datafile).build_option_list("condition"),
        None,
    )

    test_value = condition_value_set[0][1]
    dialog.form.condition_combo.setCurrentText(test_value)
    dialog.form.condition_combo.activated.emit(
        dialog.form.condition_combo.currentIndex()
    )
    assert not dialog.form.condition_combo.error
    assert dialog.form.condition_combo.currentText() == test_value
    assert dialog.form.condition_combo.toolTip() == dialog.TOOLTIPS["condition"]

    test_value = -1
    dialog.form.condition_combo.setCurrentIndex(test_value)
    result = dialog.action_condition_combo()
    assert dialog.form.condition_combo.error
    assert not result["valid"]
    assert dialog.form.condition_combo.currentText() == ""
    assert dialog.TOOLTIPS["condition"] in dialog.form.condition_combo.toolTip()
    assert result["msg"] in dialog.form.condition_combo.toolTip()


def test_102_06_action_quantity_edit(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    test_value = "1"
    dialog.form.quantity_edit.setText(test_value)
    dialog.form.quantity_edit.editingFinished.emit()
    assert not dialog.form.quantity_edit.error
    assert dialog.form.quantity_edit.text() == test_value
    assert dialog.form.quantity_edit.text() == "1"
    assert dialog.form.quantity_edit.toolTip() == dialog.TOOLTIPS["quantity"]

    test_value = ""
    dialog.form.quantity_edit.setText(test_value)
    result = dialog.action_quantity_edit()
    assert not dialog.form.quantity_edit.error
    assert result["valid"]
    assert dialog.form.quantity_edit.text() == "0"
    assert dialog.form.quantity_edit.toolTip() == dialog.TOOLTIPS["quantity"]

    test_value = "-1"
    dialog.form.quantity_edit.setText(test_value)
    result = dialog.action_quantity_edit()
    assert dialog.form.quantity_edit.error
    assert not result["valid"]
    assert dialog.form.quantity_edit.text() == test_value
    assert result["msg"] in dialog.form.quantity_edit.toolTip()
    assert dialog.TOOLTIPS["quantity"] in dialog.form.quantity_edit.toolTip()


def test_102_07_action_installed_checkbox(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    current_state = dialog.form.installed_chkbox.isChecked()
    dialog.form.installed_chkbox.setChecked(not current_state)
    assert not dialog.form.installed_chkbox.isChecked() == current_state

    current_state = dialog.form.installed_chkbox.isChecked()
    dialog.form.installed_chkbox.setChecked(not current_state)
    assert not dialog.form.installed_chkbox.isChecked() == current_state
    dialog.form.installed_chkbox.stateChanged.emit(not current_state)
    assert not dialog.form.installed_chkbox.isChecked() == current_state
    assert dialog.form.installed_chkbox.toolTip() == dialog.TOOLTIPS["installed"]
    current_state = dialog.form.installed_chkbox.isChecked()
    dialog.form.installed_chkbox.setChecked(not current_state)
    assert not dialog.form.installed_chkbox.isChecked() == current_state
    result = dialog.action_installed_checkbox()
    assert result["valid"]
    assert not dialog.form.installed_chkbox.isChecked() == current_state
    assert dialog.form.installed_chkbox.toolTip() == dialog.TOOLTIPS["installed"]


def test_102_08_action_storage_box_edit(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    test_value = "1"
    dialog.form.storage_box_edit.setText(test_value)
    dialog.form.storage_box_edit.editingFinished.emit()
    assert not dialog.form.storage_box_edit.error
    assert dialog.form.storage_box_edit.text() == test_value
    assert dialog.form.storage_box_edit.toolTip() == dialog.TOOLTIPS["box"]

    test_value = ""
    dialog.form.storage_box_edit.setText(test_value)
    assert dialog.form.storage_box_edit.text() == ""
    result = dialog.action_storage_box_edit()
    assert not dialog.form.storage_box_edit.error
    assert result["valid"]
    assert dialog.form.storage_box_edit.text() == test_value
    assert dialog.form.storage_box_edit.toolTip() == dialog.TOOLTIPS["box"]

    test_value = "10000"
    dialog.form.storage_box_edit.setText(test_value)
    result = dialog.action_storage_box_edit()
    assert dialog.form.storage_box_edit.error
    assert not result["valid"]
    assert dialog.form.storage_box_edit.text() == test_value
    assert result["msg"] in dialog.form.storage_box_edit.toolTip()
    assert dialog.TOOLTIPS["box"] in dialog.form.storage_box_edit.toolTip()


def test_102_09_action_remarks_edit(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    dialog.form.remarks_edit.setText(test_string)
    dialog.form.remarks_edit.editingFinished.emit()
    assert not dialog.form.remarks_edit.error
    assert dialog.form.remarks_edit.text() == test_string
    assert dialog.form.remarks_edit.toolTip() == dialog.TOOLTIPS["remarks"]

    # text fields have a default upper limit of 255 characters set in the
    # validation class.
    dialog.form.remarks_edit.setText(long_string)
    result = dialog.action_remarks_edit()
    assert dialog.form.remarks_edit.error
    assert not result["valid"]
    assert dialog.form.remarks_edit.text() == long_string
    assert result["msg"] in dialog.form.remarks_edit.toolTip()
    assert dialog.TOOLTIPS["remarks"] in dialog.form.remarks_edit.toolTip()


def test_102_11_action_part_number_combo(qtbot, filesystem):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)
    dialog.set_combo_box_selections(
        dialog.form.part_number_combo,
        PartSet(datafile).build_option_list("part_number"),
        None,
    )

    part = Part(datafile, part_value_set[1][1], "part_number")
    dialog.form.part_number_combo.setCurrentText(part_value_set[1][1])
    assert dialog.form.part_number_combo.currentText() == part.get_part_number()
    dialog.form.part_number_combo.activated.emit(
        dialog.form.part_number_combo.currentIndex()
    )
    assert (
        dialog.form.source_text.text()
        == Source(datafile, part.get_source()).get_source()
    )
    assert dialog.form.description_text.text() == part.get_description()
    assert dialog.form.remarks_text.text() == part.get_remarks()
    assert dialog.form.total_qty_text.text() == str(part.get_total_quantity())
    assert (
        dialog.form.order_table.rowCount()
        == OrderLineSet(
            datafile, "part_number", part_value_set[1][1]
        ).get_number_elements()
    )
    assert not dialog.form.part_number_combo.error
    assert dialog.form.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number"]

    part = Part(datafile, part_value_set[0][1], "part_number")
    dialog.form.part_number_combo.setCurrentText(part_value_set[0][1])
    assert dialog.form.part_number_combo.currentText() == part.get_part_number()
    result = dialog.action_part_number_combo()
    assert result["entry"] == part.get_part_number()
    assert (
        dialog.form.source_text.text()
        == Source(datafile, part.get_source()).get_source()
    )
    assert dialog.form.description_text.text() == part.get_description()
    assert dialog.form.remarks_text.text() == part.get_remarks()
    assert dialog.form.total_qty_text.text() == str(part.get_total_quantity())
    assert (
        dialog.form.order_table.rowCount()
        == OrderLineSet(
            datafile, "part_number", part_value_set[0][1]
        ).get_number_elements()
    )
    assert not dialog.form.part_number_combo.error
    assert result["valid"]
    assert dialog.form.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number"]

    part = Part(datafile)
    dialog.form.part_number_combo.setCurrentIndex(-1)
    assert dialog.form.part_number_combo.currentText() == part.get_part_number()
    result = dialog.action_part_number_combo()
    assert result["entry"] == part.get_part_number()
    assert (
        dialog.form.source_text.text()
        == Source(datafile, part.get_source()).get_source()
    )
    assert dialog.form.description_text.text() == part.get_description()
    assert dialog.form.remarks_text.text() == part.get_remarks()
    assert dialog.form.total_qty_text.text() == str(part.get_total_quantity())
    assert dialog.form.order_table.rowCount() == 0
    assert dialog.form.part_number_combo.error
    assert not result["valid"]
    assert dialog.TOOLTIPS["part_number"] in dialog.form.part_number_combo.toolTip()
    assert result["msg"] in dialog.form.part_number_combo.toolTip()


def test_102_14_action_delete(qtbot, filesystem, mocker):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)

    # Note: message box entries not checked.

    # delete an item
    dialog = ItemDialog(main, datafile, 193, Dialog.EDIT_ELEMENT)
    assert dialog.form.assembly_edit.text() == "AABD"
    itemset_size = ItemSet(datafile).get_number_elements()
    dialog.form.delete_button.click()
    assert dialog.form.assembly_edit.text() == ""
    new_itemset_size = ItemSet(datafile).get_number_elements()
    assert itemset_size - new_itemset_size == 1

    # try to delete a invalid item
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok
    itemset_size = ItemSet(datafile).get_number_elements()
    dialog = ItemDialog(main, datafile, None, Dialog.EDIT_ELEMENT)
    dialog.action_delete()
    new_itemset_size = ItemSet(datafile).get_number_elements()
    assert itemset_size == new_itemset_size

    # delete action fails
    mocker.patch.object(Item, "delete")
    Item.delete.return_value = False
    dialog = ItemDialog(main, datafile, 184, Dialog.EDIT_ELEMENT)
    itemset_size = ItemSet(datafile).get_number_elements()
    dialog.action_delete()
    new_itemset_size = ItemSet(datafile).get_number_elements()
    assert itemset_size == new_itemset_size


def test_102_15_action_save(qtbot, filesystem, mocker):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok

    itemset_size = ItemSet(datafile).get_number_elements()
    return_value = dialog.action_save(Dialog.SAVE_DONE)
    assert return_value == 1
    new_itemset_size = ItemSet(datafile).get_number_elements()
    assert itemset_size == new_itemset_size

    dialog = ItemDialog(main, datafile, 193, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    assert save_code == 0  # item saved successfully
    itemset_size = ItemSet(datafile).get_number_elements()
    assert itemset_size == new_itemset_size
    dialog.form.record_id_combo.setCurrentIndex(-1)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    new_itemset_size = ItemSet(datafile).get_number_elements()
    assert new_itemset_size - itemset_size == 1

    dialog = ItemDialog(main, datafile, 193, Dialog.EDIT_ELEMENT)
    itemset_size = ItemSet(datafile).get_number_elements()
    assert itemset_size == new_itemset_size
    dialog.form.record_id_combo.setCurrentIndex(-1)
    save_code = dialog.action_save(Dialog.SAVE_NEW)
    new_itemset_size = ItemSet(datafile).get_number_elements()
    assert new_itemset_size - itemset_size == 1
    assert dialog.form.record_id_combo.currentText() == ""
    assert dialog.form.assembly_edit.text() == ""

    dialog = ItemDialog(main, datafile, 193, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(10)
    assert save_code == 2  # bad save command code

    # item update failed
    mocker.patch.object(Item, "update")
    Item.update.return_value = False
    dialog = ItemDialog(main, datafile, 193, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    assert save_code == 3


def test_102_16a_action_record_id_changed(qtbot, filesystem, mocker):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")

    # A. record_id changed with no changes to current item
    dialog = ItemDialog(main, datafile, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[0][0])
    dialog.form.record_id_combo.setCurrentText(str(item_value_set[1][0]))
    dialog.action_record_id_changed()
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[1][0])
    assert dialog.form.assembly_edit.text() == item_value_set[1][2]

    # record_id changed with changes to current item
    # B-1. Click 'Yes' button
    dialog = ItemDialog(main, datafile, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    dialog.form.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_edit()
    dialog.form.record_id_combo.setCurrentText(str(item_value_set[2][0]))
    dialog.action_record_id_changed()
    # form should have new item; spot check the asembly and condition
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[2][0])
    assert dialog.form.assembly_edit.text() == item_value_set[2][2]
    assert dialog.form.assembly_edit.text() == item_value_set[2][2]
    assert (
        dialog.form.condition_combo.currentText()
        == Condition(datafile, item_value_set[2][4]).get_condition()
    )
    # check that old item was saved with new value
    item = Item(datafile, item_value_set[0][0])
    assert item.get_assembly() == item_value_set[1][2]


def test_102_16c_action_record_id_changed(qtbot, filesystem, mocker):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with changes to current item
    # C. Click 'No' button, do not save the changed item, load new item
    dialog = ItemDialog(main, datafile, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.No
    dialog.form.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_edit()
    dialog.form.record_id_combo.setCurrentText(str(item_value_set[2][0]))
    dialog.action_record_id_changed()
    # form should have new item; spot check the asembly and condition
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[2][0])
    assert dialog.form.assembly_edit.text() == item_value_set[2][2]
    assert (
        dialog.form.condition_combo.currentText()
        == Condition(datafile, item_value_set[2][4]).get_condition()
    )


def test_102_16d_action_record_id_changed(qtbot, filesystem, mocker):
    datafile, main, dialog = setup_item_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with changes to current item
    # D. Click 'Cancel' button, do not save the changed item, restore old record id
    dialog = ItemDialog(main, datafile, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Cancel
    dialog.form.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_edit()
    dialog.form.record_id_combo.setCurrentText(str(item_value_set[2][0]))
    dialog.action_record_id_changed()
    # form should have old item number
    assert dialog.form.record_id_combo.currentText() == str(item_value_set[0][0])
    assert dialog.form.assembly_edit.text() == str(item_value_set[1][2])
