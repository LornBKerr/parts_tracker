"""
Build and execute the Main Window for the Parts Tracker Program.

File:       main_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

import os
import re
from pathlib import Path
from typing import Any

from lbk_library import Dbal, IniFileParser
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow  # , QFileDialog

from .assembly_tree_page import AssemblyTreePage
from .orders_list_page import OrdersListPage
from .parts_list_page import PartsListPage

# from dialogs import Dialog, ItemDialog


class MainWindow(QMainWindow):
    """Build the Main Window for the Parts Tracker Program."""

    def __init__(self, app: QApplication, test_config_dir: str = None) -> None:
        """
        Initialize the main window for the Program.

        Parameters:
            app (QApplication): the QApplication instance
            test_config_dir (str): dir for the config file for testing
                purposes only; not used for normal running.
        """
        super().__init__()

        self.__closing: bool = False  # Is the window closing event in process

        # the current configuration state
        self.config_handler = IniFileParser(
            "parts_tracker.ini", "parts_tracker", test_config_dir
        )
        self.config = self.get_config_file()

        # get the gui form displayed by the window
        self.form = uic.loadUi("src/forms/main_window.ui", self)

        # the current database handler
        self.dbref = self.open_database()

        # configure the window, loading parts information as available
        self.configure_window()

        # set the actions for the main gui

        # File Menu Items

        self.form.action_file_exit.triggered.connect(self.close)

        # show the window
        self.show()

    def get_config_file(self) -> dict[str, Any]:
        """
        Get the stored configuration.

        The minimal config dict structure is:
        {
            'state': {
                'recent_files': (list) the 4 most recent db files opened
                'xls_file_loc": (str) where to store the parts listings
            }
        }
        'FIlES' is the set of recent files opened, most recent first

        Returns:
            (dict) The new configuration file.
        """
        config = self.config_handler.read_config()
        if not config:
            # define default configuration file
            config = {
                "settings": {
                    "recent_files": [],  # 1 empty entry
                    "xls_file_loc": str(Path.home()),
                }
            }
        # convert any strings representing lists to lists
        for section in config:
            for option in config[section]:
                if isinstance(config[section][option], str) and re.match(
                    r"\[.*\]", config[section][option]
                ):
                    a_list = config[section][option][1:-1]
                    if len(a_list) == 0:  # empty list
                        config[section][option] = []
                    else:
                        a_list = a_list.replace("'", "")
                        a_list = a_list.replace(" ", "")
                        config[section][option] = a_list.split(",")
        return config

    def save_config_file(self, config: dict[str, Any]) -> None:
        """
        Write the config file to storage.

        Parameters:
            config (dict[str, Any]: The config file to save.
        """
        self.config_handler.write_config(config)

    def update_config_file(self, config):
        """
        Allow child dialogs to update the config settings.

        Parameters:
            config (dict): the updated config file.
        """
        self.config = config
        self.save_config_file(self.config)

    def open_database(self) -> Dbal:
        """
        Initialize the database object.

        If a recent file is available, open the most recently used
        database file. Otherwise, leave the connection closed

        Returns:
            (Dbal): The database reference
        """
        dbref = Dbal()
        if len(self.config["settings"]["recent_files"]):
            # use first filename to open the parts file
            dbref.sql_connect(self.config["settings"]["recent_files"][0])
            self.set_menus_enabled(True)
        else:
            self.set_menus_enabled(False)
        return dbref

    def configure_window(self):
        """
        Configure the displayed window.

        Set the File menu list and fill the tabbed
        pages with data from the parts file if available.

        TODO: Add resizing
        """
        self.set_recent_files_menu()

        # Load the display widgets
        self.assembly_tree = AssemblyTreePage(self.form, self.dbref)
        self.part_list = PartsListPage(self.form, self.dbref)
        self.order_list = OrdersListPage(self.form, self.dbref)
        self.form.tab_widget.setCurrentIndex(0)

    def set_recent_files_menu(self) -> None:
        """
        Update the Recent Files menu.

        Show up to 4 recently opened files as listed in the
        config['files'] variable. If less than 4 files are held, hide
        remaining menu actions.
        """
        menu_actions = self.form.menu_file_recent.actions()
        i = 0
        # set the recent files that are known
        for i in range(len(self.config["settings"]["recent_files"])):
            menu_actions[i].setText(
                os.path.basename(self.config["settings"]["recent_files"][i])
            )
            menu_actions[i].setVisible(True)
            i += 1

        # hide remainder of file menu
        while i < len(menu_actions):
            menu_actions[i].setVisible(False)
            i += 1

        # If no recent files, disable menu item
        if not self.config["settings"]["recent_files"]:
            self.form.menu_file_recent.setDisabled(True)
        else:
            self.form.menu_file_recent.setEnabled(True)

    def set_menus_enabled(self, menus_enabled: bool) -> None:
        """
        Enable or disable all menu except the Files menu.

        When no database is open, disable the menus since they have
        no function.

        Parameters:
            menus_enabled (Boolean) True if menus should be active,
                False if not
        """
        self.form.menu_assembly_listing.setEnabled(menus_enabled)
        self.form.menu_parts.setEnabled(menus_enabled)
        self.form.menu_orders.setEnabled(menus_enabled)

    def exit_app_action(self) -> None:
        """Save the config file, close database, then Exit."""
        self.config_handler.write_config(self.config)
        if self.dbref.sql_is_connected():
            self.dbref.sql_close()
