"""
Test the MainWindow class.

File:       test_04_main_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys
from pathlib import Path

import mock
import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from file_system import filesystem, test_config
from lbk_library import Dbal
from PyQt6.QtWidgets import QApplication, QMainWindow
from pytestqt import qtbot
from pytestqt.qt_compat import qt_api

from pages import AssemblyTreePage, MainWindow, OrdersListPage, PartsListPage


def test_04_01_class_type(qtbot):
    with mock.patch.object(QApplication, "aboutToQuit"):
        main = MainWindow(qtbot)
        qtbot.addWidget(main)
        assert isinstance(main, MainWindow)
        assert isinstance(main, QMainWindow)


def test_04_02_get_set_config_file(qtbot, filesystem):
    source = filesystem
    config_dir = source / ".config"
    main = MainWindow(qtbot, config_dir)
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


def test_04_03_menus_enabled(qtbot):
    main = MainWindow(qtbot)
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


def test_04_04_open_database(qtbot, filesystem):
    source = filesystem
    config_dir = source / ".config"
    main = MainWindow(qtbot, config_dir)
    qtbot.addWidget(main)
    # set up new test filesystem
    db_file_path = source / "Documents/parts_tracker/"

    dbref = main.open_database()
    assert isinstance(dbref, Dbal)
    assert not main.form.menu_assembly_listing.isEnabled()
    assert not main.form.menu_parts.isEnabled()
    assert not main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()
    dbref.sql_close()

    main.config["settings"]["recent_files"].insert(0, db_file_path / "test.db")
    dbref = main.open_database()
    assert isinstance(dbref, Dbal)
    assert Path.is_file(main.config["settings"]["recent_files"][0])
    assert main.form.menu_assembly_listing.isEnabled()
    assert main.form.menu_parts.isEnabled()
    assert main.form.menu_orders.isEnabled()
    assert main.form.menu_file.isEnabled()


def test_04_05_set_files_menu(qtbot, filesystem):
    source = filesystem
    config_dir = source / ".config"
    main = MainWindow(qtbot, config_dir)
    qtbot.addWidget(main)
    # set up new test filesystem
    db_file_path = source / "Documents/parts_tracker/"

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


def test_04_06_configure_window(qtbot, filesystem):
    source = filesystem
    config_dir = source / ".config"
    main = MainWindow(qtbot, config_dir)
    qtbot.addWidget(main)
    # set up new test filesystem
    db_file_path = source / "Documents/parts_tracker/"

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

    assert isinstance(main.assembly_tree, AssemblyTreePage)
    assert isinstance(main.part_list, PartsListPage)
    assert isinstance(main.order_list, OrdersListPage)
    main.form.tab_widget.currentIndex() == 0


def test_p04_07_exit(qtbot, filesystem, monkeypatch):
    # set up new test filesystem
    source = filesystem
    config_dir = source / ".config"
    main = MainWindow(qtbot, config_dir)
    qtbot.addWidget(main)
    db_file_path = source / "Documents/parts_tracker/"

    main.form.close()
