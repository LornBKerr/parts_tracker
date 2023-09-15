"""
This is the list displaying the Orders in the database.

File:       orders_list_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""


from lbk_library import Dbal
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

# from elements import OrderSet


class OrdersListPage:
    """Display the Orders in the database."""

    def __init__(self, main_window: QMainWindow, dbref: Dbal) -> None:
        """
        Initialize and display the Order List.

        Parameters:
            main_window (QMainWindow): the parent window
            dbref (Dbal): reference to the database for this item.
        """
        self.main_window: QMainWindow = main_window
        self.dbref: Dbal = dbref

    def update_table(self) -> None:
        """Read database order table and update the display table."""
        pass

    def clear_table(self) -> None:
        """Clear the Order Line table."""
        pass

    def set_table_headers(self):
        """
        Set the table headers.

        Set the header names and set the column widths to match the size
        of the entries.
        """
        pass

    def _get_number_lines(self, order_number: str) -> int:
        """
        Get the total number of lines for this order number.

        The order_lines table is searched for the lines using this order
        number.

        Parameters:
            order_number (str): Order being searched for.

        Returns:
            (int) the total number of order lines found.
        """
        pass

    def action_order_clicked(self, table_item: QTableWidgetItem) -> None:
        """
        Show the Order Editing dialog for the specified order.

        Parameters:
            table_item (QTableWidgetItem): The clicked item.
        """
        pass
