"""
Build and execute the Main Window for the Parts Tracker Program

File:       main_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

import os
from pathlib import Path
from typing import Any  # , Union

from lbk_library import Dbal, IniFileParser
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt6 import uic

from .assembly_tree_page import AssemblyTreePage
from .parts_list_page import PartsListPage
from .orders_list_page import OrdersListPage


class MainWindow(QMainWindow):
    """
    Build and execute the Main Window for the Parts Tracker Program
    """
    def __init__(self, app: QApplication) -> None:
        """
        Initialize all the windows for the Program

        Parameters:
            app (QApplication): the QApplication instance
        """
        super().__init__()

        self.assembly_tree: AssemblyTreePage = None
        """ The tabbed pane for the assembly_tree """
        self.part_list: PartsListPage = None
        """ The tabbed pane for the parts list """
        self.order_list: OrdersListPage = None
        """ The tabbed pane for the order list """

        self.__closing: bool = False  # Is the window closing event in process

        self.recent_files: list[str] = []
        """ The set of recent files, newest file first """
        self.db_filepath: str = ""
        """ The currently open database absolute file path """
        self.config: dict[str, Any] = {}
        """ The configuration settings """
        self.config_handler: IniFileParser
        """ Handler to read and write configuration ('.ini') files """

            # get the gui form displayed by the window
        self.form = uic.loadUi("src/forms/main_window.ui", self)

           # the current configuration state
        self.config_handler = IniFileParser("parts_tracker.ini", "parts_tracker")
        self.config = self.get_config_file()

            # the current database handler
        self.dbref = self.open_database()

            # configure the window, loading parts information as available
        self.configure_window()

            # set the actions for the main gui

            # system close button (upper right corner)
        app.aboutToQuit.connect(self.exit_app_action)

            # File Menu Items
        self.form.action_file_open.triggered.connect(self.file_open_action)
        self.form.action_file_close.triggered.connect(self.file_close_action)
#        self.form.action_file_new.triggered.connect(self.file_new_action)
#        self.form.action_recent_file_1.triggered.connect(self.recent_file_1_action)
#        self.form.action_recent_file_2.triggered.connect(self.recent_file_2_action)
#        self.form.action_recent_file_3.triggered.connect(self.recent_file_3_action)
#        self.form.action_recent_file_4.triggered.connect(self.recent_file_4_action)
        self.form.action_file_exit.triggered.connect(self.exit_app_action)
#
#            # Assemblies/Items Menu Actions
#        self.form.action_new_item.triggered.connect(lambda: self.item_dialog_action(None, ADD_ELEMENT))
#        self.form.action_edit_item.triggered.connect(lambda: self.item_dialog_action(None, EDIT_ELEMENT))
#        self.form.action_edit_assembly_tree.triggered.connect(self.edit_assembly_tree_action)
#        self.form.action_save_assembly_list.triggered.connect(self.save_assembly_list_action)
#        self.form.action_update_assemby_tree.triggered.connect(self.update_assembly_tree_action)
#
#            # Parts Menu Actions
#        self.form.action_new_part.triggered.connect(lambda: self.part_dialog_action(None, ADD_ELEMENT))
#        self.form.action_edit_part.triggered.connect(lambda: self.part_dialog_action(None, EDIT_ELEMENT))
#        self.form.action_change_part_number.triggered.connect(self.part_change_pn_dialog_action)
#        self.form.action_update_part_list_table.triggered.connect(self.update_part_list_table_action)
#
#            # Orders Menu Actions
#        self.form.action_new_order.triggered.connect(lambda: self.order_dialog_action(None, ADD_ELEMENT))
#        self.form.action_edit_order.triggered.connect(lambda: self.order_dialog_action(None, EDIT_ELEMENT))
#        self.form.action_update_order_table.triggered.connect(lambda: (self.order_list.update_table()))

            # show the window
        self.show()
    # end __init__()
    
    def get_config_file(self) -> dict[str, Any]:
        """
        Get the stored configuration

        The minimal config dict structure is:
        <pre>  {
                 'FILES': {'file0': str, 'file1': str, 'file2': str, 'file3': str]}
                }
        </pre>
        'FIlES' is the set of recent files opened, most recent first

        Returns:
            (dict) The new configuration file.
        """
            # get config file
        config = self.config_handler.read_config()
        if not config:
            # define default configuration file
            config = {
                "FILES": {"file0": "", "file1": "", "file2": "", "file3": ""},
                "LOCATIONS": {"assy_file_dir": str(Path.home())},
            }

            # set recent files list
        for i in range(4):
            if config["FILES"]["file" + str(i)]:
                self.recent_files.append(config["FILES"]["file" + str(i)])
            else:
                break
        return config
    # end get_config_file()


    def save_config_file(self) -> None:
        """
        Write the config file to storage.
        """
        self.config_handler.write_config(self.config)
    # end save_config_file()

#    ##
#    # Allow child dialogs to update the config settings
#    #
#    # @param config (dict) the updated config file from a child dialog
#    def update_config_file(self, config):
#        self.config = config
#        self.save_config_file()
#    # end update_config_file()

    def open_database(self) -> Dbal:
        """
        Initialize the database object.

        If a recent file is available, open the most recently used
        database file. Otherwise, leave the connection closed

        Returns:
            (Dbal): The database reference
        """
        dbref = Dbal()
        if self.recent_files:
                # use first filename to open the parts file
            self.db_filepath = self.recent_files[0]
            dbref.sql_connect(self.db_filepath)
            self.set_menus_enabled(True)
        else:
            self.set_menus_enabled(False)
        return dbref
    # end _open_database()

    def configure_window(self):
        """
        Configure the displayed window.

        Set the File menu list, size the window and fill the tabbed
        pages with data from the parts file if available.
        """
        # set the file menu
        self.set_files_menu()

        # Load the display widgets
        self.assembly_tree = AssemblyTreePage(self.form, self.dbref)
        self.part_list = PartsListPage(self.form, self.dbref)
        self.order_list = OrdersListPage(self.form, self.dbref)
        self.form.tab_widget.setCurrentIndex(0)
    # end configure_window()

    def set_files_menu(self) -> None:
        """
        Update the Recent Files display.

        Show up to 4 recently opened files as listed in the
        config['FILES'] variable. If less than 4 files are held, hide
        remaining menu actions.
        """
        menu_actions = self.form.menu_file_recent.actions()
        i = 0
        # set the recent files that are known
        for i in range(len(self.recent_files)):
            menu_actions[i].setText(os.path.basename(self.recent_files[i]))
            menu_actions[i].setVisible(True)
            i += 1

            # hide remainder of file menu
        while i < len(menu_actions):
            menu_actions[i].setVisible(False)
            i += 1

            # If no recent files, disable menu item
        if not self.recent_files:
            self.form.menu_file_recent.setDisabled(True)
        else:
            self.form.menu_file_recent.setDisabled(False)
    # end set_files_menu()

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
    # end set_menus_enabled()

    def exit_app_action(self) -> None:
        """
        Save the config file, close database, then Exit
        """
        if not self.__closing:
            self.__closing = True
            self.config_handler.write_config(self.config)
            if self.dbref.sql_is_connected():
                self.dbref.sql_close()
        self.close()
    # end exit_app_action()

    def file_open_action(self, not_used) -> None:
        """
        Open a Parts file.

        Open a parts file, add the file to the recent files list, and
        update the display with the the new dataset.
        """
        return_value = QFileDialog.getOpenFileName(
            None, "Open file", "~/", "Parts Files (*.db)"
        )
        if not return_value[0]:
            return
        filepath = return_value[0]
        self.load_new_file(filepath)
    # end file_open_action()

#    ##
#    # Create and load a new PartsTracker File.
#    #
#    # The database is created with new, empty tables. The file already exists, it is
#    # deleted first, then recreated.
#    #
#    def file_new_action(self) -> None:
#        table_definition = parts_table_sql.sql
#        file_name = QFileDialog.getSaveFileName(
#            None, "New File", "../", "Parts Files (*.db)"
#        )[0]
#        if Path(file_name).is_file():
#            os.remove(file_name)
#        new_file = NewFile(file_name, table_definition)
#        self.load_new_file(file_name)
#    # end file_new_action()

    def load_new_file(self, filepath: str) -> None:
        """
        Build and display a new, empty database file.

        Parameters:
            filepath (String): An absolute path to file to open
        """
            # if file is already on the list, remove it
        if self.recent_files:
            for i in range(len(self.recent_files)):
                if self.recent_files[i] == filepath:
                    del self.recent_files[i]
                    break

            # add to beginning of list
        self.recent_files.insert(0, filepath)

            # update config settings and save
        for i in range(len(self.recent_files)):
            self.config["FILES"]["file" + str(i)] = self.recent_files[i]

        for i in range(len(self.recent_files), 4):
            self.config["FILES"]["file" + str(i)] = ""

        self.save_config_file()
        self.set_files_menu()

        # close the old parts file and open the new
        if self.dbref.sql_is_connected():  # if open, close it
            self.dbref.sql_close()

        self.dbref.sql_connect(filepath)

            # update the window
        if self.dbref.sql_is_connected():
            self.set_menus_enabled(True)
            self.assembly_tree.update_tree()
            self.part_list.update_table()
            self.order_list.update_table()
            self.form.tab_widget.setCurrentIndex(0)
    # end load_new_file()

    def file_close_action(self, not_used) -> None:
        """
        Close the current database file
        """
            # if a file is open, then close it
        if self.dbref.sql_is_connected():
            self.dbref.sql_close()
            self.set_menus_enabled(False)
            self.db_filepath = ""

            # save the configuration file
        self.save_config_file()

            # update the display
        self.assembly_tree.clear_tree()
        self.part_list.clear_table()
        self.order_list.clear_table()
        self.form.tab_widget.setCurrentIndex(0)
    # end file_close_action()

#    ##
#    # Open the first most recent file
#    #
#    def recent_file_1_action(self) -> None:
#        if self.recent_files and len(self.recent_files) > 0:
#            self.load_new_file(self.recent_files[0])
#    # end recent_file_1_action()
#
#    ##
#    # Open the second most recent file
#    #
#    def recent_file_2_action(self) -> None:
#        if self.recent_files and len(self.recent_files) > 1:
#            self.load_new_file(self.recent_files[1])
#    # end recent_file_2_action()
#
#    ##
#    # Open the third most recent file
#    #
#    def recent_file_3_action(self) -> None:
#        if self.recent_files and len(self.recent_files) > 2:
#            self.load_new_file(self.recent_files[2])
#    # end recent_file_3_action()
#
#    ##
#    # Open the fourth most recent file
#    #
#    def recent_file_4_action(self) -> None:
#        if self.recent_files and len(self.recent_files) > 3:
#            self.load_new_file(self.recent_files[3])
#    # end recent_file_4_action()
#
#    ##
#    # Revise the assembly structure of the tree.
#    #
#    # @param dbref (Dbal) reference to the database for this item.
#    # @param resources (AppResources) reference to the app resources
#    #
#    def edit_assembly_tree_action(self) -> None:
#        print('calling edit sturcture dialog')
#        EditStructureDialog(self, self.dbref, self.update_assembly_tree_action).exec()
#    # end edit_assembly_tree_action()
#
#    ##
#    # Save a list of items in assembly order to a csv file and/or a xlsx file
#    #
#    # @param dbref (Dbal) reference to the database for this item.
#    # @param resources (AppResources) reference to the app resources
#    # @param config (dict) the configuration settings
#    #
#    def save_assembly_list_action(self) -> None:
#        SaveAssyListDialog(self, self.dbref, self.config).exec()
#    # end save_assembly_list_action()
#
#    ##
#    # Update the assembly tree display returning to the collapsed view
#    #
#    def update_assembly_tree_action(self) -> None:
#        self.assembly_tree.update_tree()
#    # end update_assembly_tree_action()
#
#    ##
#    # Activate the Item Editing form
#    #
#    # @param resources (AppResources) reference to the app resources for this dialog.
#    # @param entry_index (integer) the index into the database for the item to be
#    #   edited, default is None
#    # @param add_item (int) The constant Dialog.ADD_ELEMENT if a new item is to be aded, Dialog.EDIT_ELEMENT for editing an
#    #   existing item
#    #
#    def item_dialog_action(self, entry_index: int, add_item: int) -> None:
#        ItemDialog(self, self.dbref, entry_index, add_item).exec()
#        self.assembly_tree.update_tree()
#    # end item_dialog_action()
#
#    ##
#    # Activate the Part Editing form
#    #
#    # @param parent (QMainWindow) the parent window owning this dialog.
#    # @param dbref (Dbal) reference to the database for this item.
#    # @param entry_index (integer) the index into the database for the part to be
#    #   edited
#    # @param add_part (int) The constant Dialog.ADD_ELEMENT if a new part is to be aded, Dialog.EDIT_ELEMENT for editing an
#    #   existing part
#    #
#    def part_dialog_action(self, entry_index: int, add_part: int) -> None:
#        PartDialog(self, self.dbref, entry_index, add_part).exec()
#        self.part_list.update_table()
#    # part_dialog_action_add
#
#    ##
#    # Change a part number throughout the database.
#    #
#    # @param parent (QMainWindow) the parent window owning this dialog.
#    # @param dbref (Dbal) reference to the database for this item.
#    #
#    def part_change_pn_dialog_action(self) -> None:
#        ChangePartNumberDialog(self, self.dbref).exec()
#        self.assembly_tree.update_tree()
#        self.part_list.update_table()
#        self.order_list.update_table()
#    # end part_change_pn_dialog_action()
#
#    ##
#    # Update the Parts list table after some change.
#    #
#    # @param dbref (Dbal) reference to the database for this item.
#    #
#    def update_part_list_table_action(self, dbref):
#        self.part_list.update_table()
#     # end update_part_list_table_action()
#
#    ##
#    # Activate the Order Editing form
#    #
#    # @param parent (QMainWindow) the parent window owning this dialog.
#    # @param dbref (Dbal) reference to the database for this order.
#    # @param resources (AppResources) reference to the app resources for this dialog.
#    # @param entry_index (integer) the index into the database for the order to be
#    #   edited, default is None
#    # @param add_order (int) The constant Dialog.ADD_ELEMENT if a new order is to be aded, Dialog.EDIT_ELEMENT for editing an
#    #   existing order
#    #
#    def order_dialog_action(self, entry_index: int, add_order: int) -> None:
#        OrderDialog(self, self.dbref, entry_index, add_order).exec()
#        self.order_list.update_table()
#    # end order_dialog_action()

# end Class MainWindow

