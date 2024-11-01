"""
Test the MainWindow class.

File:       test_204_main_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

import os
import sys
from pathlib import Path

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import DataFile
from lbk_library.gui import Dialog
from lbk_library.testing_support import datafile_close, datafile_create, filesystem
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QTableWidget,
    QTabWidget,
    QTreeWidget,
)
from test_setup import (
    directories,
    item_value_set,
    load_all_datafile_tables,
    order_value_set,
    part_value_set,
    restore_config_file,
    save_config_file,
    saved_config_file,
)

from dialogs import (  # ChangePartNumberDialog,; EditStructureDialog,
    AssemblyListDialog,
    EditConditionsDialog,
    EditSourcesDialog,
    ItemDialog,
    OrderDialog,
    PartDialog,
)
from pages import (
    AssemblyTreePage,
    MainWindow,
    OrdersListPage,
    PartsListPage,
    table_definition,
)

# Need to save and restore the existing config file so we don't
# overwrite it during testing.
saved_config_file = QSettings("Unnamed Branch", "PartsTrackerSaved")


def save_config_file(original_config_file):
    # Save the actual config file contents to be restored at end of test.
    for group in original_config_file.childGroups():
        saved_config_file.beginGroup(group)
        original_config_file.beginGroup(group)
        for key in original_config_file.childKeys():
            saved_config_file.setValue(key, original_config_file.value(key))
        original_config_file.endGroup()
        saved_config_file.endGroup()


def restore_config_file(original_config_file):
    # Restore the config file contents from the previously stored values
    for group in saved_config_file.childGroups():
        saved_config_file.beginGroup(group)
        original_config_file.beginGroup(group)
        for key in original_config_file.childKeys():
            original_config_file.setValue(key, saved_config_file.value(key))
        original_config_file.endGroup()
        saved_config_file.endGroup()


def set_environment(filesystem, qtbot):
    # setup common base settings for running tests
    source = filesystem
    parts_file_path = str(os.path.join(source, directories[2]))
    main = MainWindow()
    qtbot.addWidget(main)
    return (main, source, parts_file_path)


def test_204_01_class_type(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    assert isinstance(main, MainWindow)
    assert isinstance(main, QMainWindow)
    assert type(main.parts_file) == DataFile
    save_config_file(QSettings("Unnamed Branch", "PartsTrackerTest"))
    datafile_close(main.parts_file)


def test_204_02_initialize_config_file(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    config = main.initialize_config_file()
    assert "Documents/PartsTracker" in config.value("settings/parts_file_dir")
    assert "Documents/PartsTracker/parts_listings" in config.value(
        "settings/list_files_dir"
    )
    assert config.value("recent_files/file1") == ""
    assert config.value("recent_files/file2") == ""
    assert config.value("recent_files/file3") == ""
    assert config.value("recent_files/file4") == ""
    assert config.value("geometry/x") == int(0)
    assert config.value("geometry/y") == int(0)
    assert config.value("geometry/width") == int(1250)
    assert config.value("geometry/height") == int(920)
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_03_menus_enabled(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    main.set_menus_enabled(True)
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.form.menu_parts.isEnabled()
    assert main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()

    main.set_menus_enabled(False)
    assert not main.form.menu_assembly_listing.isEnabled()
    assert not main.form.menu_parts.isEnabled()
    assert not main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_04_open_file(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)
    config = main.config

    main.initialize_config_file()
    # no current or previous parts files available
    # file menu should be enabled, all other menus disabled
    parts_file = main.open_file()
    assert isinstance(parts_file, DataFile)
    assert not main.form.menu_assembly_listing.isEnabled()
    assert not main.form.menu_parts.isEnabled()
    assert not main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    parts_file.sql_close()

    # Create a file; all menus should be enabled
    config.setValue(
        "recent_files/file1", os.path.join(parts_file_path, "test_204_04_file1.parts")
    )
    parts_file = main.open_file()
    assert isinstance(parts_file, DataFile)
    assert os.path.isfile(config.value("recent_files/file1"))
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.form.menu_parts.isEnabled()
    assert main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_05_exit_app_action(qtbot, filesystem):
    main, source, parts_file_path = set_environment(filesystem, qtbot)
    config = main.config

    main.initialize_config_file()
    # set a dumming 'parts" file and open it.
    config.setValue(
        "recent_files/file1", os.path.join(parts_file_path, "test_204_05_file1.parts")
    )
    main.parts_file = main.open_file()
    assert isinstance(main.parts_file, DataFile)
    assert main.parts_file.sql_is_connected()

    main.exit_app_action()
    assert not main.parts_file.sql_is_connected()
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_06_get_recent_files_list(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    # Add files to to the recent files list. The config file should
    # reflect the added files
    main.initialize_config_file()
    main.config.setValue(
        "recent_files/file1", str(parts_file_path) + "/test_204_06_file1.parts"
    )
    main.config.setValue(
        "recent_files/file2", str(parts_file_path) + "/test_204_06_file2.parts"
    )
    main.config.setValue("recent_files/file3", "")
    main.config.setValue("recent_files/file4", "")

    recent_files = main.get_recent_files_list()
    assert len(recent_files) == 2
    assert recent_files[0] == str(parts_file_path) + "/test_204_06_file1.parts"
    assert recent_files[1] == str(parts_file_path) + "/test_204_06_file2.parts"
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_07_save_recent_files_list(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    recent_files = [
        str(parts_file_path) + "/test_204_07_file1.parts",
        str(parts_file_path) + "/test_204_07_file2.parts",
    ]

    main.save_recent_files_list(recent_files)
    assert (
        main.config.value("recent_files/file1")
        == str(parts_file_path) + "/test_204_07_file1.parts"
    )
    assert (
        main.config.value("recent_files/file2")
        == str(parts_file_path) + "/test_204_07_file2.parts"
    )
    assert main.config.value("recent_files/file3") == ""
    assert main.config.value("recent_files/file4") == ""
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_08_set_recent_files_menu(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    # recent_files setting is empty, files.recent files should be disabled.
    main.set_recent_files_menu()
    assert not main.form.menu_file_recent.isEnabled()

    # add files to settings.recent_files. menu should reflect files
    main.config.setValue(
        "recent_files/file1", str(parts_file_path) + "/test_204_08_file1.parts"
    )
    main.config.setValue(
        "recent_files/file2", str(parts_file_path) + "/test_204_08_file2.parts"
    )
    recent_files = main.get_recent_files_list()
    main.set_recent_files_menu()
    assert main.form.menu_file_recent.isEnabled()
    menu_actions = main.form.menu_file_recent.actions()
    for i in range(len(recent_files)):
        assert menu_actions[i].isVisible()
        assert menu_actions[i].text() == os.path.basename(
            main.config.value("recent_files/file" + str(i + 1))
        )
        i += 1
    while i < len(menu_actions):
        assert not menu_actions[i].isVisible()
        i += 1
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_09_set_tab_widgets(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.set_tab_widgets()
    tabwidget = main.form.centralWidget()
    assert isinstance(tabwidget, QTabWidget)
    assert isinstance(tabwidget.widget(0), QTreeWidget)
    assert isinstance(tabwidget.widget(1), QTableWidget)
    assert isinstance(tabwidget.widget(2), QTableWidget)


def test_204_10_configure_window(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    # Add files to settings.recent_files.
    main.config.setValue(
        "recent_files/file1", str(parts_file_path) + "/test_204_09t_file1.parts"
    )
    main.config.setValue(
        "recent_files/file2", str(parts_file_path) + "/test_204_09_file2.parts"
    )
    # configure the main window,files.recent_files should be enabled and
    # the display pages shoud be initialized.
    main.configure_window()
    assert main.form.menu_file_recent.isEnabled()
    assert isinstance(main.assembly_tree, AssemblyTreePage)
    assert isinstance(main.part_list, PartsListPage)
    assert isinstance(main.order_list, OrdersListPage)
    assert main.form.tab_widget.currentIndex() == 0

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_11_move_event(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    move_value = 10
    main.initialize_config_file()
    main.configure_window()
    main.move(move_value, move_value)
    assert main.config.value("geometry/x") == int(move_value)
    assert main.config.value("geometry/y") == int(move_value)

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_12_resize_event(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    resize_value = 700
    main.initialize_config_file()
    main.configure_window()
    main.resize(resize_value, resize_value)
    assert main.config.value("geometry/width") == int(resize_value)
    assert main.config.value("geometry/height") == int(resize_value)

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_13_get_existing_filename(filesystem, qtbot, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    test_file_name = "test_204_10_file.parts"
    mocker.patch.object(QFileDialog, "getOpenFileName")
    QFileDialog.getOpenFileName.return_value = (test_file_name, "Parts Files (*.parts)")
    value = main.get_existing_filename()
    assert value == test_file_name
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_14_get_new_filename(filesystem, qtbot, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)
    main.initialize_config_file()
    test_file_name = "test_204_11_file.parts"
    mocker.patch.object(QFileDialog, "getSaveFileName")
    QFileDialog.getSaveFileName.return_value = (test_file_name, "parts file")
    value = main.get_new_filename()
    assert value == test_file_name
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_15_load_file(filesystem, qtbot):
    main, source, parts_file_path = set_environment(filesystem, qtbot)
    main.initialize_config_file()

    parts_file1 = source + "/test_204_15_file1.parts"
    datafile_create(parts_file1, table_definition)
    parts_file2 = source + "/test_204_15_file2.parts"
    datafile_create(parts_file2, table_definition)
    parts_file3 = source + "/test_204_15_file3.parts"
    datafile_create(parts_file3, table_definition)
    parts_file4 = source + "/test_204_15_file4.parts"
    datafile_create(parts_file4, table_definition)

    # load an initial file, number of recent files = 1
    main.load_file(parts_file1)
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.config.value("recent_files/file1") == str(parts_file1)

    # Load more files, the len of recent_files never exceeds 4 and
    #   the last loaded file is always first entry.
    main.load_file(str(parts_file2))
    assert len(main.get_recent_files_list()) == 2
    assert main.config.value("recent_files/file1") == str(parts_file2)
    assert main.config.value("recent_files/file2") == str(parts_file1)

    main.load_file(str(parts_file3))
    main.load_file(str(parts_file4))
    assert len(main.get_recent_files_list()) == 4
    assert main.config.value("recent_files/file1") == str(parts_file4)
    assert main.config.value("recent_files/file2") == str(parts_file3)
    assert main.config.value("recent_files/file3") == str(parts_file2)
    assert main.config.value("recent_files/file4") == str(parts_file1)
    assert len(main.get_recent_files_list()) == 4

    main.load_file(str(parts_file1))
    assert main.config.value("recent_files/file1") == str(parts_file1)
    assert main.config.value("recent_files/file2") == str(parts_file4)
    assert main.config.value("recent_files/file3") == str(parts_file3)
    assert main.config.value("recent_files/file4") == str(parts_file2)
    assert len(main.get_recent_files_list()) == 4

    main.load_file(str(parts_file4))
    assert main.config.value("recent_files/file1") == str(parts_file4)
    assert main.config.value("recent_files/file2") == str(parts_file1)
    assert main.config.value("recent_files/file3") == str(parts_file3)
    assert main.config.value("recent_files/file4") == str(parts_file2)
    assert len(main.get_recent_files_list()) == 4

    main.load_file(str(parts_file2))
    assert main.config.value("recent_files/file1") == str(parts_file2)
    assert main.config.value("recent_files/file2") == str(parts_file4)
    assert main.config.value("recent_files/file3") == str(parts_file1)
    assert main.config.value("recent_files/file4") == str(parts_file3)
    assert len(main.get_recent_files_list()) == 4

    main.load_file("")  # empty file path, do nothing
    assert main.config.value("recent_files/file1") == str(parts_file2)
    assert main.config.value("recent_files/file2") == str(parts_file4)
    assert main.config.value("recent_files/file3") == str(parts_file1)
    assert main.config.value("recent_files/file4") == str(parts_file3)
    assert len(main.get_recent_files_list()) == 4
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_16_file_new_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    file_path1 = source + "/Documents/parts_tracker/test_204_16_file1.parts"
    file_path2 = source + "/Documents/parts_tracker/test_204_16_file2.parts"

    mocker.patch.object(MainWindow, "get_new_filename")
    main.get_new_filename.return_value = str(file_path1)
    assert main.config.value("recent_files/file1") == ""
    main.file_new_action()
    assert main.config.value("recent_files/file1") == file_path1
    assert main.parts_file.sql_is_connected()

    main.get_new_filename.return_value = str(file_path2)
    main.form.action_file_new.trigger()
    assert main.config.value("recent_files/file1") == file_path2
    assert main.config.value("recent_files/file2") == file_path1
    assert main.parts_file.sql_is_connected()

    # cover new file with same name as existing file deletes existing file.
    main.form.action_file_new.trigger()
    assert main.config.value("recent_files/file1") == file_path2
    assert main.config.value("recent_files/file2") == file_path1
    assert main.parts_file.sql_is_connected()

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_17_file_open_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    test_file_name1 = source + "/Documents/parts_tracker/test_204_17_file2.parts"
    DataFile.new_file(test_file_name1, table_definition)
    test_file_name2 = source + "/Documents/parts_tracker/test_204_17_file3.parts"
    DataFile.new_file(test_file_name2, table_definition)

    mocker.patch.object(MainWindow, "get_existing_filename")
    main.get_existing_filename.return_value = test_file_name1

    # load an initial file, number of recent files = 1
    main.file_open_action()
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.config.value("recent_files/file1") == test_file_name1
    assert main.config.value("recent_files/file2") == ""

    # load second file, number of recent files = 2
    main.get_existing_filename.return_value = test_file_name2
    main.form.action_file_open.trigger()
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.config.value("recent_files/file1") == test_file_name2
    assert main.config.value("recent_files/file2") == test_file_name1

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_18_file_close_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    test_204_18_testfile = source + "/Documents/parts_tracker/test_file2.parts"
    DataFile.new_file(test_204_18_testfile, table_definition)

    mocker.patch.object(MainWindow, "get_existing_filename")
    main.get_existing_filename.return_value = test_204_18_testfile
    assert main.config.value("recent_files/file1") == ""
    main.file_open_action()
    assert main.config.value("recent_files/file1") == test_204_18_testfile
    assert main.parts_file.sql_is_connected()
    main.form.action_file_close.trigger()
    assert os.path.isfile(main.config.value("recent_files/file1"))
    assert main.config.value("recent_files/file1") == test_204_18_testfile
    assert not main.parts_file.sql_is_connected()
    assert not main.form.menu_assembly_listing.isEnabled()
    assert not main.form.menu_parts.isEnabled()
    assert not main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_19_recent_file_1_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    test_204_19_file1 = source + "/Documents/parts_tracker/test_204_19_testfile_0"
    DataFile.new_file(test_204_19_file1, table_definition)

    main.recent_file_1_action()
    assert main.config.value("recent_files/file1") == ""
    assert not main.form.menu_file_recent.isEnabled()

    main.load_file(test_204_19_file1)
    main.file_close_action()
    assert main.config.value("recent_files/file1") == test_204_19_file1
    assert main.form.menu_file_recent.isEnabled()

    main.form.action_recent_file_1.trigger()
    assert main.config.value("recent_files/file1") == test_204_19_file1
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.form.menu_parts.isEnabled()
    assert main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_20_recent_file_2_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    test_204_20_file1 = source + "/Documents/parts_tracker/test_204_20_testfile_0"
    DataFile.new_file(test_204_20_file1, table_definition)
    test_204_20_file2 = source + "/Documents/parts_tracker/test_204_20_testfile_1"
    DataFile.new_file(test_204_20_file2, table_definition)
    test_204_20_file3 = source + "/Documents/parts_tracker/test_204_20_testfile_2"
    DataFile.new_file(test_204_20_file3, table_definition)
    test_204_20_file4 = source + "/Documents/parts_tracker/test_204_20_testfile_3"
    DataFile.new_file(test_204_20_file4, table_definition)

    main.recent_file_2_action()
    assert main.config.value("recent_files/file1") == ""
    assert main.config.value("recent_files/file2") == ""
    assert not main.form.menu_file_recent.isEnabled()

    main.load_file(test_204_20_file1)
    main.file_close_action()
    main.load_file(test_204_20_file2)
    main.file_close_action()
    assert main.config.value("recent_files/file1") == test_204_20_file2
    assert main.config.value("recent_files/file2") == test_204_20_file1
    assert main.form.menu_file_recent.isEnabled()

    main.action_recent_file_2.trigger()
    assert main.config.value("recent_files/file1") == test_204_20_file1
    assert main.config.value("recent_files/file2") == test_204_20_file2
    assert main.config.value("recent_files/file3") == ""
    assert main.config.value("recent_files/file4") == ""
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_21_recent_file_3_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    test_204_21_file1 = source + "/Documents/parts_tracker/test_204_21_testfile_1"
    DataFile.new_file(test_204_21_file1, table_definition)
    test_204_21_file2 = source + "/Documents/parts_tracker/test_204_21_testfile_2"
    DataFile.new_file(test_204_21_file2, table_definition)
    test_204_21_file3 = source + "/Documents/parts_tracker/test_204_21_testfile_3"
    DataFile.new_file(test_204_21_file3, table_definition)
    test_204_21_file4 = source + "/Documents/parts_tracker/test_204_21_testfile_4"
    DataFile.new_file(test_204_21_file4, table_definition)

    main.recent_file_3_action()
    assert main.config.value("recent_files/file1") == ""
    assert main.config.value("recent_files/file2") == ""
    assert main.config.value("recent_files/file3") == ""
    assert not main.form.menu_file_recent.isEnabled()

    main.load_file(test_204_21_file1)
    main.file_close_action()
    main.load_file(test_204_21_file2)
    main.file_close_action()
    main.load_file(test_204_21_file3)
    main.file_close_action()
    assert main.config.value("recent_files/file1") == test_204_21_file3
    assert main.config.value("recent_files/file2") == test_204_21_file2
    assert main.config.value("recent_files/file3") == test_204_21_file1
    assert main.form.menu_file_recent.isEnabled()

    main.action_recent_file_3.trigger()
    assert main.config.value("recent_files/file1") == test_204_21_file1
    assert main.config.value("recent_files/file2") == test_204_21_file3
    assert main.config.value("recent_files/file3") == test_204_21_file2
    assert main.config.value("recent_files/file4") == ""
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_22_recent_file_4_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    main.initialize_config_file()
    test_204_22_file1 = source + "/Documents/parts_tracker/test_204_22_testfile_1"
    DataFile.new_file(test_204_22_file1, table_definition)
    test_204_22_file2 = source + "/Documents/parts_tracker/test_204_22_testfile_2"
    DataFile.new_file(test_204_22_file2, table_definition)
    test_204_22_file3 = source + "/Documents/parts_tracker/test_204_22_testfile_3"
    DataFile.new_file(test_204_22_file3, table_definition)
    test_204_22_file4 = source + "/Documents/parts_tracker/test_204_22_testfile_4"
    DataFile.new_file(test_204_22_file4, table_definition)

    main.recent_file_4_action()
    assert main.config.value("recent_files/file1") == ""
    assert main.config.value("recent_files/file2") == ""
    assert main.config.value("recent_files/file3") == ""
    assert main.config.value("recent_files/file4") == ""
    assert not main.form.menu_file_recent.isEnabled()

    main.load_file(test_204_22_file1)
    main.file_close_action()
    main.load_file(test_204_22_file2)
    main.file_close_action()
    main.load_file(test_204_22_file3)
    main.file_close_action()
    main.load_file(test_204_22_file4)
    main.file_close_action()
    assert main.config.value("recent_files/file1") == test_204_22_file4
    assert main.config.value("recent_files/file2") == test_204_22_file3
    assert main.config.value("recent_files/file3") == test_204_22_file2
    assert main.config.value("recent_files/file4") == test_204_22_file1
    assert main.form.menu_file_recent.isEnabled()

    main.action_recent_file_4.trigger()
    assert main.config.value("recent_files/file1") == test_204_22_file1
    assert main.config.value("recent_files/file2") == test_204_22_file4
    assert main.config.value("recent_files/file3") == test_204_22_file3
    assert main.config.value("recent_files/file4") == test_204_22_file2
    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_23_item_dialog_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    dialog = main.item_dialog_action("", Dialog.ADD_ELEMENT)
    assert isinstance(dialog, ItemDialog)
    assert not dialog.form.record_id_combo.isEnabled()
    dialog.close()
    dialog = main.item_dialog_action(None, Dialog.EDIT_ELEMENT)
    assert isinstance(dialog, ItemDialog)
    assert dialog.form.record_id_combo.isEnabled()
    dialog.close()

    main.form.action_new_item.trigger()
    assert isinstance(dialog, ItemDialog)
    dialog.close()
    main.form.action_edit_item.trigger()
    assert isinstance(dialog, ItemDialog)
    dialog.close()

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_24_action_edit_conditions(qtbot, filesystem):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    dialog = main.edit_conditions_action()
    assert isinstance(dialog, EditConditionsDialog)
    dialog.close()

    restore_config_file(main.config)
    datafile_close(main.parts_file)


# def test_204_25_edit_assembly_tree_action(qtbot, filesystem):
#    main, source, parts_file_path = set_environment(filesystem, qtbot)
#
#    dialog = main.edit_assembly_tree_action()
#    assert isinstance(dialog, EditStructureDialog)
#    dialog.close()
#
#    restore_config_file(main.config)
#    datafile_close(main.parts_file)


def test_204_26_save_assembly_list_action(qtbot, filesystem):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    dialog = main.save_assembly_list_action()
    assert isinstance(dialog, AssemblyListDialog)
    dialog.close()

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_27_update_assembly_tree_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    test_file_name = parts_file_path + "/test_204_27_file.parts"
    test_file = datafile_create(test_file_name, table_definition)
    load_all_datafile_tables(test_file)
    main.load_file(test_file_name)
    orig_tree_items = main.update_assembly_tree_action()
    query = {
        "type": "DELETE",
        "table": "items",
        "where": "ASSEMBLY = '" + item_value_set[0][2] + "'",
    }
    sql = main.parts_file.sql_query_from_array(query)
    result = main.parts_file.sql_query(sql)
    new_tree_items = main.update_assembly_tree_action()
    assert len(orig_tree_items) - len(new_tree_items) == 1

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_28_part_dialog_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    dialog = main.part_dialog_action("", Dialog.ADD_ELEMENT)
    assert isinstance(dialog, PartDialog)
    assert not dialog.form.part_number_combo.isEnabled()
    dialog.close()
    dialog = main.part_dialog_action(None, Dialog.EDIT_ELEMENT)
    assert isinstance(dialog, PartDialog)
    assert dialog.form.part_number_combo.isEnabled()
    dialog.close()

    main.form.action_new_part.trigger()
    assert isinstance(dialog, PartDialog)
    dialog.close()
    main.form.action_edit_part.trigger()
    assert isinstance(dialog, PartDialog)
    dialog.close()

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_29_update_sources_action(qtbot, filesystem):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    dialog = main.update_sources_action()
    assert isinstance(dialog, EditSourcesDialog)
    dialog.close()

    restore_config_file(main.config)
    datafile_close(main.parts_file)


# def test_204_30_part_change_pn_action(qtbot, filesystem):
#    main, source, parts_file_path = set_environment(filesystem, qtbot)
#
#    dialog = main.part_change_pn_dialog_action()
#    assert isinstance(dialog, ChangePartNumberDialog)
#
#    restore_config_file(main.config)
#    datafile_close(main.parts_file)


def test_204_31_update_parts_list_table_action(qtbot, filesystem):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    test_file_name = parts_file_path + "/test_204_31_file.parts"
    test_file = datafile_create(test_file_name, table_definition)
    load_all_datafile_tables(test_file)
    main.load_file(test_file_name)

    main.form.action_update_part_list_table.trigger()
    orig_number_rows = main.parts_list_widget.rowCount()
    query = {
        "type": "DELETE",
        "table": "parts",
        "where": "PART_NUMBER = '" + part_value_set[0][1] + "'",
    }
    sql = main.parts_file.sql_query_from_array(query)
    main.parts_file.sql_query(sql)
    main.form.action_update_part_list_table.trigger()
    new_number_rows = main.parts_list_widget.rowCount()
    assert orig_number_rows - new_number_rows == 1

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_32_order_dialog_action(qtbot, filesystem, mocker):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    dialog = main.order_dialog_action("", Dialog.ADD_ELEMENT)
    assert isinstance(dialog, OrderDialog)
    assert not dialog.form.order_number_combo.isEnabled()
    dialog.close()
    dialog = main.order_dialog_action(None, Dialog.EDIT_ELEMENT)
    assert isinstance(dialog, OrderDialog)
    assert dialog.form.order_number_combo.isEnabled()
    dialog.close()

    main.form.action_new_order.trigger()
    assert isinstance(dialog, OrderDialog)
    dialog.close()
    main.form.action_edit_order.trigger()
    assert isinstance(dialog, OrderDialog)
    dialog.close()

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_33_update_orders_list_table_action(qtbot, filesystem):
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    test_file_name = parts_file_path + "/test_204_33_file.parts"
    test_file = datafile_create(test_file_name, table_definition)
    load_all_datafile_tables(test_file)
    main.load_file(test_file_name)

    main.form.action_update_order_table.trigger()
    orig_number_rows = main.orders_list_widget.rowCount()
    query = {
        "type": "DELETE",
        "table": "orders",
        "where": "ORDER_NUMBER = '" + order_value_set[0][1] + "'",
    }
    sql = main.parts_file.sql_query_from_array(query)
    main.parts_file.sql_query(sql)
    main.form.action_update_order_table.trigger()
    new_number_rows = main.orders_list_widget.rowCount()
    assert orig_number_rows - new_number_rows == 1

    restore_config_file(main.config)
    datafile_close(main.parts_file)


def test_204_99_restore_config_file(qtbot, filesystem):
    # restore the saved config file.
    main, source, parts_file_path = set_environment(filesystem, qtbot)

    restore_config_file(main.config)
    datafile_close(main.parts_file)
