"""
This is the list displaying the Orders in the database

File:       orders_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""


from lbk_library import Dbal
from PyQt6.QtWidgets import QMainWindow


class OrdersListPage:
    """
    This is the list displaying the Orders in the database
    """

    def __init__(self, main_window: QMainWindow, dbref: Dbal) -> None:
        """
        Initialize and display the Order List

        Parameters:
        main_window (QMainWindow): the parent window
        dbref (Dbal): reference to the database for this item.
        """
        self.main_window: QMainWindow = main_window
        self.dbref: Dbal = dbref

        # set up the Orders Listing Table
        self.table = self.main_window.orders_table_widget

    # #
    # #

    def update_table(self) -> None:
        """
        Read the database order table and update the display table.
        """
        pass

    # ##
    # ##
    # end update_table()

    def clear_table(self) -> None:
        """
        Clear the contents of the Order Line table
        """
        self.table.clearContents()

    # end clear_table()


# ###

# end class OrdersListPage
