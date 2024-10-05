"""
Test the AssemblyListDialog class.

File:       test_104_assembly_list_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
Version     1.0.0
"""

import csv
import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import DataFile  # , Element
from lbk_library.gui import Dialog
from lbk_library.testing_support import datafile_close, datafile_create, filesystem
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QFileDialog, QMainWindow, QMessageBox
from test_setup import datafile_name, item_value_set, load_all_datafile_tables

from dialogs import AssemblyListDialog, BaseDialog
from elements import Item, Part
from pages import table_definition

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}

# a basic empty config file for part_tracker testing.
test_config = {
    "settings": {
        "recent_files": [],
        "test_file_file_dir": "",
        "assy_list_dir": "",
    },
    "recent_files": ["", "", "", ""],
    "geometry": [0, 0, 1237, 908],
}


# fill the config directory locations
def build_test_config():
    config = QSettings("Unnamed Branch", "PartsTrackerTest")
    config.beginGroup("settings")
    config.setValue("parts_file_dir", "Documents/PartsTracker")
    config.setValue("list_files_dir", "Documents/PartsTracker/parts_listings")
    config.endGroup()

    config.beginGroup("recent_files")  # 4 empty file names
    config.setValue("file1", "")
    config.setValue("file2", "")
    config.setValue("file3", "")
    config.setValue("file4", "")
    config.endGroup()

    config.beginGroup("geometry")
    config.setValue("x", 0)  # 'x': top of window
    config.setValue("y", 0)  # 'y': left side of window
    config.setValue("width", 1250)  # width of window
    config.setValue("height", 920)  # height of window
    config.endGroup()

    return config


# dummy function to represent the assembly tree page updating.
# def assy_tree_update_tree():
#    return


def setup_assembly_dialog(qtbot, filesystem):
    filename = filesystem + "/" + datafile_name
    parts_file = datafile_create(filename, table_definition)
    load_all_datafile_tables(parts_file)
    main = QMainWindow()
    dialog = AssemblyListDialog(main, parts_file, build_test_config())
    qtbot.addWidget(main)
    return (parts_file, main, dialog)


def test_105_01_class_type(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    assert isinstance(dialog, AssemblyListDialog)
    assert isinstance(dialog, BaseDialog)
    datafile_close(parts_file)


def test_105_02_set_tool_tips(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    dialog.set_tool_tips()
    assert dialog.form.start_edit.toolTip() == dialog.TOOLTIPS["start_assy"]
    assert dialog.form.stop_edit.toolTip() == dialog.TOOLTIPS["stop_assy"]
    assert dialog.form.save_location_edit.toolTip() == dialog.TOOLTIPS["save_loc"]
    assert dialog.form.cancel_button.toolTip() == dialog.TOOLTIPS["cancel"]
    assert dialog.form.save_button.toolTip() == dialog.TOOLTIPS["generate"]
    datafile_close(parts_file)


def test_105_03_action_start_changed(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    # verify initial value is blank
    assert dialog.form.start_edit.text() == ""
    dialog.form.start_edit.editingFinished.emit()
    assert dialog.form.start_edit.text() == ""
    test_value = "a"
    dialog.form.start_edit.setText(test_value)
    dialog.form.start_edit.editingFinished.emit()
    assert dialog.form.start_edit.text() == test_value.upper()
    datafile_close(parts_file)


def test_105_04_action_stop_changed(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    # verify initial value is blank
    assert dialog.stop_edit.text() == ""
    dialog.form.stop_edit.editingFinished.emit()
    assert dialog.stop_edit.text() == ""
    test_value = "a"
    dialog.form.stop_edit.setText(test_value)
    dialog.form.stop_edit.editingFinished.emit()
    assert dialog.stop_edit.text() == test_value.upper()
    datafile_close(parts_file)


def test_105_05_action_new_location(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    # initial location
    assert dialog.form.save_location_edit.text() == dialog.config.value(
        "settings/list_files_dir"
    )

    mocker.patch.object(QFileDialog, "getExistingDirectory")
    test_dir = filesystem + "/" + "PartsTracker/parts_list"
    QFileDialog.getExistingDirectory.return_value = test_dir

    dialog.new_location_action.trigger()
    assert dialog.form.save_location_edit.text() == test_dir
    assert dialog.config.value("settings/list_files_dir") == test_dir

    datafile_close(parts_file)


def test_105_06_action_save_location_changed(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    # initial location
    assert dialog.form.save_location_edit.text() == dialog.config.value(
        "settings/list_files_dir"
    )

    test_dir = filesystem + "/" + "PartsTracker/new_parts_list"
    assert not os.path.exists(test_dir)
    dialog.form.save_location_edit.setText(test_dir)
    dialog.save_location_edit.editingFinished.emit()
    assert os.path.exists(test_dir)
    assert dialog.form.save_location_edit.text() == test_dir
    assert dialog.config.value("settings/list_files_dir") == test_dir

    datafile_close(parts_file)


def test_104_07_get_start_stop_points(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    dialog.form.start_edit.setText("")
    start, stop = dialog.get_start_stop_points()
    assert start == "A"
    assert stop == "ZZZ"

    dialog.form.start_edit.setText("C")
    dialog.form.stop_edit.setText("")
    start, stop = dialog.get_start_stop_points()
    assert start == "C"
    assert stop == "CZZZ"

    datafile_close(parts_file)


def test_104_08_get_itemset(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    row_count = len(item_value_set)
    start = "A"
    end = "ZZZ"
    itemset = dialog.get_itemset(start, end)
    assert row_count == len(itemset)

    start = "C"
    end = "CZZZ"
    row_count = 0
    for row in item_value_set:
        if row[2] >= start and row[2] < end:
            row_count += 1
    itemset = dialog.get_itemset(start, end)
    assert row_count == len(itemset)

    datafile_close(parts_file)


def test_105_09_write_item_line(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    os.mkdir(filesystem + "/" + "PartsTracker")
    test_file = filesystem + "/" + "PartsTracker/parts_list"
    csv_file = open(test_file + ".csv", "w")
    writer = csv.writer(csv_file)

    item = Item(parts_file, 184)
    part = Part(parts_file, item.get_part_number(), "part_number")
    value = dialog.write_item_line(item, part, writer)
    csv_file.close()

    csv_file = open(test_file + ".csv", "r")
    reader = csv.reader(csv_file)
    line = next(reader)
    assert item.get_assembly() == line[0]
    assert item.get_record_id() == int(line[1])
    assert item.get_part_number() == line[2]
    assert part.get_description() == line[3]
    assert item.get_quantity() == int(line[4])
    assert item.get_condition() == int(line[5])
    if item.get_installed():
        assert "X" == line[6]
    else:
        assert "" == line[6]
    assert item.get_remarks() == line[7]
    assert part.get_remarks() == line[8]
    csv_file.close()

    datafile_close(parts_file)


def test_105_10_write_csv_file(qtbot, filesystem):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    os.makedirs(filesystem + "/" + "PartsTracker")
    test_file = filesystem + "/" + "PartsTracker/parts_list.csv"
    item_set = dialog.get_itemset("A", "ZZZ")

    value = dialog.write_csv_file(test_file, item_set)
    assert value

    with open(test_file, "r") as fp:
        num_lines = len(fp.readlines())
    assert num_lines == len(item_set) + 1  # Length of item set plus header line


def test_105_10_action_write_file(qtbot, filesystem, mocker):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, filesystem)

    mocker.patch.object(Dialog, "message_box_exec")
    Dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes

    test_dir = filesystem + "/PartsTracker/parts_listings"
    os.makedirs(test_dir)
    dialog.form.start_edit.setText("A")
    dialog.form.stop_edit.setText("ZZZ")
    dialog.form.save_location_edit.setText(test_dir)
    dialog.save_location_edit.editingFinished.emit()

    dialog.action_write_file()
    item_set = dialog.get_itemset("A", "ZZZ")
    test_file = test_dir + "/A_ZZZ.csv"
    with open(test_file, "r") as fp:
        num_lines = len(fp.readlines())
    assert num_lines == len(item_set) + 1  # Length of item set plus header line
    assert dialog.form.start_edit.text() == ""
    assert dialog.form.stop_edit.text() == ""

    Dialog.message_box_exec.return_value = QMessageBox.StandardButton.No

    dialog.form.start_edit.setText("B")
    dialog.form.stop_edit.setText("")
    dialog.form.save_location_edit.setText(test_dir)
    dialog.save_location_edit.editingFinished.emit()

    dialog.action_write_file()
    item_set = dialog.get_itemset("B", "BZZZ")
    test_file = test_dir + "/B_BZZZ.csv"
    with open(test_file, "r") as fp:
        num_lines = len(fp.readlines())
    assert num_lines == len(item_set) + 1  # Length of item set plus header line
    assert dialog.isHidden()  # widget is hidden on a close event.
