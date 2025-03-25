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

from lbk_library.gui import Dialog, ErrorFrame
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
    long_string,
    test_string,
)
from PySide6.QtWidgets import QMainWindow, QMessageBox
from test_setup import (
    condition_value_set,
    datafile_name,
    item_value_set,
    load_all_datafile_tables,
    part_value_set,
    source_value_set,
)

from dialogs import ItemDialog
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
from forms import Ui_ItemDialog
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


def setup_item_dialog(qtbot, tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + datafile_name
    parts_file = datafile_create(filename, table_definition)
    load_all_datafile_tables(parts_file)
    main = QMainWindow()
    dialog = ItemDialog(main, parts_file, None, Dialog.EDIT_ELEMENT)
    qtbot.addWidget(main)
    return (parts_file, main, dialog)


def test_102_01_class_type(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    assert isinstance(dialog, ItemDialog)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, Ui_ItemDialog)
    datafile_close(parts_file)


def test_102_02_set_error_frames(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    dialog.set_error_frames()
    assert isinstance(dialog.assembly_edit.error_frame, ErrorFrame)
    assert isinstance(dialog.condition_combo.error_frame, ErrorFrame)
    assert isinstance(dialog.part_number_combo.error_frame, ErrorFrame)
    assert isinstance(dialog.quantity_edit.error_frame, ErrorFrame)
    assert isinstance(dialog.record_id_combo.error_frame, ErrorFrame)
    assert isinstance(dialog.storage_box_edit.error_frame, ErrorFrame)
    datafile_close(parts_file)


def test_102_03_set_visible_add_edit_elements(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    assert dialog.get_operation() == Dialog.EDIT_ELEMENT
    dialog.set_visible_add_edit_elements()
    assert dialog.record_id_combo.isEnabled()
    assert dialog.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id"]
    dialog.set_operation(Dialog.ADD_ELEMENT)
    dialog.set_visible_add_edit_elements()
    assert not dialog.record_id_combo.isEnabled()
    assert not dialog.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id"]
    assert dialog.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id_tbd"]
    datafile_close(parts_file)


def test_102_04_fill_part_fields(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)
    dialog.set_combo_box_selections(
        dialog.part_number_combo,
        PartSet(parts_file).build_option_list("part_number"),
        None,
    )

    dialog.fill_part_fields()
    assert dialog.part_number_combo.currentText() == ""
    assert dialog.source_text.text() == ""
    assert dialog.description_text.text() == ""
    assert dialog.remarks_text.text() == ""
    assert dialog.total_qty_text.text() == "0"
    dialog.fill_part_fields(part_value_set[0][1])
    assert dialog.part_number_combo.currentText() == part_value_set[0][1]
    assert dialog.source_text.text() == source_value_set[part_value_set[0][2] - 1][1]
    assert dialog.description_text.text() == part_value_set[0][3]
    assert dialog.remarks_text.text() == part_value_set[0][4]
    qty = 0
    for item in ItemSet(parts_file, "part_number", part_value_set[0][1]):
        qty += item.get_quantity()
    assert dialog.total_qty_text.text() == str(qty)
    datafile_close(parts_file)


def test_102_05_fill_dialog_fields(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    # no item selected, add item dialog, all selections should be blank.
    dialog = ItemDialog(main, parts_file, None, Dialog.ADD_ELEMENT)
    dialog.fill_dialog_fields()
    assert dialog.record_id_combo.currentText() == ""
    assert dialog.assembly_edit.text() == ""
    assert dialog.condition_combo.currentText() == ""
    assert dialog.quantity_edit.text() == ""
    assert not dialog.installed_chkbox.isChecked()
    assert dialog.part_number_combo.currentText() == ""
    assert dialog.order_table.rowCount() == 0

    dialog.set_element(Item(parts_file, item_value_set[0][0]))
    dialog.fill_dialog_fields()
    assert dialog.record_id_combo.currentText() == str(item_value_set[0][0])
    assert dialog.assembly_edit.text() == item_value_set[0][2]
    assert dialog.condition_combo.currentText() == "New"
    assert dialog.quantity_edit.text() == str(item_value_set[0][3])
    assert dialog.installed_chkbox.isChecked() == bool(int(item_value_set[0][5]))
    assert dialog.part_number_combo.currentText() == item_value_set[0][1]
    assert dialog.remarks_edit.text() == item_value_set[0][7]
    assert dialog.order_table.rowCount() == 0
    datafile_close(parts_file)


def test_102_06_clear_dialog(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    dialog = ItemDialog(main, parts_file, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    assert dialog.record_id_combo.currentText() == str(item_value_set[0][0])
    dialog.clear_dialog()
    assert dialog.record_id_combo.currentText() == ""
    assert dialog.assembly_edit.text() == ""
    datafile_close(parts_file)


def test_102_07_action_assembly_edit(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    test_value = item_value_set[0][2]
    dialog.assembly_edit.setText(test_value)
    dialog.assembly_edit.editingFinished.emit()
    assert not dialog.assembly_edit.error
    assert dialog.assembly_edit.text() == test_value.upper()
    assert dialog.assembly_edit.toolTip() == dialog.TOOLTIPS["assembly"]

    test_value = ""
    dialog.assembly_edit.setText(test_value)
    result = dialog.action_assembly_edit()

    assert dialog.assembly_edit.error
    assert not result["valid"]
    assert dialog.assembly_edit.text() == test_value
    assert result["msg"] in dialog.assembly_edit.toolTip()
    assert dialog.TOOLTIPS["assembly"] in dialog.assembly_edit.toolTip()
    assert dialog.assembly_edit.error
    datafile_close(parts_file)


def test_102_08_action_condition_combo(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)
    dialog.set_combo_box_selections(
        dialog.condition_combo,
        ConditionSet(parts_file).build_option_list("condition"),
        None,
    )

    test_value = condition_value_set[0][1]
    dialog.condition_combo.setCurrentText(test_value)
    dialog.condition_combo.activated.emit(dialog.condition_combo.currentIndex())
    assert not dialog.condition_combo.error
    assert dialog.condition_combo.currentText() == test_value
    assert dialog.condition_combo.toolTip() == dialog.TOOLTIPS["condition"]

    test_value = -1
    dialog.condition_combo.setCurrentIndex(test_value)
    result = dialog.action_condition_combo()
    assert dialog.condition_combo.error
    assert not result["valid"]
    assert dialog.condition_combo.currentText() == ""
    assert dialog.TOOLTIPS["condition"] in dialog.condition_combo.toolTip()
    assert result["msg"] in dialog.condition_combo.toolTip()
    datafile_close(parts_file)


def test_102_09_action_quantity_edit(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    test_value = "1"
    dialog.quantity_edit.setText(test_value)
    dialog.quantity_edit.editingFinished.emit()
    assert not dialog.quantity_edit.error
    assert dialog.quantity_edit.text() == test_value
    assert dialog.quantity_edit.text() == "1"
    assert dialog.quantity_edit.toolTip() == dialog.TOOLTIPS["quantity"]

    test_value = ""
    dialog.quantity_edit.setText(test_value)
    result = dialog.action_quantity_edit()
    assert not dialog.quantity_edit.error
    assert result["valid"]
    assert dialog.quantity_edit.text() == "0"
    assert dialog.quantity_edit.toolTip() == dialog.TOOLTIPS["quantity"]

    test_value = "-1"
    dialog.quantity_edit.setText(test_value)
    result = dialog.action_quantity_edit()
    assert dialog.quantity_edit.error
    assert not result["valid"]
    assert dialog.quantity_edit.text() == test_value
    assert result["msg"] in dialog.quantity_edit.toolTip()
    assert dialog.TOOLTIPS["quantity"] in dialog.quantity_edit.toolTip()
    datafile_close(parts_file)


def test_102_10_action_installed_checkbox(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    current_state = dialog.installed_chkbox.isChecked()
    dialog.installed_chkbox.setChecked(not current_state)
    assert not dialog.installed_chkbox.isChecked() == current_state

    current_state = dialog.installed_chkbox.isChecked()
    dialog.installed_chkbox.setChecked(not current_state)
    assert not dialog.installed_chkbox.isChecked() == current_state
    dialog.installed_chkbox.stateChanged.emit(not current_state)
    assert not dialog.installed_chkbox.isChecked() == current_state
    assert dialog.installed_chkbox.toolTip() == dialog.TOOLTIPS["installed"]
    current_state = dialog.installed_chkbox.isChecked()
    dialog.installed_chkbox.setChecked(not current_state)
    assert not dialog.installed_chkbox.isChecked() == current_state
    result = dialog.action_installed_checkbox()
    assert result["valid"]
    assert not dialog.installed_chkbox.isChecked() == current_state
    assert dialog.installed_chkbox.toolTip() == dialog.TOOLTIPS["installed"]
    datafile_close(parts_file)


def test_102_11_action_storage_box_edit(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    test_value = "1"
    dialog.storage_box_edit.setText(test_value)
    dialog.storage_box_edit.editingFinished.emit()
    assert not dialog.storage_box_edit.error
    assert dialog.storage_box_edit.text() == test_value
    assert dialog.storage_box_edit.toolTip() == dialog.TOOLTIPS["box"]

    test_value = ""
    dialog.storage_box_edit.setText(test_value)
    assert dialog.storage_box_edit.text() == ""
    result = dialog.action_storage_box_edit()
    assert not dialog.storage_box_edit.error
    assert result["valid"]
    assert dialog.storage_box_edit.text() == test_value
    assert dialog.storage_box_edit.toolTip() == dialog.TOOLTIPS["box"]

    test_value = "10000"
    dialog.storage_box_edit.setText(test_value)
    result = dialog.action_storage_box_edit()
    assert dialog.storage_box_edit.error
    assert not result["valid"]
    assert dialog.storage_box_edit.text() == test_value
    assert result["msg"] in dialog.storage_box_edit.toolTip()
    assert dialog.TOOLTIPS["box"] in dialog.storage_box_edit.toolTip()
    datafile_close(parts_file)


def test_102_12_action_remarks_edit(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    dialog.remarks_edit.setText(test_string)
    dialog.remarks_edit.editingFinished.emit()
    assert not dialog.remarks_edit.error
    assert dialog.remarks_edit.text() == test_string
    assert dialog.remarks_edit.toolTip() == dialog.TOOLTIPS["remarks"]

    # text fields have a default upper limit of 255 characters set in the
    # validation class.
    dialog.remarks_edit.setText(long_string)
    result = dialog.action_remarks_edit()
    assert dialog.remarks_edit.error
    assert not result["valid"]
    assert dialog.remarks_edit.text() == long_string
    assert result["msg"] in dialog.remarks_edit.toolTip()
    assert dialog.TOOLTIPS["remarks"] in dialog.remarks_edit.toolTip()
    datafile_close(parts_file)


def test_102_13_action_part_number_combo(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)
    dialog.set_combo_box_selections(
        dialog.part_number_combo,
        PartSet(parts_file).build_option_list("part_number"),
        None,
    )

    part = Part(parts_file, part_value_set[1][1], "part_number")
    dialog.part_number_combo.setCurrentText(part_value_set[1][1])
    assert dialog.part_number_combo.currentText() == part.get_part_number()
    dialog.part_number_combo.activated.emit(dialog.part_number_combo.currentIndex())
    assert (
        dialog.source_text.text() == Source(parts_file, part.get_source()).get_source()
    )
    assert dialog.description_text.text() == part.get_description()
    assert dialog.remarks_text.text() == part.get_remarks()
    assert dialog.total_qty_text.text() == str(part.get_total_quantity())
    assert (
        dialog.order_table.rowCount()
        == OrderLineSet(
            parts_file, "part_number", part_value_set[1][1]
        ).get_number_elements()
    )
    assert not dialog.part_number_combo.error
    assert dialog.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number"]

    part = Part(parts_file, part_value_set[0][1], "part_number")
    dialog.part_number_combo.setCurrentText(part_value_set[0][1])
    assert dialog.part_number_combo.currentText() == part.get_part_number()
    result = dialog.action_part_number_combo()
    assert result["entry"] == part.get_part_number()
    assert (
        dialog.source_text.text() == Source(parts_file, part.get_source()).get_source()
    )
    assert dialog.description_text.text() == part.get_description()
    assert dialog.remarks_text.text() == part.get_remarks()
    assert dialog.total_qty_text.text() == str(part.get_total_quantity())
    assert (
        dialog.order_table.rowCount()
        == OrderLineSet(
            parts_file, "part_number", part_value_set[0][1]
        ).get_number_elements()
    )
    assert not dialog.part_number_combo.error
    assert result["valid"]
    assert dialog.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number"]

    part = Part(parts_file)
    dialog.part_number_combo.setCurrentIndex(-1)
    assert dialog.part_number_combo.currentText() == part.get_part_number()
    result = dialog.action_part_number_combo()
    assert result["entry"] == part.get_part_number()
    assert (
        dialog.source_text.text() == Source(parts_file, part.get_source()).get_source()
    )
    assert dialog.description_text.text() == part.get_description()
    assert dialog.remarks_text.text() == part.get_remarks()
    assert dialog.total_qty_text.text() == str(part.get_total_quantity())
    assert dialog.order_table.rowCount() == 0
    assert dialog.part_number_combo.error
    assert not result["valid"]
    assert dialog.TOOLTIPS["part_number"] in dialog.part_number_combo.toolTip()
    assert result["msg"] in dialog.part_number_combo.toolTip()
    datafile_close(parts_file)


def test_102_14_action_delete(qtbot, tmp_path, mocker):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    # Note: message box entries not checked.

    # delete an item
    dialog = ItemDialog(main, parts_file, 193, Dialog.EDIT_ELEMENT)
    assert dialog.assembly_edit.text() == "AABD"
    itemset_size = ItemSet(parts_file).get_number_elements()
    dialog.delete_button.click()
    assert dialog.assembly_edit.text() == ""
    new_itemset_size = ItemSet(parts_file).get_number_elements()
    assert itemset_size - new_itemset_size == 1

    # try to delete a invalid item
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok
    itemset_size = ItemSet(parts_file).get_number_elements()
    dialog = ItemDialog(main, parts_file, None, Dialog.EDIT_ELEMENT)
    dialog.action_delete()
    new_itemset_size = ItemSet(parts_file).get_number_elements()
    assert itemset_size == new_itemset_size

    # delete action fails
    mocker.patch.object(Item, "delete")
    Item.delete.return_value = False
    dialog = ItemDialog(main, parts_file, 184, Dialog.EDIT_ELEMENT)
    itemset_size = ItemSet(parts_file).get_number_elements()
    dialog.action_delete()
    new_itemset_size = ItemSet(parts_file).get_number_elements()
    assert itemset_size == new_itemset_size
    datafile_close(parts_file)


def test_102_15_action_save(qtbot, tmp_path, mocker):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok

    itemset_size = ItemSet(parts_file).get_number_elements()
    return_value = dialog.action_save(Dialog.SAVE_DONE)
    assert return_value == 1
    new_itemset_size = ItemSet(parts_file).get_number_elements()
    assert itemset_size == new_itemset_size

    dialog = ItemDialog(main, parts_file, 193, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    assert save_code == 0  # item saved successfully
    itemset_size = ItemSet(parts_file).get_number_elements()
    assert itemset_size == new_itemset_size
    dialog.record_id_combo.setCurrentIndex(-1)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    new_itemset_size = ItemSet(parts_file).get_number_elements()
    assert new_itemset_size - itemset_size == 1

    dialog = ItemDialog(main, parts_file, 193, Dialog.EDIT_ELEMENT)
    itemset_size = ItemSet(parts_file).get_number_elements()
    assert itemset_size == new_itemset_size
    dialog.record_id_combo.setCurrentIndex(-1)
    save_code = dialog.action_save(Dialog.SAVE_NEW)
    new_itemset_size = ItemSet(parts_file).get_number_elements()
    assert new_itemset_size - itemset_size == 1
    assert dialog.record_id_combo.currentText() == ""
    assert dialog.assembly_edit.text() == ""

    dialog = ItemDialog(main, parts_file, 193, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(10)
    assert save_code == 2  # bad save command code

    # item update failed
    mocker.patch.object(Item, "update")
    Item.update.return_value = False
    dialog = ItemDialog(main, parts_file, 193, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    assert save_code == 3
    datafile_close(parts_file)


def test_102_16_action_record_id_changed(qtbot, tmp_path, mocker):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with no changes to current item
    dialog = ItemDialog(main, parts_file, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    assert dialog.record_id_combo.currentText() == str(item_value_set[0][0])
    dialog.record_id_combo.setCurrentText(str(item_value_set[1][0]))
    dialog.action_record_id_changed()
    assert dialog.record_id_combo.currentText() == str(item_value_set[1][0])
    assert dialog.assembly_edit.text() == item_value_set[1][2]

    # record_id changed with changes to current item
    # Click 'Yes' button
    dialog = ItemDialog(main, parts_file, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    dialog.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_edit()
    dialog.record_id_combo.setCurrentText(str(item_value_set[2][0]))
    dialog.action_record_id_changed()
    # form should have new item; spot check the asembly and condition
    assert dialog.record_id_combo.currentText() == str(item_value_set[2][0])
    assert dialog.assembly_edit.text() == item_value_set[2][2]
    assert dialog.assembly_edit.text() == item_value_set[2][2]
    assert (
        dialog.condition_combo.currentText()
        == Condition(parts_file, item_value_set[2][4]).get_condition()
    )
    # check that old item was saved with new value
    item = Item(parts_file, item_value_set[0][0])
    assert item.get_assembly() == item_value_set[1][2]
    datafile_close(parts_file)


def test_102_17_action_record_id_changed(qtbot, tmp_path, mocker):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with changes to current item
    # Click 'No' button, do not save the changed item, load new item
    dialog = ItemDialog(main, parts_file, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.No
    dialog.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_edit()
    dialog.record_id_combo.setCurrentText(str(item_value_set[2][0]))
    dialog.action_record_id_changed()
    # form should have new item; spot check the asembly and condition
    assert dialog.record_id_combo.currentText() == str(item_value_set[2][0])
    assert dialog.assembly_edit.text() == item_value_set[2][2]
    assert (
        dialog.condition_combo.currentText()
        == Condition(parts_file, item_value_set[2][4]).get_condition()
    )
    datafile_close(parts_file)


def test_102_18_action_record_id_changed(qtbot, tmp_path, mocker):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)
    mocker.patch.object(Dialog, "message_box_exec")

    # record_id changed with changes to current item
    # D. Click 'Cancel' button, do not save the changed item, restore old record id
    dialog = ItemDialog(main, parts_file, item_value_set[0][0], Dialog.EDIT_ELEMENT)
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Cancel
    dialog.assembly_edit.setText(item_value_set[1][2])
    dialog.action_assembly_edit()
    dialog.record_id_combo.setCurrentText(str(item_value_set[2][0]))
    dialog.action_record_id_changed()
    # form should have old item number
    assert dialog.record_id_combo.currentText() == str(item_value_set[0][0])
    assert dialog.assembly_edit.text() == str(item_value_set[1][2])
    datafile_close(parts_file)


def test_102_19_set_tooltips(qtbot, tmp_path):
    parts_file, main, dialog = setup_item_dialog(qtbot, tmp_path)

    #    assert dialog.order_number_combo.toolTip() == dialog.TOOLTIPS["order_number_combo"]
    assert dialog.assembly_edit.toolTip() == dialog.TOOLTIPS["assembly"]
    assert dialog.storage_box_edit.toolTip() == dialog.TOOLTIPS["box"]
    assert dialog.cancel_button.toolTip() == dialog.TOOLTIPS["cancel"]
    assert dialog.condition_combo.toolTip() == dialog.TOOLTIPS["condition"]
    assert dialog.delete_button.toolTip() == dialog.TOOLTIPS["delete"]
    assert dialog.installed_chkbox.toolTip() == dialog.TOOLTIPS["installed"]
    assert dialog.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number"]
    assert dialog.quantity_edit.toolTip() == dialog.TOOLTIPS["quantity"]
    assert dialog.record_id_combo.toolTip() == dialog.TOOLTIPS["record_id"]
    assert dialog.remarks_edit.toolTip() == dialog.TOOLTIPS["remarks"]
    assert dialog.save_new_button.toolTip() == dialog.TOOLTIPS["save_new"]
    assert dialog.save_done_button.toolTip() == dialog.TOOLTIPS["save_done"]

    datafile_close(parts_file)
