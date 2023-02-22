"""
This is the list displaying the Parts in the database.

File:       parts_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import Dbal
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class PartsListPage:
    """Displaying the Parts in the database."""

    def __init__(self, main_window: QMainWindow, dbref: Dbal) -> None:
        """
        Initialize and display the Part List.

        Parameters
            main_window (QMainWindow): the parent window
            dbref (Dbal): reference to the database for this item.
        """
        self.main_window: QMainWindow = main_window
        self.dbref: Dbal = dbref

    def update_table(self) -> None:
        """Update the display table from database."""
        pass

    def clear_table(self):
        """Clear the contents of the Parts Table."""
        pass

    def set_table_headers(self) -> None:
        """
        Set the table headers.

        The header names are set and the column widths to match the size
        of the entries are set.
        """
        pass

    def action_part_clicked(self, table_item: QTableWidgetItem) -> None:
        """
        Display the Part Editing dialog for the indicated part number.

        Parameters:
            table_item (QTableWidgetItem); The requested part number.
        """
        pass
