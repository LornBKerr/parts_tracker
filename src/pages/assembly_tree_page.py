"""
This page displays the Items in a tree format by assembly order

File:       assembly_tree_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import Dbal
from PyQt6.QtWidgets import QMainWindow

class AssemblyTreePage:
    """
    This page displays the Items in a tree format by assembly order
    """
    def __init__(self, main_window: QMainWindow, dbref:Dbal) -> None:
        """
        Initialize the assembly tree widget

        Parameters:
            main_window (QMainWindow): the parent window
            dbref (Dbal):  database reference for the assembly items.
        """
        self.main_window: QMainWindow  = main_window
        self.dbref: Dbal = dbref


# end classAssemblyTreePage

