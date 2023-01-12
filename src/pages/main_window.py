"""
Build and execute the Main Window for the Parts Tracker Program

File:       main_window.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from pathlib import Path
from typing import Any  # , Union

from lbk_library import Dbal, IniFileParser
from PyQt6.QtWidgets import QApplication, QMainWindow
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

# end Class MainWindow

