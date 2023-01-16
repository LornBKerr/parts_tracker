"""
This page displays the Items in a tree format by assembly order

File:       assembly_tree_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from lbk_library import Dbal
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTreeWidgetItem  # , QTableWidgetItem

from elements import ItemSet, Part


class AssemblyTreePage:
    """
    This page displays the Items in a tree format by assembly order
    """

    def __init__(self, main_window: QMainWindow, dbref: Dbal) -> None:
        """
        Initialize the assembly tree widget

        Parameters:
            main_window (QMainWindow): the parent window
            dbref (Dbal):  database reference for the assembly items.
        """
        self.main_window: QMainWindow = main_window
        self.dbref: Dbal = dbref

        self.tree = self.main_window.assembly_tree_widget
        self.set_tree_headers()
        if self.dbref.sql_is_connected():
            self.update_tree()

        self.tree.expanded.connect(self.resize)
        self.main_window.button_collapse_tree.clicked.connect(self.action_collapse)
        self.main_window.button_expand_tree.clicked.connect(self.action_expand)

        self.tree.itemClicked.connect(self.action_item_clicked)
    # end __init__()

    def update_tree(self) -> None:
        """
        Update the listing after changes to the underlying data.
        """
        # clear the existing tree so we don't append the new info
        self.tree.clear()
        # get the items to display
        item_set = ItemSet(self.dbref, None, None, "assembly")

        key = dict()
        values = list()
        for item in item_set:
            assembly = item.get_assembly()
            part = Part(self.dbref, item.get_part_number(), "part_number")
            installed = item.get_installed()
            if installed == 1:
                installed = "Yes"
            else:
                installed = ""

            try:
                values = list(
                    [
                        assembly,
                        str(item.get_record_id()),
                        item.get_part_number(),
                        part.get_description(),
                        str(item.get_quantity()),
                        item.get_condition(),
                        installed,
                        item.get_remarks(),
                    ]
                )
            except TypeError:
                print(sys.exc_info())
                print(item.get_properties())
                print(part.get_properties())
                print(values, "\n")

            if len(assembly) == 1:
                key[assembly] = QTreeWidgetItem(self.tree, values)
            else:
                parent = assembly[0:-1]
                if parent != "0":  # Ignore the entry for the Car itself (assembly '0A')
                    finished = False
                    while not finished:
                        try:
                            key[parent]
                            finished = True
                        except KeyError:
                            parent = parent[0:-1]
                    key[assembly] = QTreeWidgetItem(key[parent], values)
                else:
                    continue

            key[assembly].setTextAlignment(
                0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
            key[assembly].setTextAlignment(
                2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
            key[assembly].setTextAlignment(
                3, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
            key[assembly].setTextAlignment(
                4, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            )
            key[assembly].setTextAlignment(
                5, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
            key[assembly].setTextAlignment(
                6, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            )
            key[assembly].setTextAlignment(
                7, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )

    # end update_tree

    def clear_tree(self):
        """
        Clear the assembly listing tree display
        """
        self.tree.clear()

    # end clear_tree()

    def resize(self) -> None:
        """
        Resize left-most column after expanding or contracting tree
        """
        self.tree.resizeColumnToContents(0)

    # end resize()

    def set_tree_headers(self):
        """
        Set the tree headers.

        The header names are set and the column widths to match the size of the entries are set.
        """
        column_names = [
            "Assembly",
            "Item Num",
            "Part Number",
            "Description",
            "Qty Used",
            "Condition",
            "Installed",
            "Remarks",
        ]
        self.tree.setColumnCount(len(column_names))
        self.tree.setHeaderLabels(column_names)
        self.tree.setColumnWidth(0, 80)  # Assembly
        self.tree.setColumnWidth(1, 80)  # Item Number
        self.tree.setColumnWidth(2, 110)  # Part Number
        self.tree.setColumnWidth(3, 320)  # Description
        self.tree.setColumnWidth(4, 70)  # Qty Used
        self.tree.setColumnWidth(5, 70)  # Condition
        self.tree.setColumnWidth(6, 70)  # Installed

    # end set_tree_headers(()

    def action_collapse(self):
        """
        Collapse the tree to just top level entries
        """
        self.tree.collapseAll()
        self.resize()

    # end action_collapse()

    def action_expand(self):
        """
        Expand the tree to show all levels.
        """
        self.tree.expandAll()
        self.resize()

    # end action_expand()

    def action_item_clicked(self, tree_item: QTreeWidgetItem, column: int):
        """
        Display the Item Editing Form.

        Parameteres:
            tree_item (QTreeWidgetItem): the Item clicked
            column (int): the column clicked
        """
        item_number_column = 1
        dialog = ItemDialog(
            self.main_window.tab_widget,
            self.dbref,
            tree_item.text(item_number_column),
            EDIT_ELEMENT,
        )
        dialog.exec()
        self.update_tree()

    # end action_item_clicked


# end classAssemblyTreePage
