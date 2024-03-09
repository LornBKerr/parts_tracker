"""
Build and execute the Main Window for the Parts Tracker Program.

File:       main_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

import os

from lbk_library import Dbal  # , IniFileParser

from PyQt5 import uic
from PyQt5.QtCore import QSettings  # QPoint,
from PyQt5.QtGui import QMoveEvent, QResizeEvent
from PyQt5.QtWidgets import QMainWindow  # QFileDialog,

# import re
# from pathlib import Path
# from typing import Any
# from lbk_library.gui import Dialog
# from .assembly_tree_page import AssemblyTreePage
# from .orders_list_page import OrdersListPage
# from .parts_list_page import PartsListPage
# from dialogs import (  # AssemblyListDialog, ChangePartNumberDialog, EditStructureDialog,OrderDialog, PartDialog, SaveAssyListDialog
#    ItemDialog,
# )
# from .parts_table_definition import table_definition


class MainWindow(QMainWindow):
    """Build the Main Window for the Parts Tracker Program."""

    def __init__(self) -> None:
        """Initialize the main window for the Program."""
        super().__init__()
        self.config = QSettings("Unnamed Branch", "Parts Tracker")
        self.dbref: Dbal = Dbal()
        self.recent_files: list[str] = []

        #        self.assembly_tree: AssemblyTreePage
        #        self.orders_list: OrdersListPage
        #        self.parts_list: PartsListPage
        #
        # set configuration
        if not len(self.config.allKeys()):
            self.initialize_config_file()

        self.form = uic.loadUi("src/forms/main_window.ui", self)
        self.current_db_file = ""
        self.dbref = self.open_database()

        #        self.configure_window()

        #        # set the actions for the main gui
        #
        #        #  -- File Menu Items --
        #        self.form.action_file_open.triggered.connect(self.file_open_action)
        #        self.form.action_file_close.triggered.connect(self.file_close_action)
        #
        #        self.form.action_file_new.triggered.connect(self.file_new_action)
        #        self.form.action_recent_file_1.triggered.connect(self.recent_file_1_action)
        #        self.form.action_recent_file_2.triggered.connect(self.recent_file_2_action)
        #        self.form.action_recent_file_3.triggered.connect(self.recent_file_3_action)
        #        self.form.action_recent_file_4.triggered.connect(self.recent_file_4_action)
        #
        #        self.form.action_file_exit.triggered.connect(self.close)
        #
        # -- Assemblies/Items Menu Actions --
        #        self.form.action_new_item.triggered.connect(
        #            lambda: self.item_dialog_action(None, Dialog.ADD_ELEMENT)
        #        )
        #        self.form.action_edit_item.triggered.connect(
        #            lambda: self.item_dialog_action(None, Dialog.EDIT_ELEMENT)
        #        )
        #        self.form.action_edit_assembly_tree.triggered.connect(
        #            self.edit_assembly_tree_action
        #        )
        #        self.form.action_save_assembly_list.triggered.connect(
        #            self.save_assembly_list_action
        #        )
        #        self.form.action_update_assemby_tree.triggered.connect(
        #            self.update_assembly_tree_action
        #        )
        #
        #        #     # Parts Menu Actions
        #        # self.form.action_new_part.triggered.connect(lambda: self.part_dialog_action(None, ADD_ELEMENT))
        #        # self.form.action_edit_part.triggered.connect(lambda: self.part_dialog_action(None, EDIT_ELEMENT))
        #        # self.form.action_change_part_number.triggered.connect(self.part_change_pn_dialog_action)
        #        # self.form.action_update_part_list_table.triggered.connect(self.update_part_list_table_action)
        #        #
        #        #     # Orders Menu Actions
        #        # self.form.action_new_order.triggered.connect(lambda: self.order_dialog_action(None, ADD_ELEMENT))
        #        # self.form.action_edit_order.triggered.connect(lambda: self.order_dialog_action(None, EDIT_ELEMENT))
        #        # self.form.action_update_order_table.triggered.connect(lambda: (self.order_list.update_table()))

        # show the window
        self.show()

    #    def save_config_file(self, config: dict[str, Any]) -> None:
    #        """
    #        Write the config file to storage.
    #
    #        Parameters:
    #            config (dict[str, Any]: The config file to save.
    #        """
    #        self.config_handler.write_config(config)
    #
    #    def update_config_file(self, config):
    #        """
    #        Allow child dialogs to update the config settings.
    #
    #        Parameters:
    #            config (dict): the updated config file.
    #        """
    #        self.config = config
    #        self.save_config_file(self.config)

    def configure_window(self):
        """
        Configure the displayed window.

        Set the location and size of the window from the saved
        configuration. Set the File menu list and fill the tabbed pages
        with data from the parts file if available.
        """

        # Set the geometry of the main window.
        self.move(self.config.value("geometry/x"), self.config.value("geometry/y"))
        self.resize(
            self.config.value("geometry/width"), self.config.value("geometry/height")
        )

        # Set the recent files list and "file.recent files" menu
        self.set_recent_files_list()
        self.set_recent_files_menu()

        # Load the display widgets
        # self.assembly_tree = AssemblyTreePage(self.form, self.dbref)
        # self.part_list = PartsListPage(self.form, self.dbref)
        # self.order_list = OrdersListPage(self.form, self.dbref)
        # self.form.tab_widget.setCurrentIndex(0)

    #    def get_existing_filename(self) -> str:
    #        """Make testing file_open_action easier."""
    #        filename_set = QFileDialog.getOpenFileName(
    #            None,
    #            "New File",
    #            self.config["settings"]["db_file_dir"],
    #            "Parts Files (*.parts)",
    #        )
    #        return filename_set[0]
    #
    #    def get_new_filename(self) -> str:
    #        """Make testing file_new_action easier."""
    #        filename_set = QFileDialog.getSaveFileName(
    #            None,
    #            "New File",
    #            self.config["settings"]["db_file_dir"],
    #            "Parts Files (*.parts)",
    #        )
    #        return filename_set[0]
    #
    #    def load_file(self, filepath: str) -> None:
    #        """
    #        Build and display a new, empty database file.
    #
    #        Parameters:
    #            filepath (String): An absolute path to file to open
    #        """
    #        # if filepath is empty, ignore it
    #        if len(filepath) == 0:
    #            return
    #
    #        # if file is already on the recent files list, move to beginning.
    #        if filepath in self.recent_files:
    #            self.recent_files.insert(
    #                0, self.recent_files.pop(self.recent_files.index(filepath))
    #            )
    #        else:
    #            self.recent_files.insert(0, filepath)
    #        self.set_recent_files_menu()
    #
    #        # close the old parts file and open the new
    #        if self.dbref.sql_is_connected():  # if open, close it
    #            self.dbref.sql_close()
    #
    #        self.dbref.sql_connect(filepath)
    #
    #        # update the window
    #        if self.dbref.sql_is_connected():
    #            self.set_menus_enabled(True)
    #
    #            self.assembly_tree.update_tree()
    #            self.part_list.update_table()
    #            self.order_list.update_table()
    #            self.form.tab_widget.setCurrentIndex(0)

    #    def file_open_action(self) -> None:
    #        """
    #        Open a Parts file.
    #
    #        Open a parts file, add the file to the recent files list, and
    #        update the display with the the new dataset.
    #        """
    #        # TODO Handle canceling file selection without a file selected.
    #        filepath = self.get_existing_filename()
    #        self.load_file(filepath)
    #
    #    def file_close_action(self) -> None:
    #        """Close the current database file."""
    #        # if a file is open, then close it
    #        if self.dbref.sql_is_connected():
    #            self.dbref.sql_close()
    #        self.current_db_file = ""
    #        self.set_menus_enabled(False)
    #        self.save_config_file(self.config)
    #
    #        # update the display
    #        self.assembly_tree.clear_tree()
    #        # self.part_list.clear_table()
    #        # self.order_list.clear_table()
    #        self.form.tab_widget.setCurrentIndex(0)
    #
    #    def file_new_action(self) -> None:
    #        """
    #        Create and load a new PartsTracker File.
    #
    #        The database is created with new, empty tables. The file already
    #        exists, it is deleted first, then recreated.
    #        """
    #        # TODO Handle canceling file selection without a file selected.
    #        file_name = self.get_new_filename()
    #        if Path(file_name).is_file():
    #            os.remove(file_name)
    #        new_file = Dbal.new_file(file_name, table_definition)
    #        self.load_file(file_name)
    #
    #    def recent_file_1_action(self) -> None:
    #        """Open the first most recent file."""
    #        if (
    #            self.config["settings"]["recent_files"]
    #            and len(self.config["settings"]["recent_files"]) > 0
    #        ):
    #            self.load_file(self.config["settings"]["recent_files"][0])
    #
    #    def recent_file_2_action(self) -> None:
    #        """Open the second most recent file."""
    #        if (
    #            self.config["settings"]["recent_files"]
    #            and len(self.config["settings"]["recent_files"]) > 1
    #        ):
    #            self.load_file(self.config["settings"]["recent_files"][1])
    #
    #    def recent_file_3_action(self) -> None:
    #        """Open the third most recent file."""
    #        if (
    #            self.config["settings"]["recent_files"]
    #            and len(self.config["settings"]["recent_files"]) > 2
    #        ):
    #            self.load_file(self.config["settings"]["recent_files"][2])
    #
    #    def recent_file_4_action(self) -> None:
    #        """Open the fourth most recent file."""
    #        if (
    #            self.config["settings"]["recent_files"]
    #            and len(self.config["settings"]["recent_files"]) > 3
    #        ):
    #            self.load_file(self.config["settings"]["recent_files"][3])
    #
    #   def item_dialog_action(self, entry_index: int, add_item: int) -> None:
    #        """
    #        Activate the Item Editing form.
    #
    #        Parameters:
    #            record_id (int): the index into the database for the item to
    #                be edited, default is None.
    #            add_item (int): The constant Dialog.ADD_ELEMENT if a new item is
    #                to be aded, Dialog.EDIT_ELEMENT for editing an existing item.
    #        """
    #        if entry_index == "":  # handle blank entry index (record_id)
    #            entry_index = -1
    #        ItemDialog(self, self.dbref, entry_index, add_item).exec()
    #        # self.assembly_tree.update_tree()
    #
    #
    #    def edit_assembly_tree_action(self) -> None:
    #        """Revise the assembly structure of the tree."""
    #        EditStructureDialog(self.dbref, self.assembly_tree.update_tree).exec()
    #
    #    def save_assembly_list_action(self) -> None:
    #        """Save list of items (assembly order) to csv file or xlsx file."""
    #        SaveAssyListDialog(self, self.dbref, self.config).exec()
    #
    #    def update_assembly_tree_action(self) -> None:
    #        """Update the assembly tree display, showing collapsed view."""
    #        self.assembly_tree.update_tree()
    #
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
    #    def part_change_pn_dialog_action(self) -> None:
    #        """
    #        Change a part number throughout the database.
    #
    #         Parameteres:
    #            parent (QMainWindow) the parent window owning this dialog.
    #            dbref (Dbal) reference to the database for this item.
    #        """
    #        ChangePartNumberDialog(self, self.dbref).exec()
    #        self.assembly_tree.update_tree()
    #        self.parts_list.update_table()
    #        self.order_list.update_table()
    #
    #    def update_part_list_table_action(self, dbref):
    #        """
    #        Update the Parts list table after some change.
    #
    #        Parameters:
    #            dbref (Dbal) reference to the database for this item.
    #        """
    #        self.part_list.update_table()
    #
    #    def order_dialog_action(self, entry_index: int, add_order: int) -> None:
    #        """
    #        Activate the Order Editing form
    #
    #        Parameters:
    #            parent (QMainWindow) the parent window owning this dialog.
    #            dbref (Dbal) reference to the database for this order.
    #            resources (AppResources) reference to the app resources for
    #               this dialog.
    #            entry_index (int) the index into the database for the order
    #                to be edited, default is None
    #            add_order (int) The constant Dialog.ADD_ELEMENT if a new
    #                order is to be aded, Dialog.EDIT_ELEMENT for editing
    #                an existing order.
    #        """
    #        OrderDialog(self, self.dbref, entry_index, add_order).exec()
    #        self.order_list.update_table()

    def moveEvent(self, move_event: QMoveEvent) -> None:
        """Update the window location when the main window is moved."""
        self.config.setValue("geometry/x", int(move_event.pos().x()))
        self.config.setValue("geometry/y", int(move_event.pos().y()))

    def resizeEvent(self, resize_event: QResizeEvent) -> None:
        """Update the window location when the main window is moved."""
        self.config.setValue("geometry/width", int(resize_event.size().width()))
        self.config.setValue("geometry/height", int(resize_event.size().height()))

        # TODO _Add resizing to tab widgets to match size of central widget.

    def initialize_config_file(self) -> None:
        """
        Set up a new stored configuration.

        The minimal config structure is:
            'settings': {
                'db_file_dir': (str) Where to store the parts database,
                    defaults to the directory
                    "{user documents directory}/PartsTracker"
                'list_files_dir': (str) where to store the 'csv'/'xlxs'
                    parts listings, defaults to the directory
                    "{user documents directory}/PartsTracker/parts_listings"
            },
            'recent_files': (list[str]) an empty list of recent files
                opened as full paths., The list will be limited to a max
                of 4 filenames as full paths with the mostly opened
                file first.,
            'Geometry': l(list[int])
                x: int - top_left_horizontal position, default is 0
                y: int - top_left_vertical position, default is 0
                width: int -  Width of window, default is 1250
                height: int - height of the window, default is 920
        """
        self.config.beginGroup("settings")
        self.config.setValue("db_file_dir", "Documents/PartsTracker")
        self.config.setValue("list_files_dir", "Documents/PartsTracker/parts_listings")

        self.config.endGroup()

        self.config.beginGroup("recent_files")  # 4 empty file names
        self.config.setValue("file0", "")
        self.config.setValue("file1", "")
        self.config.setValue("file2", "")
        self.config.setValue("file3", "")
        self.config.endGroup()

        self.config.beginGroup("geometry")
        self.config.setValue("x", 0)  # 'x': top of window
        self.config.setValue("y", 0)  # 'y': left side of window
        self.config.setValue("width", 1250)  # width of window
        self.config.setValue("height", 920)  # height of window
        self.config.endGroup()

        return self.config

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

    def open_database(self) -> Dbal:
        """
        Initialize the database object.

        If a recent file is available, open the most recently used
        database file. Otherwise, leave the connection closed

        Returns:
            (Dbal): The database reference
        """
        if not self.config.value("recent_files/file0") == "":
            # use first filename to open the parts file
            self.current_db_file = self.config.value("recent_files/file0")
            self.dbref.sql_connect(self.current_db_file)
            self.set_menus_enabled(True)
        else:
            self.set_menus_enabled(False)
        return self.dbref

    def exit_app_action(self) -> None:
        """Save the config file, close database, then Exit."""
        self.config.sync()
        if self.dbref.sql_is_connected():
            self.dbref.sql_close()

    def load_recent_files_list(self) -> None:
        """Set the recent_files list from the config file."""
        self.recent_files.clear()  # ensure the list is empty.

        self.config.beginGroup("recent_files")
        for key in self.config.childKeys():
            if len(self.config.value(key)):
                self.recent_files.append(self.config.value(key))
        self.config.endGroup()

    def set_recent_files_menu(self) -> None:
        """
        Update the Recent Files menu.

        Show up to 4 recently opened files as listed in self.recent_files
        variable. If less than 4 files are held, hide the remaining
        menu actions.
        """
        menu_actions = self.form.menu_file_recent.actions()

        i = 0
        # set the recent files that are known
        print(self.recent_files)
        if len(self.recent_files) > 0:
            while i < len(self.recent_files):
                menu_actions[i].setText(os.path.basename(self.recent_files[i]))
                menu_actions[i].setVisible(True)
                i += 1
        # hide remainder of file menu
        while i < len(menu_actions):
            menu_actions[i].setVisible(False)
            i += 1

        # If no recent files, disable menu item
        if not len(self.recent_files):
            self.form.menu_file_recent.setDisabled(True)
        else:
            self.form.menu_file_recent.setEnabled(True)



# end
