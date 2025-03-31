"""
Test the EditConditionsDialog. class.

File:       test_103_edit_conditions_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.0
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library.gui import Dialog
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
)
from PySide6.QtCore import QModelIndex, Qt
from test_setup import (
    datafile_name,
    load_all_datafile_tables,
)

from dialogs import EditConditionsDialog
from elements import Condition, ConditionSet
from forms import Ui_TableDialog
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


def setup_table_tests(qtbot, tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + datafile_name
    parts_file = datafile_create(filename, table_definition)
    load_all_datafile_tables(parts_file)
    data_set = ConditionSet(parts_file)
    dialog = EditConditionsDialog(None, parts_file)
    qtbot.addWidget(dialog)
    return (dialog, parts_file, data_set)


def test_103_01_class_type(qtbot, tmp_path):
    dialog, parts_file, data_set = setup_table_tests(qtbot, tmp_path)

    assert isinstance(dialog, EditConditionsDialog)
    assert isinstance(dialog, Ui_TableDialog)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog.conditions, ConditionSet)


def test_103_02_build_data_set(qtbot, tmp_path):
    dialog, parts_file, data_set = setup_table_tests(qtbot, tmp_path)

    dataset = dialog.build_data_set()
    set = dialog.conditions.get_property_set()
    for row in range(len(set)):
        for column in range(len(set[row].get_properties())):
            assert dataset[row][column] == set[row]._get_property(
                dialog.COLUMN_NAMES[column]
            )


def test_103_03_setup_form(qtbot, tmp_path):
    dialog, parts_file, data_set = setup_table_tests(qtbot, tmp_path)

    dialog.setup_form()
    assert dialog.windowTitle() == "Edit Item Conditions"
    assert (
        dialog.form_label.text()
        == "<b>Add</b> or <b>Edit</b> the set of Item Conditions."
    )
    for i in range(len(dialog.HEADER_TITLES)):
        assert dialog.model._header_titles[i] == dialog.HEADER_TITLES[i]
    datafile_close(parts_file)


def test_103_04_append_row(qtbot, tmp_path):
    dialog, parts_file, data_set = setup_table_tests(qtbot, tmp_path)

    row_count = dialog.model.rowCount()
    dialog.append_row()
    assert dialog.model.rowCount() == row_count + 1


def test_103_05_show_record_id(qtbot, tmp_path):
    dialog, parts_file, data_set = setup_table_tests(qtbot, tmp_path)

    assert not dialog.record_id_checkbox.isChecked()
    assert dialog.table.isColumnHidden(dialog.COLUMN_NAMES.index("record_id"))

    dialog.record_id_checkbox.click()
    assert dialog.record_id_checkbox.isChecked()
    assert not dialog.table.isColumnHidden(dialog.COLUMN_NAMES.index("record_id"))

    dialog.record_id_checkbox.click()
    assert not dialog.record_id_checkbox.isChecked()
    assert dialog.table.isColumnHidden(dialog.COLUMN_NAMES.index("record_id"))


def test_103_06_data_changed(qtbot, tmp_path):
    dialog, parts_file, data_set = setup_table_tests(qtbot, tmp_path)

    dialog._change_in_process = True
    dialog.data_changed(QModelIndex(), QModelIndex())
    assert dialog._change_in_process

    row = 0
    column = 1
    condition = Condition(data_set)
    test_data = "Not Usable"
    results = condition.set_condition(test_data)

    dialog._change_in_process = False
    index = dialog.model.createIndex(0, 1)
    dialog.model.setData(index, test_data)

    assert dialog.model.data(index, Qt.ItemDataRole.DisplayRole) == test_data
    assert (
        dialog.model.data(index, Qt.ItemDataRole.ToolTipRole) == dialog.TOOLTIPS[column]
    )
    assert (
        dialog.model.data(index, Qt.ItemDataRole.BackgroundRole)
        == dialog.NORMAL_BACKGROUND
    )

    test_data = ""
    results = condition.set_condition(test_data)
    dialog.model.setData(index, test_data)
    assert dialog.model.data(index, Qt.ItemDataRole.DisplayRole) == test_data
    assert results["msg"] in dialog.model.data(index, Qt.ItemDataRole.ToolTipRole)
    assert dialog.TOOLTIPS[column] in dialog.model.data(
        index, Qt.ItemDataRole.ToolTipRole
    )
    assert (
        dialog.model.data(index, Qt.ItemDataRole.BackgroundRole)
        == dialog.ERROR_BACKGROUND
    )

    test_data = "new_condition"
    index = dialog.model.createIndex(data_set.get_number_elements(), 1)
    orig_num_elements = ConditionSet(parts_file).get_number_elements()
    dialog.model.setData(index, test_data)
    assert dialog.model.data(index, Qt.ItemDataRole.DisplayRole) == test_data
    assert (
        dialog.model.data(index, Qt.ItemDataRole.ToolTipRole) == dialog.TOOLTIPS[column]
    )
    assert (
        dialog.model.data(index, Qt.ItemDataRole.BackgroundRole)
        == dialog.NORMAL_BACKGROUND
    )

    assert not dialog._change_in_process

def test_103_07_close_form(qtbot, tmp_path):
    dialog, parts_file, data_set = setup_table_tests(qtbot, tmp_path)

    assert dialog.close_form()

