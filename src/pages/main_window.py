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
from lbk_library.gui.dialog import Dialog

from PyQt6.QtWidgets import QFileDialog, QMainWindow
from PyQt6 import uic

from dialogs import ItemDialog

from . import AssemblyTreePage
# from . import OrdersListPage
# from . import PartsListPage
from . import table_definition


class MainWindow(QMainWindow):
    """Build the Main Window for the Parts Tracker Program."""

    def __init__(self, test_config_dir: str = None) -> None:
        """
        Initialize the main window for the Program.

        Parameters:
            test_config_dir (str): dir for the config file for testing
                purposes only; not used for normal running.
        """
        super().__init__()
        self.assembly_tree: AssemblyTreePage

        # TODO Change this to use QSettings object
        self.config_handler = IniFileParser(
            "parts_tracker.ini", "parts_tracker", test_config_dir
        )
        self.config = self.get_config_file()
        self.form = uic.loadUi("src/forms/main_window.ui", self)
        self.current_db_file = ""
        self.dbref = self.open_database()

        self.configure_window()

        # set the actions for the main gui

        #  -- File Menu Items --
        self.form.action_file_open.triggered.connect(self.file_open_action)
        self.form.action_file_close.triggered.connect(self.file_close_action)
        self.form.action_file_new.triggered.connect(self.file_new_action)

        self.form.action_recent_file_1.triggered.connect(self.recent_file_1_action)
        self.form.action_recent_file_2.triggered.connect(self.recent_file_2_action)
        self.form.action_recent_file_3.triggered.connect(self.recent_file_3_action)
        self.form.action_recent_file_4.triggered.connect(self.recent_file_4_action)

        self.form.action_file_exit.triggered.connect(self.close)

        # -- Assemblies/Items Menu Actions --
        self.form.action_new_item.triggered.connect(
            lambda: self.item_dialog_action(None, Dialog.ADD_ELEMENT)
        )
        self.form.action_edit_item.triggered.connect(lambda: self.item_dialog_action(None, Dialog.EDIT_ELEMENT))
        #
        # self.form.action_edit_assembly_tree.triggered.connect(self.edit_assembly_tree_action)
        # self.form.action_save_assembly_list.triggered.connect(self.save_assembly_list_action)
        # self.form.action_update_assemby_tree.triggered.connect(self.update_assembly_tree_action)
        #
        #     # Parts Menu Actions
        # self.form.action_new_part.triggered.connect(lambda: self.part_dialog_action(None, ADD_ELEMENT))
        # self.form.action_edit_part.triggered.connect(lambda: self.part_dialog_action(None, EDIT_ELEMENT))
        # self.form.action_change_part_number.triggered.connect(self.part_change_pn_dialog_action)
        # self.form.action_update_part_list_table.triggered.connect(self.update_part_list_table_action)
        #
        #     # Orders Menu Actions
        # self.form.action_new_order.triggered.connect(lambda: self.order_dialog_action(None, ADD_ELEMENT))
        # self.form.action_edit_order.triggered.connect(lambda: self.order_dialog_action(None, EDIT_ELEMENT))
        # self.form.action_update_order_table.triggered.connect(lambda: (self.order_list.update_table()))

        # show the window
        self.show()

    # TODO Change this to use QSettings object
    def get_config_file(self) -> dict[str, Any]:
        """
        Get the stored configuration.

        The minimal config dict structure is:
        {
            'settings': {
                'recent_files': (list)  is the set of recent files
                    opened, most recent first, as full paths.
                'db_file_dir': (str) Where to store the parts database,
                    defaults to the directory
                    "{user documents directory}/PartsTracker"
                'xls_file_dir': (str) where to store the 'csv'/'xlxs'
                    parts listings,  defaults to the directory
                    "{user documents directory}/PartsTracker/parts_listings"
            }
        }

        Returns:
            (dict) The new configuration file.
        """
        config = self.config_handler.read_config()
        if not config:
            # define default configuration file
            config = {
                "settings": {
                    "recent_files": [],
                    "db_file_dir": str(
                        os.path.join(Path.home(), "Documents/PartsTracker")
                    ),
                    "xls_file_dir": str(
                        os.path.join(
                            Path.home(), "Documents/PartsTracker/parts_listings"
                        )
                    ),
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
            self.current_db_file = self.config["settings"]["recent_files"][0]
            dbref.sql_connect(self.current_db_file)
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
        # self.part_list = PartsListPage(self.form, self.dbref)
        # self.order_list = OrdersListPage(self.form, self.dbref)
        # self.form.tab_widget.setCurrentIndex(0)

    def set_recent_files_menu(self) -> None:
        """
        Update the Recent Files menu.

        Show up to 4 recently opened files as listed in the
        config['settings']['recent_files'] variable. If less than 4 files are held, hide
        remaining menu actions.
        """
        menu_actions = self.form.menu_file_recent.actions()
        i = 0
        # set the recent files that are known
        i = 0
        for filename in self.config["settings"]["recent_files"]:
            menu_actions[i].setText(os.path.basename(filename))
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

    def get_existing_filename(self) -> str:
        """Make testing file_open_action easier."""
        filename_set = QFileDialog.getOpenFileName(
            None,
            "New File",
            self.config["settings"]["db_file_dir"],
            "Parts Files (*.db)",
        )
        return filename_set[0]

    def get_new_filename(self) -> str:
        """Make testing file_new_action easier."""
        filename_set = QFileDialog.getSaveFileName(
            None,
            "New File",
            self.config["settings"]["db_file_dir"],
            "Parts Files (*.db)",
        )
        return filename_set[0]

    def load_file(self, filepath: str) -> None:
        """
        Build and display a new, empty database file.

        Parameters:
            filepath (String): An absolute path to file to open
        """
        # if file is already on the list, remove it
        if self.config["settings"]["recent_files"]:
            for i in range(len(self.config["settings"]["recent_files"])):
                if self.config["settings"]["recent_files"][i] == filepath:
                    del self.config["settings"]["recent_files"][i]
                    break

        # add to beginning of list
        self.config["settings"]["recent_files"].insert(0, filepath)
        self.current_db_file = self.config["settings"]["recent_files"][0]
        # drop 5th entry if exists
        if len(self.config["settings"]["recent_files"]) > 4:
            del self.config["settings"]["recent_files"][4]

        self.save_config_file(self.config)
        self.set_recent_files_menu()

        # close the old parts file and open the new
        if self.dbref.sql_is_connected():  # if open, close it
            self.dbref.sql_close()

        self.dbref.sql_connect(filepath)

        # update the window
        if self.dbref.sql_is_connected():
            self.set_menus_enabled(True)

            self.assembly_tree.update_tree()
            # self.part_list.update_table()
            # self.order_list.update_table()
            # self.form.tab_widget.setCurrentIndex(0)

    def file_open_action(self) -> None:
        """
        Open a Parts file.

        Open a parts file, add the file to the recent files list, and
        update the display with the the new dataset.
        """
        filepath = self.get_existing_filename()
        self.load_file(filepath)

    def file_close_action(self) -> None:
        """Close the current database file."""
        # if a file is open, then close it
        if self.dbref.sql_is_connected():
            self.dbref.sql_close()
        self.current_db_file = ""
        self.set_menus_enabled(False)
        self.save_config_file(self.config)

        # update the display
        self.assembly_tree.clear_tree()
        # self.part_list.clear_table()
        # self.order_list.clear_table()
        self.form.tab_widget.setCurrentIndex(0)

    def file_new_action(self) -> None:
        """
        Create and load a new PartsTracker File.

        The database is created with new, empty tables. The file already
        exists, it is deleted first, then recreated.
        """
        file_name = self.get_new_filename()
        if Path(file_name).is_file():
            os.remove(file_name)
        new_file = Dbal.new_file(file_name, table_definition)
        self.load_file(file_name)

    def recent_file_1_action(self) -> None:
        """Open the first most recent file."""
        if (
            self.config["settings"]["recent_files"]
            and len(self.config["settings"]["recent_files"]) > 0
        ):
            self.load_file(self.config["settings"]["recent_files"][0])

    def recent_file_2_action(self) -> None:
        """Open the second most recent file."""
        if (
            self.config["settings"]["recent_files"]
            and len(self.config["settings"]["recent_files"]) > 1
        ):
            self.load_file(self.config["settings"]["recent_files"][1])

    def recent_file_3_action(self) -> None:
        """Open the third most recent file."""
        if (
            self.config["settings"]["recent_files"]
            and len(self.config["settings"]["recent_files"]) > 2
        ):
            self.load_file(self.config["settings"]["recent_files"][2])

    def recent_file_4_action(self) -> None:
        """Open the fourth most recent file."""
        if (
            self.config["settings"]["recent_files"]
            and len(self.config["settings"]["recent_files"]) > 3
        ):
            self.load_file(self.config["settings"]["recent_files"][3])

    def exit_app_action(self) -> None:
        """Save the config file, close database, then Exit."""
        pass

    # self.config_handler.write_config(self.config)
    # if self.dbref.sql_is_connected():
    #     self.dbref.sql_close()
    #     self.current_db_file = ""

    def item_dialog_action(self, entry_index: int, add_item: int) -> None:
        """
        Activate the Item Editing form.

        Parameters:
            record_id (int): the index into the database for the item to
                be edited, default is None.
            add_item (int): The constant Dialog.ADD_ELEMENT if a new item is
                to be aded, Dialog.EDIT_ELEMENT for editing an existing item.
        """
        ItemDialog(self, self.dbref, entry_index, Dialog.ADD_ELEMENT).exec()
        # self.assembly_tree.update_tree()

    #    def edit_assembly_tree_action(self) -> None:
    #        """Revise the assembly structure of the tree."""
    #        print('calling edit sturcture dialog')
    #        EditStructureDialog(self, self.dbref, self.update_assembly_tree_action).exec()
    #
    #    def save_assembly_list_action(self) -> None:
    #        """Save list of items (assembly order) to csv file or xlsx file."""
    #         SaveAssyListDialog(self, self.dbref, self.config).exec()
    #
    #    def update_assembly_tree_action(self) -> None:
    #        """Update the assembly tree display, showing collapsed view."""
    #        self.assembly_tree.update_tree()
    #
    #    def part_dialog_action(self, entry_index: int, add_part: int) -> None:
    #        """
    #        Activate the Part Editing form.
    #
    #        Parameters:
    #            parent (QMainWindow) the parent window owning this dialog.
    #            dbref (Dbal) reference to the database for this item.
    #            entry_index (integer) the index into the database for the
    #                part to be edited.
    #            add_part (int) The constant Dialog.ADD_ELEMENT if a new part
    #                is to be aded, Dialog.EDIT_ELEMENT for editing an
    #                existing part
    #        """
    #        PartDialog(self, self.dbref, entry_index, add_part).exec()
    #        self.part_list.update_table()
    #
    #
    #    #
    #    # Change a part number throughout the database.
    #    #
    #    # @param parent (QMainWindow) the parent window owning this dialog.
    #    # @param dbref (Dbal) reference to the database for this item.
    #    #
    #    def part_change_pn_dialog_action(self) -> None:
    #       ChangePartNumberDialog(self, self.dbref).exec()
    #       self.assembly_tree.update_tree()
    #       self.parts_list.update_table()
    #       self.order_list.update_table()


    #
    # Update the Parts list table after some change.
    #
    # @param dbref (Dbal) reference to the database for this item.
    #
    # def update_part_list_table_action(self, dbref):
    #     self.part_list.update_table()
    # end update_part_list_table_action()


    #
    # Activate the Order Editing form
    #
    # @param parent (QMainWindow) the parent window owning this dialog.
    # @param dbref (Dbal) reference to the database for this order.
    # @param resources (AppResources) reference to the app resources for this dialog.
    # @param entry_index (integer) the index into the database for the order to be
    #   edited, default is None
    # @param add_order (int) The constant Dialog.ADD_ELEMENT if a new order is
    #       to be aded, Dialog.EDIT_ELEMENT for editing an existing order
    #
    # def order_dialog_action(self, entry_index: int, add_order: int) -> None:
    #    OrderDialog(self, self.dbref, entry_index, add_order).exec()
    #    self.order_list.update_table()
    # end order_dialog_action()

# end
