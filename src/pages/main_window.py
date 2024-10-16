"""
Build and execute the Main Window for the Parts Tracker Program.

File:       main_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.0
"""

import os
from pathlib import Path

from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog
from PyQt5 import uic
from PyQt5.QtCore import QSettings  # QPoint,
from PyQt5.QtGui import QMoveEvent, QResizeEvent
from PyQt5.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QTableWidget,
    QTabWidget,
    QTreeWidget,
)

from dialogs import (
    AssemblyListDialog,
    ChangePartNumberDialog,
    EditConditionsDialog,
    EditSourcesDialog,
    EditStructureDialog,
    ItemDialog,
    OrderDialog,
    PartDialog,
)

from .assembly_tree_page import AssemblyTreePage
from .orders_list_page import OrdersListPage
from .parts_file_definition import table_definition
from .parts_list_page import PartsListPage

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class MainWindow(QMainWindow):
    """Build the Main Window for the Parts Tracker Program."""

    def __init__(self) -> None:
        """Initialize the main window for the Program."""
        super().__init__()
        self.config = QSettings("Unnamed Branch", "PartsTracker")
        """The configuration setup."""
        self.parts_file: PartsFile = PartsFile()
        """The parts file of the set of parts information."""
        self.__number_recent_files = 4
        """ The number of recent files listed in the recent Files menu."""

        self.form = uic.loadUi("src/forms/main_window.ui", self)
        self.tab_widget: QTabWidget
        self.assembly_tree_widget: QTreeWidget = QTreeWidget()
        self.orders_list_widget: QTableWidget = QTableWidget()
        self.parts_list_widget: QTableWidget = QTableWidget()

        # set configuration
        if not len(self.config.allKeys()):
            self.initialize_config_file()

        # open the last used file if any.
        self.parts_file = self.open_file()

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
        self.form.action_edit_item.triggered.connect(
            lambda: self.item_dialog_action(None, Dialog.EDIT_ELEMENT)
        )
        self.form.action_edit_conditions.triggered.connect(self.edit_conditions_action)
        self.form.action_edit_assembly_tree.triggered.connect(
            self.edit_assembly_tree_action
        )
        self.form.action_save_assembly_list.triggered.connect(
            self.save_assembly_list_action
        )
        self.form.action_update_assemby_tree.triggered.connect(
            self.assembly_tree.update_tree
        )

        # -- Parts Menu Actions --
        self.form.action_new_part.triggered.connect(
            lambda: self.part_dialog_action(None, Dialog.ADD_ELEMENT)
        )
        self.form.action_edit_part.triggered.connect(
            lambda: self.part_dialog_action(None, Dialog.EDIT_ELEMENT)
        )
        self.form.action_update_sources.triggered.connect(self.update_sources_action)
        self.form.action_change_part_number.triggered.connect(
            self.part_change_pn_dialog_action
        )
        self.form.action_update_part_list_table.triggered.connect(
            self.part_list.update_table
        )

        # -- Orders Menu Actions --
        self.form.action_new_order.triggered.connect(
            lambda: self.order_dialog_action(None, Dialog.ADD_ELEMENT)
        )
        self.form.action_edit_order.triggered.connect(
            lambda: self.order_dialog_action(None, Dialog.EDIT_ELEMENT)
        )
        self.form.action_update_order_table.triggered.connect(
            lambda: (self.order_list.update_table())
        )
        self.show()

    def initialize_config_file(self) -> None:
        """
        Set up a new stored configuration.

         The minimal config structure is:
             'settings': {
                 'parts_file_dir': (str) Where to store the parts file,
                     defaults to the directory
                     "{user documents directory}/PartsTracker"
                 'list_files_dir': (str) where to store the 'csv'/'xlxs'
                     parts listings, defaults to the directory
                     "{user documents directory}/PartsTracker/parts_listings"
             },
             'recent_files': {set of 4 most recent files opened, from
                     newest to oldest as full paths. Initially set to
                     empty strings.
                 file1: (str) - Most recent or current file open(ed).
                 file2: (str) - next most recent file.
                 file3: (str) - 3rd most recent file.
                 file4: (str) - 4th most recent file opened.
             },
             'Geometry': l(list[int])
                 x: int - top_left_horizontal position, default is 0
                 y: int - top_left_vertical position, default is 0
                 width: int -  Width of window, default is 1250
                 height: int - height of the window, default is 920
        """
        self.config.beginGroup("settings")
        self.config.setValue("parts_file_dir", "Documents/PartsTracker/parts_files")
        self.config.setValue("list_files_dir", "Documents/PartsTracker/parts_listings")
        self.config.endGroup()

        self.config.beginGroup("recent_files")  # 4 empty file names
        self.config.setValue("file1", "")
        self.config.setValue("file2", "")
        self.config.setValue("file3", "")
        self.config.setValue("file4", "")
        self.config.endGroup()

        self.config.beginGroup("geometry")
        self.config.setValue("x", 0)  # 'x': top of window
        self.config.setValue("y", 0)  # 'y': left side of window
        self.config.setValue("width", 1250)  # width of window
        self.config.setValue("height", 920)  # height of window
        self.config.endGroup()

        return self.config

    def open_file(self) -> PartsFile:
        """
        Load the last used file.

        If a recent file is available, open the most recently used
        parts file. Otherwise, leave the connection closed

        Returns:
            (PartsFile): The parts file reference
        """
        if not self.config.value("recent_files/file1") == "":
            # use first filename to open the parts file
            self.parts_file.sql_connect(self.config.value("recent_files/file1"))
            self.set_menus_enabled(True)
        else:
            self.set_menus_enabled(False)
        return self.parts_file

    def configure_window(self):
        """
        Configure the displayed window.

        Set the location and size of the window from the saved
        configuration. Set the File menu list and fill the tabbed pages
        with data from the parts file if available.
        """
        # setup the tabbed panel
        self.set_tab_widgets()

        # Set the geometry of the main window.
        self.move(
            int(self.config.value("geometry/x")), int(self.config.value("geometry/y"))
        )
        self.resize(
            int(self.config.value("geometry/width")),
            int(self.config.value("geometry/height")),
        )

        # Set the "file->recent files" menu
        self.set_recent_files_menu()

        # Load the display widgets
        self.assembly_tree = AssemblyTreePage(
            self.assembly_tree_widget, self.parts_file
        )
        self.part_list = PartsListPage(self.parts_list_widget, self.parts_file)
        self.order_list = OrdersListPage(self.orders_list_widget, self.parts_file)
        self.tab_widget.setCurrentIndex(0)

    def set_recent_files_menu(self) -> None:
        """
        Update the Recent Files menu.

        Show up to 4 recently opened files as listed in recent_files
        variable. If less than 4 files are held, hide the remaining
        menu actions.
        """
        menu_actions = self.form.menu_file_recent.actions()

        i = 0
        # set the recent files that are known
        recent_files = self.get_recent_files_list()

        if len(recent_files) > 0:
            while i < len(recent_files) and i < 4:
                menu_actions[i].setText(os.path.basename(recent_files[i]))
                menu_actions[i].setVisible(True)
                i += 1
        # hide remainder of file menu
        while i < len(menu_actions):
            menu_actions[i].setVisible(False)
            i += 1

        # If no recent files, disable menu item
        if not len(recent_files):
            self.form.menu_file_recent.setDisabled(True)
        else:
            self.form.menu_file_recent.setEnabled(True)

    def set_menus_enabled(self, menus_enabled: bool) -> None:
        """
        Enable or disable all menu except the Files menu.

        When no parts file is open, disable the menus since they have
        no function.

        Parameters:
            menus_enabled (Boolean) True if menus should be active,
                False if not
        """
        self.form.menu_assembly_listing.setEnabled(menus_enabled)
        self.form.menu_parts.setEnabled(menus_enabled)
        self.form.menu_orders.setEnabled(menus_enabled)

    def get_existing_filename(self) -> str:
        """
        Get a file path using the QFileDialog..

        Returns:
            (str) the selected filepath.
        """
        file_name, type = QFileDialog.getOpenFileName(
            None,
            "Open a Parts file",
            self.config.value("settings/parts_file_dir"),
            "Parts Files (*.parts)",
        )
        return str(file_name)

    def get_new_filename(self) -> str:
        """Make testing file_new_action easier."""
        filename, type = QFileDialog.getSaveFileName(
            None,
            "Open a new Parts file",
            self.config.value("settings/parts_file_dir"),
            "Parts Files (*.parts)",
        )
        return str(filename)

    def load_file(self, filepath: str) -> None:
        """
        Build and display a new, empty parts file file.

        Parameters:
            filepath (String): An absolute path to file to open
        """
        # if filepath is empty, ignore it
        if len(str(filepath)) == 0:
            return

        # if file is already on the recent files list, move to beginning.
        recent_files = self.get_recent_files_list()
        if filepath in recent_files:
            recent_files.insert(0, recent_files.pop(recent_files.index(filepath)))
        else:
            recent_files.insert(0, filepath)
        self.save_recent_files_list(recent_files)
        self.set_recent_files_menu()

        # close the old parts file and open the new
        if self.parts_file.sql_is_connected():  # if open, close it
            self.parts_file.sql_close()

        self.parts_file.sql_connect(filepath)

        # update the window
        if self.parts_file.sql_is_connected():
            self.set_menus_enabled(True)
            self.assembly_tree.update_tree()
            self.part_list.update_table()
            self.order_list.update_table()
            self.form.tab_widget.setCurrentIndex(0)

    def file_open_action(self) -> None:
        """
        Open a Parts file.

        Open a parts file, add the file to the recent files list, and
        update the display with the the new dataset.
        """
        filepath = self.get_existing_filename()
        self.load_file(filepath)

    def file_close_action(self) -> None:
        """Close the current parts file file."""
        # if a file is open, then close it
        if self.parts_file.sql_is_connected():
            self.parts_file.sql_close()
        self.set_menus_enabled(False)

        # update the display
        self.assembly_tree.clear_tree()
        self.part_list.clear_table()
        self.order_list.clear_table()
        self.form.tab_widget.setCurrentIndex(0)

    def file_new_action(self) -> None:
        """
        Create and load a new PartsTracker File.

        The parts file is created with new, empty tables. The file already
        exists, it is deleted first, then recreated.
        """
        file_name = self.get_new_filename()
        if Path(file_name).is_file():
            os.remove(file_name)
        PartsFile.new_file(file_name, table_definition)
        self.load_file(file_name)

    def recent_file_1_action(self) -> None:
        """Open the first most recent file."""
        file_1 = self.config.value("recent_files/file1")
        if Path(file_1).is_file():
            self.load_file(file_1)

    def recent_file_2_action(self) -> None:
        """Open the second most recent file."""
        file_2 = self.config.value("recent_files/file2")
        if Path(file_2).is_file():
            self.load_file(file_2)

    def recent_file_3_action(self) -> None:
        """Open the third most recent file."""
        file_3 = self.config.value("recent_files/file3")
        if Path(file_3).is_file():
            self.load_file(file_3)

    def recent_file_4_action(self) -> None:
        """Open the fourth most recent file."""
        file_4 = self.config.value("recent_files/file4")
        if Path(file_4).is_file():
            self.load_file(file_4)

    def exit_app_action(self) -> None:
        """Save the config file, close parts file, then Exit."""
        self.config.sync()
        if self.parts_file.sql_is_connected():
            self.parts_file.sql_close()

    def item_dialog_action(self, record_id: int, add_item: int) -> None:
        """
        Activate the Item Editing form.

        Parameters:
            record_id (int): the index into the parts file for the item to
                be edited, default is None.
            add_item (int): The constant Dialog.Dialog.ADD_ELEMENT if a new item is
                to be aded, Dialog.Dialog.EDIT_ELEMENT for editing an existing item.

        Returns:
            (dialog) the opened ItemDialog object
        """
        if record_id == "":  # handle blank entry index (record_id)
            record_id = -1
        dialog = ItemDialog(self, self.parts_file, record_id, add_item)
        dialog.open()
        self.assembly_tree.update_tree()
        return dialog

    def edit_conditions_action(self) -> None:
        """
        Revise the set of conditions available for an Item.

        Returns:
            (dialog) the opened EditConditionDialog object
        """
        dialog = EditConditionsDialog(self.parts_file)
        dialog.open()
        return dialog

    def edit_assembly_tree_action(self) -> None:
        """
        Revise the assembly structure of the tree.

        Returns:
            (dialog) the opened EditStructureDialog object
        """
        dialog = EditStructureDialog(self.parts_file, self.assembly_tree.update_tree)
        dialog.open()
        return dialog

    def save_assembly_list_action(self) -> None:
        """
        Save list of items (assembly order) to csv file or xlsx file.

        The list will be saved to the file location given in the config
        file entry "settings/list_files_dir".

        Returns:
            (dialog) the opened AssemblyListDialog object
        """
        dialog = AssemblyListDialog(self, self.parts_file, self.config)
        dialog.open()
        return dialog

    def update_assembly_tree_action(self) -> None:
        """
        Update the assembly tree display, showing collapsed view.

        returns:
            dict[str, str] the set of items for the tree.
        """
        tree_items = self.assembly_tree.update_tree()
        return tree_items

    def part_dialog_action(self, record_id: int, add_part: int) -> None:
        """
         Activate the Part Editing form.

        Parameters:
             record_id (integer) the index into the parts file for the
                 part to be edited.
             add_part (int) The constant Dialog.Dialog.ADD_ELEMENT if a new part
                 is to be aded, Dialog.EDIT_ELEMENT for editing an
                 existing part

        Returns:
            (dialog) the opened PartDialog object
        """
        if record_id == "":  # handle blank entry index (record_id)
            record_id = -1
        dialog = PartDialog(self, self.parts_file, record_id, add_part)
        dialog.open()
        self.part_list.update_table()
        return dialog

    def update_sources_action(self):
        """
        Revise the set of part sources available for a Part.

        Returns:
            (dialog) the opened EditSourceDialog object
        """
        dialog = EditSourcesDialog(self.parts_file)
        dialog.open()
        return dialog

    def part_change_pn_dialog_action(self) -> None:
        """
        Change a part number throughout the parts file.

         Parameters:
            parent (QMainWindow) the parent window owning this dialog.
        """
        dialog = ChangePartNumberDialog(self, self.parts_file)
        dialog.open()
        self.assembly_tree.update_tree()
        self.part_list.update_table()
        self.order_list.update_table()
        return dialog

    def order_dialog_action(self, record_id: int, add_order: int) -> None:
        """
        Activate the Order Editing form.

        Parameters:
            record_id (int) the index into the parts file for the order
                to be edited, default is None
            add_order (int) The constant Dialog.Dialog.ADD_ELEMENT if a new
                order is to be aded, Dialog.EDIT_ELEMENT for editing
                an existing order.
        """
        dialog = OrderDialog(self, self.parts_file, record_id, add_order)
        dialog.open()
        self.order_list.update_table()
        return dialog

    def moveEvent(self, move_event: QMoveEvent) -> None:
        """Update the window location when the main window is moved."""
        self.config.setValue("geometry/x", int(move_event.pos().x()))
        self.config.setValue("geometry/y", int(move_event.pos().y()))

    def resizeEvent(self, resize_event: QResizeEvent) -> None:
        """Update the window location when the main window is moved."""
        self.config.setValue("geometry/width", int(resize_event.size().width()))
        self.config.setValue("geometry/height", int(resize_event.size().height()))

    def set_tab_widgets(self):
        """Set the tab widget items."""
        self.tab_widget = QTabWidget(self.form)
        self.tab_widget.setTabShape(QTabWidget.Triangular)
        self.tab_widget.setStyleSheet(
            "QTabWidget::pane {margin-top: 0; margin-right: 5px; margin-bottom: 5px; "
            + "margin-left: 5px;}\n"
            + "QTabWidget::tab-bar {left: 8px}"
        )

        self.tab_widget.addTab(self.assembly_tree_widget, "Assembly Page")
        self.tab_widget.addTab(self.parts_list_widget, "Parts Page")
        self.tab_widget.addTab(self.orders_list_widget, "Orders Page")

        self.form.setCentralWidget(self.tab_widget)

    def get_recent_files_list(self) -> list[str]:
        """
        Set the recent_files list from the config file.

        Returns:
            list[str]: the set of recentss files from the config settins.
        """
        recent_files = []  # ensure the list is empty.

        self.config.beginGroup("recent_files")
        for key in self.config.childKeys():
            if len(self.config.value(key)):
                recent_files.append(self.config.value(key))
            if len(recent_files) == self.__number_recent_files:
                break
        self.config.endGroup()
        return recent_files

    def save_recent_files_list(self, recent_files: list[str]) -> None:
        """
        Set the recent_files list from the config file.

        Parameters:
            recent_files (list[str]: the modified list of recent files.
        """
        self.config.beginGroup("recent_files")
        i = 0
        while i < len(recent_files) and i < self.__number_recent_files:
            self.config.setValue("file" + str(i + 1), recent_files[i])
            i += 1
        while i < self.__number_recent_files:
            self.config.setValue("file" + str(i + 1), "")
            i += 1
        self.config.endGroup()
