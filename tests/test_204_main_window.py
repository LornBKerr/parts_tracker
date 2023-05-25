"""
Test the MainWindow class.

File:       test_204_main_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys
from pathlib import Path

import pytest
from lbk_library import Dbal
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow
from pytestqt import qtbot
from test_setup import (
    build_test_config,
    db_create,
    db_open,
    directories,
    filesystem,
    test_config,
)

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from pages import MainWindow  # AssemblyTreePage, , OrdersListPage, PartsListPage


def set_environment(filesystem, qtbot):
    # setup common base settings for running tests
    source = filesystem
    config_dir = os.path.join(source, directories[0])
    db_file_path = os.path.join(source, directories[2])
    main = MainWindow(config_dir)
    qtbot.addWidget(main)
    config_file = build_test_config(source)
    main.update_config_file(config_file)
    return (main, source, db_file_path)


def test_204_01_class_type(qtbot):
    main = MainWindow()
    qtbot.addWidget(main)
    assert isinstance(main, MainWindow)
    assert isinstance(main, QMainWindow)


def test_204_02_get_set_config_file(filesystem, qtbot):
    source = filesystem
    main = MainWindow(source / ".config")
    qtbot.addWidget(main)
    ini_path = main.config_handler.config_path()
    assert not os.path.exists(ini_path)
    # read config file
    config = main.get_config_file()
    assert len(config["settings"]["recent_files"]) == 0

    # write config file
    assert not os.path.exists(ini_path)
    main.save_config_file(config)
    assert os.path.exists(ini_path)
    config = main.get_config_file()
    assert len(config["settings"]["recent_files"]) == 0

    # update config file
    config["settings"]["recent_files"].append(str(Path.home()))
    assert len(config["settings"]["recent_files"]) == 1
    main.update_config_file(config)
    config = main.get_config_file()
    assert os.path.exists(ini_path)
    assert len(config["settings"]["recent_files"]) == 1
    assert config["settings"]["recent_files"][0] == str(Path.home())


def test_204_03_menus_enabled(filesystem, qtbot):
    source = filesystem
    main = MainWindow(source / ".config")
    qtbot.addWidget(main)
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


def test_204_04_open_database(filesystem, qtbot):
    main, source, db_file_path = set_environment(filesystem, qtbot)

    # no current or previous db files available
    # file menu should be enabled, all other menus disabled
    dbref = main.open_database()
    assert isinstance(dbref, Dbal)
    assert not main.form.menu_assembly_listing.isEnabled()
    assert not main.form.menu_parts.isEnabled()
    assert not main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    dbref.sql_close()

    # Create a file; all menus should be enabled
    config = main.get_config_file()
    config["settings"]["recent_files"].insert(0, os.path.join(db_file_path, "test.db"))
    main.update_config_file(config)
    dbref = main.open_database()
    assert isinstance(dbref, Dbal)
    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.form.menu_parts.isEnabled()
    assert main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()


def test_204_05_set_files_menu(filesystem, qtbot):
    main, source, db_file_path = set_environment(filesystem, qtbot)

    # recent_files setting is empty, files.recent files should be disabled.
    main.set_recent_files_menu()
    assert not main.form.menu_file_recent.isEnabled()

    # add files to settings.recent_files. menu should reflect files
    config = main.get_config_file()
    config["settings"]["recent_files"].append(str(db_file_path) + "/test_file1.db")
    config["settings"]["recent_files"].append(str(db_file_path) + "/test_file2.db")
    main.update_config_file(config)
    main.set_recent_files_menu()

    assert main.form.menu_file_recent.isEnabled()
    menu_actions = main.form.menu_file_recent.actions()
    for i in range(0, len(config["settings"]["recent_files"])):
        assert menu_actions[i].isVisible()
        assert menu_actions[i].text() == os.path.basename(
            config["settings"]["recent_files"][i]
        )
        i += 1
    while i < len(menu_actions):
        assert not menu_actions[i].isVisible()
        i += 1


def test_204_06_configure_window(filesystem, qtbot):
    main, source, db_file_path = set_environment(filesystem, qtbot)

    # Add files to settings.recent_files.
    config = main.get_config_file()
    config["settings"]["recent_files"].append(str(db_file_path) + "/test_file1.db")
    config["settings"]["recent_files"].append(str(db_file_path) + "/test_file2.db")
    main.update_config_file(config)

    # configure the main window,files.recent_files should be enabled and
    # the display pages shoud be initialized.
    main.configure_window()
    assert main.form.menu_file_recent.isEnabled()
    #    assert isinstance(main.assembly_tree, AssemblyTreePage)
    #    assert isinstance(main.part_list, PartsListPage)
    #    assert isinstance(main.order_list, OrdersListPage)
    assert main.form.tab_widget.currentIndex() == 0


def test_204_07_get_existing_filename(filesystem, qtbot):
    #    source = filesystem
    #    config_dir = os.path.join(source, directories[0])
    #    db_file_path = os.path.join(source, directories[2])
    #    main = MainWindow(config_dir)
    #    qtbot.addWidget(main)
    #    config_file = build_test_config(source)
    #    main.update_config_file(config_file)
    #    value = main.get_existing_filename()
    #    assert value
    assert 1  # requires manual input


def test_204_08_get_new_filename(filesystem, qtbot):
    #    source = filesystem
    #    config_dir = os.path.join(source, directories[0])
    #    db_file_path = os.path.join(source, directories[2])
    #    main = MainWindow(config_dir)
    #    qtbot.addWidget(main)
    #    config_file = build_test_config(source)
    #    main.update_config_file(config_file)
    #    value = main.get_new_filename()
    #    assert value
    assert 1  # requires manual input


def test_204_09_load_file(filesystem, qtbot):
    main, source, db_file_path = set_environment(filesystem, qtbot)

    db_file0_path = str(source / "Documents/parts_tracker/test_file1.db")
    db_file1_path = str(source / "Documents/parts_tracker/test_file2.db")
    db_file2_path = str(source / "Documents/parts_tracker/test_file3.db")
    db_file3_path = str(source / "Documents/parts_tracker/test_file4.db")
    db_file4_path = str(source / "Documents/parts_tracker/test_file5.db")

    # load an initial file, number of recent files = 1
    main.load_file(db_file0_path)
    assert main.form.menu_assembly_listing.isEnabled()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 1
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file0_path)
    assert main.current_db_file == db_file0_path

    # Load more files, the len of recent_files never seceeds 4 and
    #   the last loaded file is always first entry.
    main.load_file(db_file1_path)
    assert len(main.get_config_file()["settings"]["recent_files"]) == 2
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file1_path)
    assert main.get_config_file()["settings"]["recent_files"][1] == str(db_file0_path)
    assert main.current_db_file == db_file1_path

    main.load_file(db_file2_path)
    main.load_file(db_file3_path)
    assert len(main.get_config_file()["settings"]["recent_files"]) == 4
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file3_path)
    assert main.get_config_file()["settings"]["recent_files"][1] == str(db_file2_path)
    assert main.get_config_file()["settings"]["recent_files"][2] == str(db_file1_path)
    assert main.get_config_file()["settings"]["recent_files"][3] == str(db_file0_path)

    main.load_file(db_file0_path)
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file0_path)
    assert main.get_config_file()["settings"]["recent_files"][1] == str(db_file3_path)
    assert main.get_config_file()["settings"]["recent_files"][2] == str(db_file2_path)
    assert main.get_config_file()["settings"]["recent_files"][3] == str(db_file1_path)

    main.load_file(db_file4_path)
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file4_path)
    assert main.get_config_file()["settings"]["recent_files"][1] == str(db_file0_path)
    assert main.get_config_file()["settings"]["recent_files"][2] == str(db_file3_path)
    assert main.get_config_file()["settings"]["recent_files"][3] == str(db_file2_path)

    main.load_file(db_file3_path)
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file3_path)
    assert main.get_config_file()["settings"]["recent_files"][1] == str(db_file4_path)
    assert main.get_config_file()["settings"]["recent_files"][2] == str(db_file0_path)
    assert main.get_config_file()["settings"]["recent_files"][3] == str(db_file2_path)


def test_204_10_file_open_action(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)
    file_path = source / "Documents/parts_tracker/test_file1.db"

    mocker.patch.object(MainWindow, "get_existing_filename")
    main.get_existing_filename.return_value = str(file_path)
    assert len(main.config["settings"]["recent_files"]) == 0
    main.file_open_action()
    assert len(main.config["settings"]["recent_files"]) == 1
    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.config["settings"]["recent_files"][0] == str(file_path)
    assert main.current_db_file == str(file_path)

    config_file = main.get_config_file()
    config_file["settings"]["recent_files"] = []
    main.update_config_file(config_file)
    config_file = build_test_config(source)
    main.update_config_file(config_file)
    file_path = source / "Documents/parts_tracker/test_file1.db"
    main.form.action_file_open.trigger()
    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.config["settings"]["recent_files"][0] == str(file_path)


def test_204_11_action_file_open(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)
    file_path = source / "Documents/parts_tracker/test_file1.db"

    mocker.patch.object(MainWindow, "get_existing_filename")
    main.get_existing_filename.return_value = str(file_path)
    assert len(main.config["settings"]["recent_files"]) == 0
    main.form.action_file_open.trigger()
    assert len(main.config["settings"]["recent_files"]) == 1
    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.config["settings"]["recent_files"][0] == str(file_path)


def test_204_12_file_close_action(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)
    file_path = source / "Documents/parts_tracker/test_file1.db"

    mocker.patch.object(MainWindow, "get_existing_filename")
    main.get_existing_filename.return_value = str(file_path)
    assert len(main.config["settings"]["recent_files"]) == 0
    main.file_open_action()
    assert len(main.config["settings"]["recent_files"]) == 1
    assert main.dbref.sql_is_connected()
    main.file_close_action()
    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.config["settings"]["recent_files"][0] == str(file_path)
    assert not main.dbref.sql_is_connected()
    assert not main.form.menu_assembly_listing.isEnabled()
    assert not main.form.menu_parts.isEnabled()
    assert not main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()


def test_204_13_action_file_close(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)
    file_path = source / "Documents/parts_tracker/test_file1.db"

    mocker.patch.object(MainWindow, "get_existing_filename")
    main.get_existing_filename.return_value = str(file_path)
    assert len(main.config["settings"]["recent_files"]) == 0
    main.form.action_file_open.trigger()
    assert len(main.config["settings"]["recent_files"]) == 1
    assert main.dbref.sql_is_connected()
    main.file_close_action()
    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.config["settings"]["recent_files"][0] == str(file_path)
    assert not main.dbref.sql_is_connected()
    assert not main.form.menu_assembly_listing.isEnabled()
    assert not main.form.menu_parts.isEnabled()
    assert not main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()


def test_204_14_file_new_action(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)
    file_path = source / "Documents/parts_tracker/test_file1.db"

    mocker.patch.object(MainWindow, "get_new_filename")
    main.get_new_filename.return_value = str(file_path)
    assert len(main.config["settings"]["recent_files"]) == 0
    main.file_new_action()
    assert len(main.config["settings"]["recent_files"]) == 1
    assert main.dbref.sql_is_connected()
    assert len(main.config["settings"]["recent_files"]) == 1
    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.config["settings"]["recent_files"][0] == str(file_path)


def test_204_15_action_file_new(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)
    file_path = source / "Documents/parts_tracker/test_file1.db"

    mocker.patch.object(MainWindow, "get_new_filename")
    main.get_new_filename.return_value = str(file_path)
    assert len(main.config["settings"]["recent_files"]) == 0
    main.form.action_file_new.trigger()
    assert len(main.config["settings"]["recent_files"]) == 1
    assert main.dbref.sql_is_connected()
    assert len(main.config["settings"]["recent_files"]) == 1
    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.config["settings"]["recent_files"][0] == str(file_path)


def test_204_16_recent_file_1_action(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)

    db_file0_path = str(source / "Documents/parts_tracker/test_file1.db")
    db_file1_path = str(source / "Documents/parts_tracker/test_file2.db")
    db_file2_path = str(source / "Documents/parts_tracker/test_file3.db")
    db_file3_path = str(source / "Documents/parts_tracker/test_file4.db")
    db_file4_path = str(source / "Documents/parts_tracker/test_file5.db")

    main.recent_file_1_action()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 0
    assert not main.form.menu_file_recent.isEnabled()

    main.load_file(db_file0_path)
    main.file_close_action()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 1
    assert main.form.menu_file_recent.isEnabled()
    assert main.current_db_file == ""

    main.recent_file_1_action()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 1
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.form.menu_parts.isEnabled()
    assert main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    assert main.current_db_file == db_file0_path


def test_204_17_action_recent_file_1(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)

    db_file0_path = str(source / "Documents/parts_tracker/test_file1.db")
    db_file1_path = str(source / "Documents/parts_tracker/test_file2.db")
    db_file2_path = str(source / "Documents/parts_tracker/test_file3.db")
    db_file3_path = str(source / "Documents/parts_tracker/test_file4.db")
    db_file4_path = str(source / "Documents/parts_tracker/test_file5.db")

    main.action_recent_file_1.trigger()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 0
    assert not main.form.menu_file_recent.isEnabled()

    main.load_file(db_file0_path)
    main.file_close_action()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 1
    assert main.form.menu_file_recent.isEnabled()
    assert main.current_db_file == ""

    main.action_recent_file_1.trigger()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 1
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.form.menu_parts.isEnabled()
    assert main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    assert main.current_db_file == db_file0_path


def test_204_18_recent_file_2_action(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)

    db_file0_path = str(source / "Documents/parts_tracker/test_file1.db")
    db_file1_path = str(source / "Documents/parts_tracker/test_file2.db")
    db_file2_path = str(source / "Documents/parts_tracker/test_file3.db")
    db_file3_path = str(source / "Documents/parts_tracker/test_file4.db")
    db_file4_path = str(source / "Documents/parts_tracker/test_file5.db")

    main.recent_file_2_action()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 0
    assert not main.form.menu_file_recent.isEnabled()

    main.load_file(db_file0_path)
    main.file_close_action()
    main.load_file(db_file1_path)
    main.file_close_action()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 2
    assert main.form.menu_file_recent.isEnabled()
    assert main.current_db_file == ""
    assert main.get_config_file()["settings"]["recent_files"][0] == db_file1_path
    assert main.get_config_file()["settings"]["recent_files"][1] == db_file0_path

    main.recent_file_2_action()
    assert main.current_db_file == db_file0_path
    assert len(main.get_config_file()["settings"]["recent_files"]) == 2
    assert main.get_config_file()["settings"]["recent_files"][1] == db_file1_path
    assert main.get_config_file()["settings"]["recent_files"][0] == db_file0_path


def test_204_19_action_recent_file_2(qtbot, filesystem, mocker):
    main, source, db_file_path = set_environment(filesystem, qtbot)

    db_file0_path = str(source / "Documents/parts_tracker/test_file1.db")
    db_file1_path = str(source / "Documents/parts_tracker/test_file2.db")
    db_file2_path = str(source / "Documents/parts_tracker/test_file3.db")
    db_file3_path = str(source / "Documents/parts_tracker/test_file4.db")
    db_file4_path = str(source / "Documents/parts_tracker/test_file5.db")

    main.action_recent_file_2.trigger()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 0
    assert not main.form.menu_file_recent.isEnabled()

    main.load_file(db_file0_path)
    main.file_close_action()
    main.load_file(db_file1_path)
    main.file_close_action()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 2
    assert main.form.menu_file_recent.isEnabled()
    assert main.current_db_file == ""
    assert main.get_config_file()["settings"]["recent_files"][0] == db_file1_path
    assert main.get_config_file()["settings"]["recent_files"][1] == db_file0_path

    main.action_recent_file_2.trigger()
    assert main.current_db_file == db_file0_path
    assert len(main.get_config_file()["settings"]["recent_files"]) == 2
    assert main.get_config_file()["settings"]["recent_files"][1] == db_file1_path
    assert main.get_config_file()["settings"]["recent_files"][0] == db_file0_path


# def test_204_07_exit_app_action(qtbot, filesystem):
#    # set up new test filesystem
#    source = filesystem
#    config_dir = source / ".config"
#    db_file_path = Path(source / "Documents/parts_tracker/")
#    main = MainWindow(config_dir)
#    qtbot.addWidget(main)
#    config = main.get_config_file()
#    config["settings"]["recent_files"].append(str(db_file_path) + "/test_file1.db")
#    db_path = db_file_path / "test_file1.db"
#    db_path.open(mode="r")
#    main.config = config
#    main.dbref = main.open_database()
#    assert isinstance(main.dbref, Dbal)
#    assert main.dbref.sql_is_connected()
#
#    main.config["settings"]["recent_files"].append(str(db_file_path) + "/test_file2.db")
#    main.exit_app_action()
#    assert not main.dbref.sql_is_connected()
#    assert len(main.config["settings"]["recent_files"]) == 2
#
