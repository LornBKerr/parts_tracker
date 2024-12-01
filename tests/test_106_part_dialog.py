"""
Test the PartDialog class.

File:       test_103_part_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
Version :   1.0.0
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
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from test_setup import (
    datafile_name,
    load_all_datafile_tables,
    part_value_set,
    source_value_set,
)

from dialogs import BaseDialog, PartDialog
from elements import ItemSet, OrderLineSet, Part, PartSet, Source, SourceSet
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


def setup_part_dialog(qtbot, filesystem):
    filename = filesystem + "/" + datafile_name
    parts_file = datafile_create(filename, table_definition)
    load_all_datafile_tables(parts_file)
    main = QMainWindow()
    dialog = PartDialog(main, parts_file, None, Dialog.EDIT_ELEMENT)
    qtbot.addWidget(main)
    return (parts_file, main, dialog)


def test_106_01_constructor(qtbot, filesystem):
    """
    Initialize the dialog.

    Item Dialog extends Base Dialog. The dialog's element should be
    a Part
    """
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    assert isinstance(dialog, PartDialog)
    assert isinstance(dialog, BaseDialog)
    assert isinstance(dialog.get_element(), Part)
    datafile_close(parts_file)


def test_106_02_set_error_frames(qtbot, filesystem):
    """Each LineEdit and ComboBox must have an associated ErrorFrame."""
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    dialog.set_error_frames()
    assert isinstance(dialog.form.part_number_combo.error_frame, ErrorFrame)
    assert isinstance(dialog.form.part_number_edit.error_frame, ErrorFrame)
    assert isinstance(dialog.form.source_combo.error_frame, ErrorFrame)
    assert isinstance(dialog.form.description_edit.error_frame, ErrorFrame)
    assert isinstance(dialog.form.remarks_edit.error_frame, ErrorFrame)
    datafile_close(parts_file)


def test_106_03_set_visible_add_edit_elements(qtbot, filesystem):
    """
    Ensure correct input widgets are displayed.

    When mode is 'Edit', the record id combo box should be enabeld and
    hae the 'record_id' tooltip. Whe in 'Add' mode, the combo box should
    be disabled and the tooltip should be set to 'roecord_id_tbd'.
    """
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    assert dialog.get_operation() == Dialog.EDIT_ELEMENT
    dialog.set_visible_add_edit_elements()
    assert dialog.form.part_number_combo.isEnabled()
    assert (
        dialog.form.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number_combo"]
    )
    assert not dialog.form.part_number_edit.isEnabled()

    dialog.set_operation(Dialog.ADD_ELEMENT)
    dialog.set_visible_add_edit_elements()
    assert dialog.form.part_number_edit.isEnabled()
    assert not dialog.form.part_number_combo.isEnabled()
    datafile_close(parts_file)


def test_106_04_fill_item_table(qtbot, filesystem):
    """
    The item table should reflect the current part number.

    The fields will be blank if no part number is selected.
    """
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    dialog.fill_item_table("")
    assert dialog.form.item_table.rowCount() == 0

    part_number = part_value_set[2][1]
    itemset = ItemSet(parts_file, "part_number", part_number, "assembly")
    dialog.fill_item_table(part_number)
    assert dialog.form.item_table.rowCount() == itemset.get_number_elements()
    items = itemset.get_property_set()
    print("test", items)
    row = 0
    for item in items:
        print("test", item.get_properties())
        assert dialog.form.item_table.item(row, 0).text() == item.get_assembly()
        assert dialog.form.item_table.item(row, 1).text() == str(item.get_record_id())
        assert dialog.form.item_table.item(row, 2).text() == str(item.get_quantity())
        if item.get_installed():
            assert dialog.form.item_table.item(row, 3).text() == "Yes"
        else:
            assert dialog.form.item_table.item(row, 3).text() == "No"
        row += 1
    datafile_close(parts_file)


def test_106_05_fill_dialog_fields(qtbot, filesystem):
    """All dialog fields should be filled correctly."""
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    # no item selected, add item dialog, all selections should be blank.
    dialog = PartDialog(main, parts_file, None, Dialog.ADD_ELEMENT)
    dialog.fill_dialog_fields()
    assert dialog.form.part_number_combo.count() == len(part_value_set)
    assert dialog.form.part_number_edit.text() == ""
    assert dialog.form.part_number_combo.currentText() == ""
    assert dialog.form.record_id_edit.text() == "0"
    assert dialog.form.source_combo.currentText() == ""
    assert dialog.form.description_edit.text() == ""
    assert dialog.form.remarks_edit.text() == ""
    assert dialog.form.order_table.rowCount() == 0
    assert dialog.form.item_table.rowCount() == 0

    dialog = PartDialog(main, parts_file, part_value_set[0][0], Dialog.ADD_ELEMENT)
    dialog.fill_dialog_fields()
    assert dialog.form.part_number_edit.text() == part_value_set[0][1]
    assert dialog.form.part_number_combo.currentText() == part_value_set[0][1]
    assert dialog.form.record_id_edit.text() == str(part_value_set[0][0])
    assert (
        dialog.form.source_combo.currentText()
        == Source(parts_file, part_value_set[0][2]).get_source()
    )
    assert dialog.form.description_edit.text() == part_value_set[0][3]
    assert dialog.form.remarks_edit.text() == part_value_set[0][4]
    assert dialog.form.order_table.rowCount() == 2
    assert dialog.form.item_table.rowCount() == 1

    dialog = PartDialog(main, parts_file, part_value_set[1][0], Dialog.ADD_ELEMENT)
    dialog.fill_dialog_fields()
    assert dialog.form.part_number_edit.text() == part_value_set[1][1]
    assert dialog.form.part_number_combo.currentText() == part_value_set[1][1]
    assert dialog.form.record_id_edit.text() == str(part_value_set[1][0])
    assert (
        dialog.form.source_combo.currentText()
        == Source(parts_file, part_value_set[1][2]).get_source()
    )
    assert dialog.form.description_edit.text() == part_value_set[1][3]
    assert dialog.form.remarks_edit.text() == part_value_set[1][4]
    assert dialog.form.order_table.rowCount() == 1
    assert dialog.form.item_table.rowCount() == 1
    datafile_close(parts_file)


def test_106_04_action_source_changed(qtbot, filesystem):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)
    dialog.set_combo_box_selections(
        dialog.form.source_combo,
        SourceSet(parts_file).build_option_list("source"),
        None,
    )

    test_value = source_value_set[0][1]
    dialog.form.source_combo.setCurrentText(test_value)
    dialog.form.source_combo.activated.emit(dialog.form.source_combo.currentIndex())
    print(dialog.form.source_combo.currentIndex())
    assert not dialog.form.source_combo.error
    assert dialog.form.source_combo.currentText() == test_value
    assert dialog.form.source_combo.toolTip() == dialog.TOOLTIPS["source_combo"]

    test_value = -1
    dialog.form.source_combo.setCurrentIndex(test_value)
    result = dialog.action_source_changed()
    assert dialog.form.source_combo.error
    assert not result["valid"]
    assert dialog.form.source_combo.currentText() == ""
    assert dialog.TOOLTIPS["source_combo"] in dialog.form.source_combo.toolTip()
    assert result["msg"] in dialog.form.source_combo.toolTip()
    datafile_close(parts_file)


def test_106_05_action_description_edit(qtbot, filesystem):
    """
    The 'description' entry is required and can be 1 to 255
    characters long. The description field have a default upper limit
    of 255 characters and a default minimum length of 1 character set in
    the validation class.
    """
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    # length within bounds
    dialog.form.description_edit.setText(test_string)
    dialog.form.description_edit.editingFinished.emit()
    assert not dialog.form.description_edit.error
    assert dialog.form.description_edit.text() == test_string
    assert dialog.form.description_edit.toolTip() == dialog.TOOLTIPS["description_edit"]

    # length exceeds max length
    dialog.form.description_edit.setText(long_string)
    result = dialog.action_description_edit()
    assert dialog.form.description_edit.error
    assert not result["valid"]
    assert dialog.form.description_edit.text() == long_string
    assert result["msg"] in dialog.form.description_edit.toolTip()
    assert dialog.TOOLTIPS["description_edit"] in dialog.form.description_edit.toolTip()

    # length less than min length
    dialog.form.description_edit.setText("")
    result = dialog.action_description_edit()
    assert dialog.form.description_edit.error
    assert not result["valid"]
    assert dialog.form.description_edit.text() == ""
    assert result["msg"] in dialog.form.description_edit.toolTip()
    assert dialog.TOOLTIPS["description_edit"] in dialog.form.description_edit.toolTip()
    datafile_close(parts_file)


def test_106_06_action_remarks_changed(qtbot, filesystem):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    dialog.form.remarks_edit.setText(test_string)
    dialog.form.remarks_edit.editingFinished.emit()
    assert not dialog.form.remarks_edit.error
    assert dialog.form.remarks_edit.text() == test_string
    assert dialog.form.remarks_edit.toolTip() == dialog.TOOLTIPS["remarks_edit"]

    # text fields have a default upper limit of 255 characters set in the
    # validation class.
    dialog.form.remarks_edit.setText(long_string)
    result = dialog.action_remarks_changed()
    assert dialog.form.remarks_edit.error
    assert not result["valid"]
    assert dialog.form.remarks_edit.text() == long_string
    assert result["msg"] in dialog.form.remarks_edit.toolTip()
    assert dialog.TOOLTIPS["remarks_edit"] in dialog.form.remarks_edit.toolTip()
    datafile_close(parts_file)


def test_106_09_clear_dialog(qtbot, filesystem):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    dialog = PartDialog(main, parts_file, part_value_set[0][0], Dialog.EDIT_ELEMENT)
    assert dialog.form.record_id_edit.text() == str(part_value_set[0][0])
    dialog.clear_dialog()
    assert dialog.form.part_number_combo.count() == len(part_value_set)
    assert dialog.form.part_number_edit.text() == ""
    assert dialog.form.part_number_combo.currentText() == ""
    assert dialog.form.record_id_edit.text() == "0"
    assert dialog.form.source_combo.currentText() == ""
    assert dialog.form.description_edit.text() == ""
    assert dialog.form.remarks_edit.text() == ""
    datafile_close(parts_file)


def test_106_10_action_part_number_combo_changed(qtbot, filesystem):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    # set new part number with no other changes.
    part1 = Part(parts_file, part_value_set[1][1], "part_number")
    part2 = Part(parts_file, part_value_set[0][1], "part_number")
    dialog = PartDialog(main, parts_file, part1.get_record_id())
    dialog.form.part_number_combo.setCurrentText(part1.get_part_number())
    assert dialog.form.part_number_combo.currentText() == part1.get_part_number()

    dialog.form.part_number_combo.setCurrentText(part2.get_part_number())
    dialog.form.part_number_combo.activated.emit(
        dialog.form.part_number_combo.currentIndex()
    )
    assert (
        dialog.form.source_combo.currentText()
        == Source(parts_file, part2.get_source()).get_source()
    )
    assert dialog.form.description_edit.text() == part2.get_description()
    assert dialog.form.remarks_edit.text() == part2.get_remarks()
    assert dialog.form.total_qty_text.text() == str(part2.get_total_quantity())
    assert (
        dialog.form.order_table.rowCount()
        == OrderLineSet(
            parts_file, "part_number", part2.get_part_number()
        ).get_number_elements()
    )
    assert not dialog.form.part_number_combo.error
    assert (
        dialog.form.part_number_combo.toolTip() == dialog.TOOLTIPS["part_number_combo"]
    )
    datafile_close(parts_file)


def test_106_11_action_part_number_combo_changed(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes

    # set new part number after changing one dialog entry
    part1 = Part(parts_file, part_value_set[1][1], "part_number")
    part2 = Part(parts_file, part_value_set[0][1], "part_number")
    dialog = PartDialog(main, parts_file, part1.get_record_id())

    assert dialog.form.part_number_combo.currentText() == part1.get_part_number()
    dialog.form.part_number_combo.setCurrentText(part2.get_part_number())
    assert dialog.form.part_number_combo.currentText() == part2.get_part_number()
    dialog.form.description_edit.setText("new description")
    dialog.form.description_edit.editingFinished.emit()
    dialog.form.part_number_combo.activated.emit(
        dialog.form.part_number_combo.currentIndex()
    )
    assert dialog.form.part_number_combo.currentText() == part2.get_part_number()
    assert (
        dialog.form.source_combo.currentText()
        == Source(parts_file, part2.get_source()).get_source()
    )
    assert dialog.form.description_edit.text() == part2.get_description()
    assert dialog.form.remarks_edit.text() == part2.get_remarks()
    assert dialog.form.total_qty_text.text() == str(part2.get_total_quantity())
    datafile_close(parts_file)


def test_106_12_action_part_number_combo_changed(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    mocker.patch.object(Part, "update")
    Part.update.return_value = False

    # set new part number after changing one dialog entry, part update fails
    part1 = Part(parts_file, part_value_set[1][1], "part_number")
    part2 = Part(parts_file, part_value_set[0][1], "part_number")
    new_description = "new description"
    dialog = PartDialog(main, parts_file, part1.get_record_id())

    assert dialog.form.part_number_combo.currentText() == part1.get_part_number()
    dialog.form.part_number_combo.setCurrentText(part2.get_part_number())
    assert dialog.form.part_number_combo.currentText() == part2.get_part_number()
    dialog.form.description_edit.setText(new_description)
    dialog.form.description_edit.editingFinished.emit()
    dialog.form.part_number_combo.activated.emit(
        dialog.form.part_number_combo.currentIndex()
    )
    assert dialog.form.part_number_combo.currentText() == part2.get_part_number()
    assert (
        dialog.form.source_combo.currentText()
        == Source(parts_file, part2.get_source()).get_source()
    )
    assert dialog.form.description_edit.text() == new_description
    assert dialog.form.remarks_edit.text() == part2.get_remarks()
    datafile_close(parts_file)


def test_106_13_action_part_number_combo_changed(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.No

    # don't save, load new part values
    part1 = Part(parts_file, part_value_set[1][1], "part_number")
    part2 = Part(parts_file, part_value_set[0][1], "part_number")
    new_description = "new description"
    dialog = PartDialog(main, parts_file, part1.get_record_id())
    dialog.form.description_edit.setText(new_description)
    dialog.form.description_edit.editingFinished.emit()
    dialog.form.part_number_combo.setCurrentText(part2.get_part_number())
    assert not dialog.form.part_number_combo.currentText() == part1.get_part_number()
    dialog.form.part_number_combo.activated.emit(
        dialog.form.part_number_combo.currentIndex()
    )
    assert dialog.form.part_number_combo.currentText() == part2.get_part_number()
    assert (
        dialog.form.source_combo.currentText()
        == Source(parts_file, part2.get_source()).get_source()
    )
    datafile_close(parts_file)


def test_106_14_action_part_number_combo_changed(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Cancel

    # cancel change after changing one dialog entry
    part1 = Part(parts_file, part_value_set[1][1], "part_number")
    part2 = Part(parts_file, part_value_set[0][1], "part_number")
    new_description = "new description"
    dialog.form.description_edit.setText(new_description)
    dialog.form.description_edit.editingFinished.emit()
    dialog.form.part_number_combo.setCurrentText(part1.get_part_number())
    assert not dialog.form.part_number_combo.currentText() == part2.get_part_number()
    dialog.form.part_number_combo.activated.emit(
        dialog.form.part_number_combo.currentIndex()
    )
    assert dialog.form.part_number_combo.currentText() == part1.get_part_number()
    datafile_close(parts_file)


def test_106_15_action_delete(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)

    # delete an part
    dialog = PartDialog(main, parts_file, 1954, Dialog.EDIT_ELEMENT)
    assert dialog.form.record_id_edit.text() == "1954"
    partset_size = PartSet(parts_file).get_number_elements()
    dialog.form.delete_button.click()
    assert dialog.form.record_id_edit.text() == "0"
    new_partset_size = PartSet(parts_file).get_number_elements()
    assert partset_size - new_partset_size == 1

    # try to delete a invalid item
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok
    partset_size = PartSet(parts_file).get_number_elements()
    dialog = PartDialog(main, parts_file, None, Dialog.EDIT_ELEMENT)
    dialog.action_delete()
    new_partset_size = PartSet(parts_file).get_number_elements()
    assert partset_size == new_partset_size

    # delete action fails
    mocker.patch.object(Part, "delete")
    Part.delete.return_value = False
    dialog = PartDialog(main, parts_file, 184, Dialog.EDIT_ELEMENT)
    partset_size = PartSet(parts_file).get_number_elements()
    dialog.action_delete()
    new_partset_size = PartSet(parts_file).get_number_elements()
    assert partset_size == new_partset_size
    datafile_close(parts_file)


def test_106_15_action_save(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Ok

    partset_size = PartSet(parts_file).get_number_elements()
    return_value = dialog.action_save(Dialog.SAVE_DONE)
    assert return_value == 1
    new_partset_size = PartSet(parts_file).get_number_elements()
    assert partset_size == new_partset_size

    dialog = PartDialog(main, parts_file, 1954, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    assert save_code == 0  # item saved successfully
    partset_size = PartSet(parts_file).get_number_elements()
    assert partset_size == new_partset_size
    dialog.form.record_id_edit.setText("")
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    new_partset_size = PartSet(parts_file).get_number_elements()
    assert new_partset_size - partset_size == 1

    dialog = PartDialog(main, parts_file, 1954, Dialog.EDIT_ELEMENT)
    partset_size = PartSet(parts_file).get_number_elements()
    assert partset_size == new_partset_size
    dialog.form.record_id_edit.setText("")
    save_code = dialog.action_save(Dialog.SAVE_NEW)
    new_partset_size = PartSet(parts_file).get_number_elements()
    assert new_partset_size - partset_size == 1
    assert dialog.form.record_id_edit.text() == "0"
    assert dialog.form.part_number_edit.text() == ""

    dialog = PartDialog(main, parts_file, 1954, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(10)
    assert save_code == 2  # bad save command code

    # part update failed
    mocker.patch.object(Part, "update")
    Part.update.return_value = False
    dialog = PartDialog(main, parts_file, 1954, Dialog.EDIT_ELEMENT)
    save_code = dialog.action_save(Dialog.SAVE_DONE)
    assert save_code == 3
    datafile_close(parts_file)


def test_106_16a_action_part_number_edit_changed(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_part_dialog(qtbot, filesystem)
    mocker.patch.object(Dialog, "message_box_exec")

    # A. part number changed with no changes to current item
    dialog = PartDialog(main, parts_file, None, Dialog.ADD_ELEMENT)
    dialog.form.part_number_edit.setText("17001")
    dialog.form.action_part_number_edit_changed()
    assert not dialog.form.part_number_combo.isVisible()
    assert dialog.form.record_id_edit.text() == "0"
    assert dialog.form.source_combo.currentText() == ""
    dialog.form.source_combo.setCurrentText("Ebay")
    dialog.form.description_edit.setText("desc")
    dialog.form.remarks_edit.setText("remark")
    dialog.form.part_number_edit.setText("17002")
    dialog.form.action_part_number_edit_changed()
    assert dialog.form.record_id_edit.text() == "0"
    assert dialog.form.source_combo.currentText() == "Ebay"
    assert dialog.form.description_edit.text() == "desc"
    assert dialog.form.remarks_edit.text() == "remark"
    assert dialog.form.item_table.rowCount() == 0
    assert dialog.form.order_table.rowCount() == 0

    # B. Enter illegal part number
    dialog.form.part_number_edit.setText("")
    dialog.form.action_part_number_edit_changed()
    assert dialog.form.part_number_edit.error

    # C. Enter an existing part number.
    dialog.form.part_number_edit.setText("17005")
    dialog.form.action_part_number_edit_changed()
    dialog.form.part_number_combo.curentText = "17005"
    assert dialog.form.part_number_combo.isEnabled()
    assert not dialog.form.part_number_edit.isEnabled()
    datafile_close(parts_file)
