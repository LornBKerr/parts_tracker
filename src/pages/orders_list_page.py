"""
This page displays the Orders in a table.

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

    def __init__(self, main_window: QMainWindow, dbref:Dbal) -> None:
        """
        Initialize and display the Order List

        Parameters:
            main_window (QMainWindow): the parent window
            dbref (Dbal): reference to the database for the orders.
        """
        self.main_window: QMainWindow  = main_window
        self.dbref: Dbal = dbref



    # end __init__()





# end class OrdersListPage

