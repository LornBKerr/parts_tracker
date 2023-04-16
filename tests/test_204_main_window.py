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
from PyQt6.QtWidgets import QMainWindow
from pytestqt import qtbot

# from pytestqt.qt_compat import qt_api

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import (
    build_test_config,
    db_create,
    db_open,
    directories,
    filesystem,
    test_config,
)

from pages import MainWindow  # AssemblyTreePage, , OrdersListPage, PartsListPage


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
    source = filesystem
    config_dir = os.path.join(source, directories[0])
    db_file_path = os.path.join(source, directories[2])
    main = MainWindow(config_dir)
    qtbot.addWidget(main)
    config_file = build_test_config(source)
    main.update_config_file(config_file)

    dbref = main.open_database()
    assert isinstance(dbref, Dbal)
    assert not main.form.menu_assembly_listing.isEnabled()
    assert not main.form.menu_parts.isEnabled()
    assert not main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    dbref.sql_close()

    main.config["settings"]["recent_files"].insert(
        0, os.path.join(db_file_path, "test.db")
    )
    main.update_config_file(config_file)
    dbref = main.open_database()
    assert isinstance(dbref, Dbal)

    assert os.path.isfile(main.config["settings"]["recent_files"][0])
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.form.menu_parts.isEnabled()
    assert main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()


def test_204_05_set_files_menu(filesystem, qtbot):
    source = filesystem
    config_dir = os.path.join(source, directories[0])
    db_file_path = os.path.join(source, directories[2])
    main = MainWindow(config_dir)
    qtbot.addWidget(main)
    config_file = build_test_config(source)
    main.update_config_file(config_file)

    main.set_recent_files_menu()
    assert not main.form.menu_file_recent.isEnabled()
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
    source = filesystem
    config_dir = os.path.join(source, directories[0])
    db_file_path = os.path.join(source, directories[2])
    main = MainWindow(config_dir)
    qtbot.addWidget(main)
    config_file = build_test_config(source)
    main.update_config_file(config_file)

    main.configure_window()
    assert not main.form.menu_file_recent.isEnabled()
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

    #    assert isinstance(main.assembly_tree, AssemblyTreePage)
    #    assert isinstance(main.part_list, PartsListPage)
    #    assert isinstance(main.order_list, OrdersListPage)
    main.form.tab_widget.currentIndex() == 0


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
    source = filesystem
    config_dir = os.path.join(source, directories[0])
    db_file_path = os.path.join(source, directories[2])
    main = MainWindow(config_dir)
    qtbot.addWidget(main)
    config_file = build_test_config(source)
    main.update_config_file(config_file)

    db_file0_path = str(source / "Documents/parts_tracker/test_file1.db")
    db_file1_path = str(source / "Documents/parts_tracker/test_file2.db")
    db_file2_path = str(source / "Documents/parts_tracker/test_file3.db")
    db_file3_path = str(source / "Documents/parts_tracker/test_file4.db")
    db_file4_path = str(source / "Documents/parts_tracker/test_file5.db")

    main.load_file(db_file0_path)
    assert main.form.menu_assembly_listing.isEnabled()
    assert len(main.get_config_file()["settings"]["recent_files"]) == 1
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file0_path)

    main.load_file(db_file1_path)
    assert len(main.get_config_file()["settings"]["recent_files"]) == 2
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file1_path)
    assert main.get_config_file()["settings"]["recent_files"][1] == str(db_file0_path)

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
    print(main.get_config_file()["settings"]["recent_files"])
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file4_path)
    assert main.get_config_file()["settings"]["recent_files"][1] == str(db_file0_path)
    assert main.get_config_file()["settings"]["recent_files"][2] == str(db_file3_path)
    assert main.get_config_file()["settings"]["recent_files"][3] == str(db_file2_path)

    main.load_file(db_file3_path)
    print(main.get_config_file()["settings"]["recent_files"])
    assert main.get_config_file()["settings"]["recent_files"][0] == str(db_file3_path)
    assert main.get_config_file()["settings"]["recent_files"][1] == str(db_file4_path)
    assert main.get_config_file()["settings"]["recent_files"][2] == str(db_file0_path)
    assert main.get_config_file()["settings"]["recent_files"][3] == str(db_file2_path)


# def test_204_07_exit_app_action(filesystem, qtbot):
#    source = filesystem
#    config_dir = os.path.join(source, directories[0])
#    db_file_path = os.path.join(source, directories[2])
#    main = MainWindow(config_dir)
#    qtbot.addWidget(main)
#    config_file = build_test_config(source)
#    config_file["settings"]["recent_files"].append(str(db_file_path) + "/test_file1.db")
#    main.update_config_file(config_file)
#
#    main.dbref = main.open_database()
#    assert isinstance(main.dbref, Dbal)
#    assert main.dbref.sql_is_connected()
#
#    main.config["settings"]["recent_files"].append(str(db_file_path) + "/test_file2.db")
#    main.exit_app_action()
#    assert not main.dbref.sql_is_connected()
#    assert len(main.config["settings"]["recent_files"]) == 2
#
#
# def test_p04_08_exit(qtbot, db_create):
#    pass
