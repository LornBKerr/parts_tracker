"""
This page displays the Items in a tree format by assembly order.

File:       assembly_tree_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

# import sys

from lbk_library import Dbal

# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTreeWidgetItem  # , QTableWidgetItem

# from elements import ItemSet, Part


class AssemblyTreePage:
    """Displays the Items in a tree format by assembly order."""

    def __init__(self, main_window: QMainWindow, dbref: Dbal) -> None:
        """
        Initialize the assembly tree widget.

        Parameters:
            main_window (QMainWindow): the parent window
            dbref (Dbal):  database reference for the assembly items.
        """
        self.main_window: QMainWindow = main_window
        self.dbref: Dbal = dbref

    def update_tree(self) -> None:
        """Update the listing after changes to the underlying data."""
        pass

    def clear_tree(self):
        """Clear the assembly listing tree display."""
        pass

    def resize(self) -> None:
        """Resize left-most column when needed."""
        pass

    def set_tree_headers(self):
        """
        Set the tree headers.

        The header names are set and the column widths to match the size
        of the entries are set.
        """
        pass

    def action_collapse(self):
        """Collapse the tree to top level entries."""

    def action_expand(self):
        """Expand the tree to show all levels."""

    def action_item_clicked(self, tree_item: QTreeWidgetItem, column: int):
        """
        Display the Item Editing Form.

        Parameteres:
            tree_item (QTreeWidgetItem): the Item clicked
            column (int): the column clicked
        """
        item_number_column = 1
