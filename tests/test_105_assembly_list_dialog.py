"""
Test the AssemblyListDialog class.

File:       test_104_assembly_list_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
Version     1.1.0
"""

import csv
import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

# from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog
from lbk_library.testing_support import datafile_close, datafile_create, filesystem
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from test_setup import datafile_name, item_value_set, load_all_datafile_tables

from dialogs import AssemblyListDialog
from elements import Item, Part
from pages import table_definition

file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.1.0": "Changed library 'PyQt5' to 'PySide6' and code cleanup",
}


# Main window with a config fragment.
class SimpleMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = QSettings("Unnamed Branch", "PartsTrackerTEet")
        self.config.beginGroup("settings")
        self.config.setValue("parts_file_dir", "Documents/PartsTracker/parts_files")
        self.config.setValue("list_files_dir", "Documents/PartsTracker/parts_listings")
        self.config.endGroup()


def setup_assembly_dialog(qtbot, tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + datafile_name
    parts_file = datafile_create(filename, table_definition)
    load_all_datafile_tables(parts_file)
    main_window = SimpleMainWindow()
    dialog = AssemblyListDialog(main_window, parts_file, Dialog.EDIT_ELEMENT)
    qtbot.addWidget(main_window)
    return (parts_file, main_window, dialog)


def test_105_01_class_type(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    assert isinstance(dialog, AssemblyListDialog)
    assert isinstance(dialog, Dialog)
    datafile_close(parts_file)


def test_105_02_set_tool_tips(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    dialog.set_tool_tips()
    assert dialog.start_edit.toolTip() == dialog.TOOLTIPS["start_assy"]
    assert dialog.stop_edit.toolTip() == dialog.TOOLTIPS["stop_assy"]
    assert dialog.save_location_edit.toolTip() == dialog.TOOLTIPS["save_loc"]
    assert dialog.cancel_button.toolTip() == dialog.TOOLTIPS["cancel"]
    assert dialog.save_button.toolTip() == dialog.TOOLTIPS["generate"]
    datafile_close(parts_file)


def test_105_03_action_start_changed(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    # verify initial value is blank
    assert dialog.start_edit.text() == ""
    dialog.start_edit.editingFinished.emit()
    assert dialog.start_edit.text() == ""
    test_value = "a"
    dialog.start_edit.setText(test_value)
    dialog.start_edit.editingFinished.emit()
    assert dialog.start_edit.text() == test_value.upper()
    datafile_close(parts_file)


def test_105_04_action_stop_changed(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    # verify initial value is blank
    assert dialog.stop_edit.text() == ""
    dialog.stop_edit.editingFinished.emit()
    assert dialog.stop_edit.text() == ""
    test_value = "a"
    dialog.stop_edit.setText(test_value)
    dialog.stop_edit.editingFinished.emit()
    assert dialog.stop_edit.text() == test_value.upper()
    datafile_close(parts_file)


def test_105_05_action_new_location(qtbot, tmp_path, mocker):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    # initial location
    assert dialog.save_location_edit.text() == dialog.config.value(
        "settings/list_files_dir"
    )

    mocker.patch.object(QFileDialog, "getExistingDirectory")
    test_dir = tmp_path / "PartsTracker/parts_list"
    QFileDialog.getExistingDirectory.return_value = test_dir

    dialog.new_location_action.trigger()
    assert dialog.save_location_edit.text() == str(test_dir)
    assert dialog.config.value("settings/list_files_dir") == test_dir

    datafile_close(parts_file)


def test_105_06_action_save_location_changed(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    # initial location
    assert dialog.save_location_edit.text() == dialog.config.value(
        "settings/list_files_dir"
    )

    test_dir = str(tmp_path / "PartsTracker/new_parts_list")
    assert not os.path.exists(test_dir)
    dialog.save_location_edit.setText(test_dir)
    dialog.save_location_edit.editingFinished.emit()
    assert os.path.exists(test_dir)
    assert dialog.save_location_edit.text() == test_dir
    assert dialog.config.value("settings/list_files_dir") == test_dir

    datafile_close(parts_file)


def test_105_07_get_start_stop_points(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    dialog.start_edit.setText("")
    start, stop = dialog.get_start_stop_points()
    assert start == "A"
    assert stop == "ZZZ"

    dialog.start_edit.setText("C")
    dialog.stop_edit.setText("")
    start, stop = dialog.get_start_stop_points()
    assert start == "C"
    assert stop == "CZZZ"

    datafile_close(parts_file)


def test_105_08_get_itemset(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    row_count = len(item_value_set)
    start = "A"
    end = "ZZZ"
    itemset = dialog.get_itemset(start, end)
    for i in range(row_count):
        print(i)
        print(itemset[i].get_properties())
q        print(item_value_set[i])
        print()

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


def test_105_09_write_item_line(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    os.mkdir(tmp_path / "PartsTracker")
    test_file = tmp_path / "PartsTracker/parts_list"
    csv_file = open(str(test_file) + ".csv", "w")
    writer = csv.writer(csv_file)

    item = Item(parts_file, 184)
    part = Part(parts_file, item.get_part_number(), "part_number")
    value = dialog.write_item_line(item, part, writer)
    csv_file.close()

    csv_file = open(str(test_file) + ".csv", "r")
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


def test_105_10_write_csv_file(qtbot, tmp_path):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    os.makedirs(tmp_path / "PartsTracker")
    test_file = tmp_path / "PartsTracker/parts_list.csv"
    item_set = dialog.get_itemset("A", "ZZZ")

    value = dialog.write_csv_file(test_file, item_set)
    assert value

    with open(test_file, "r") as fp:
        num_lines = len(fp.readlines())
    assert num_lines == len(item_set) + 1  # Length of item set plus header line


def test_105_10_action_write_file(qtbot, tmp_path, mocker):
    parts_file, main, dialog = setup_assembly_dialog(qtbot, tmp_path)

    mocker.patch.object(Dialog, "message_box_exec")
    Dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes

    test_dir = tmp_path / "PartsTracker/parts_listings"
    os.makedirs(test_dir)
    dialog.start_edit.setText("A")
    dialog.stop_edit.setText("ZZZ")
    dialog.save_location_edit.setText(str(test_dir))
    dialog.save_location_edit.editingFinished.emit()

    dialog.action_write_file()
    item_set = dialog.get_itemset("A", "ZZZ")
    test_file = test_dir / "A_ZZZ.csv"
    with open(test_file, "r") as fp:
        num_lines = len(fp.readlines())
    assert num_lines == len(item_set) + 1  # Length of item set plus header line
    assert dialog.start_edit.text() == ""
    assert dialog.stop_edit.text() == ""

    Dialog.message_box_exec.return_value = QMessageBox.StandardButton.No

    dialog.start_edit.setText("B")
    dialog.stop_edit.setText("")
    dialog.save_location_edit.setText(str(test_dir))
    dialog.save_location_edit.editingFinished.emit()

    dialog.action_write_file()
    item_set = dialog.get_itemset("B", "BZZZ")
    test_file = test_dir / "B_BZZZ.csv"
    with open(test_file, "r") as fp:
        num_lines = len(fp.readlines())
    assert num_lines == len(item_set) + 1  # Length of item set plus header line
    assert dialog.isHidden()  # widget is hidden on a close event.
