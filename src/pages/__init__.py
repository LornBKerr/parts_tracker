"""
The pages collection providing the pages for the main window.

This module contains the following classes:
    MainWindow (QMainWindow): The Core window into the program.
    AssemblyTreePage (QWidget): Displays the Items in a Tree listing
        format.
    PartsListPaage (QObject): Displays the Parts in a Table listing.
    OrderListPage (OQject): Displays the Orders in a Table Listing.

Also included is:
    table_definition (List[str]): A list of sql definitions for the
        Parts Database file.

File       __init__.py
Author     Lorn B Kerr
Copyright  (c) 2023, 2024 Lorn B Kerr
License:    MIT, see file License
"""

from .assembly_tree_page import AssemblyTreePage
from .main_window import MainWindow
from .orders_list_page import OrdersListPage
from .parts_list_page import PartsListPage
from .parts_table_definition import table_definition
