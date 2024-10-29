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
from lbk_library.testing_support import datafile_close, datafile_create, filesystem
from test_setup import datafile_name, load_all_datafile_tables

from dialogs import EditConditionsDialog
from elements import ConditionSet
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}

header_names = ["Record Id", "Condition"]


def setup_table_tests(qtbot, filesystem):
    filename = filesystem + "/" + datafile_name
    parts_file = datafile_create(filename, table_definition)
    load_all_datafile_tables(parts_file)
    data_set = ConditionSet(parts_file)
    dialog = EditConditionsDialog(None, parts_file)
    qtbot.addWidget(dialog)
    return (dialog, parts_file, data_set)


def test_103_01_class_type(qtbot, filesystem):
    dialog, parts_file, data_set = setup_table_tests(qtbot, filesystem)

    assert isinstance(dialog, EditConditionsDialog)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog.conditions, ConditionSet)
    for i in range(len(header_names)):
        assert dialog.model._header_titles[i] == header_names[i]
    datafile_close(parts_file)


def test_103_02_build_data_set(qtbot, filesystem):
    dialog, parts_file, data_set = setup_table_tests(qtbot, filesystem)

    dataset = dialog.build_data_set(dialog.conditions)
    set = dialog.conditions.get_property_set()
    for row in range(len(set)):
        for column in range(len(set[row].get_properties())):
            assert dataset[row][column] == set[row]._get_property(
                dialog.COLUMN_NAMES[column]
            )


def test_103_03_setup_form(qtbot, filesystem):
    dialog, parts_file, data_set = setup_table_tests(qtbot, filesystem)

    assert dialog.form.windowTitle() == "Edit Item Conditions"
    assert (
        dialog.form_label.text()
        == "<b>Add</b> or <b>Edit</b> the set of Item Conditions."
    )


def test_103_04_append_row(qtbot, filesystem):
    dialog, parts_file, data_set = setup_table_tests(qtbot, filesystem)

    row_count = dialog.model.rowCount()
    dialog.append_row()
    assert dialog.model.rowCount() == row_count + 1


def test_103_05_show_record_id(qtbot, filesystem):
    dialog, parts_file, data_set = setup_table_tests(qtbot, filesystem)

    assert not dialog.form.record_id_checkbox.isChecked()
    assert dialog.table.isColumnHidden(dialog.COLUMN_NAMES.index("record_id"))

    dialog.form.record_id_checkbox.click()
    assert dialog.form.record_id_checkbox.isChecked()
    assert not dialog.table.isColumnHidden(dialog.COLUMN_NAMES.index("record_id"))

    dialog.form.record_id_checkbox.click()
    assert not dialog.form.record_id_checkbox.isChecked()
    assert dialog.table.isColumnHidden(dialog.COLUMN_NAMES.index("record_id"))
