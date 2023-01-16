"""
This is the list displaying the Parts in the database

File:       parts_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import Dbal
from PyQt6.QtWidgets import QMainWindow


class PartsListPage:
    """
    This is the list displaying the Parts in the database
    """

    def __init__(self, main_window: QMainWindow, dbref: Dbal) -> None:
        """
        Initialize and display the Part List

        Parameters
            main_window (QMainWindow): the parent window
            dbref (Dbal): reference to the database for this item.
        """
        self.main_window: QMainWindow = main_window
        self.dbref: Dbal = dbref

        # set up the Parts Listing Table
        self.table = self.main_window.parts_table_widget
        # set the table headers and load the table

    # #
    # #

    def update_table(self) -> None:
        """
        Read the database part table and update the display table.
        """
        pass

    # ##
    # ##

    def clear_table(self):
        """
        Clear the contents of the Parts Table.
        """
        self.table.clearContents()

    # end clear_table()


# ###
# ###

# end class PartsListPage

