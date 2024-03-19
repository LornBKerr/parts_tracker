"""
Display the Items in a tree format by assembly order.

File:       assembly_tree_page.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

# import sys
from typing import Any

from lbk_library import Dbal, Dialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem

from dialogs import ItemDialog
from elements import Item, ItemSet, Part


class AssemblyTreePage:
    """Displays the Items in a tree format by assembly order."""

    COL_NAMES = [
        "Assembly",
        "Item Num",
        "Part Number",
        "Description",
        "Qty Used",
        "Condition",
        "Installed",
        "Remarks",
    ]
    """ Names of the tree columns."""

    def __init__(self, form: QMainWindow, parts_file: Dbal) -> None:
        """
        Initialize the assembly tree widget.

        Parameters:
            tree (QTreeWidget): the tree to be filled with info
            parts_file (Dbal):  database reference for the parts file.
        """
        self.parts_file: Dbal = parts_file
        self.form = form
        self.tree = form.assembly_tree_widget

        self.resize_columns()
        self.set_tree_headers()

        if self.parts_file.sql_is_connected():
            self.update_tree()

        self.form.button_expand_tree.clicked.connect(self.action_expand)
        self.form.button_collapse_tree.clicked.connect(self.action_collapse)
        self.tree.itemExpanded.connect(self.resize_columns)
        self.tree.itemCollapsed.connect(self.resize_columns)
        self.tree.itemClicked.connect(self.action_item_clicked)

    def update_tree(self) -> None:
        """
        Update the listing after changes to the underlying data.

        Returns:
            dict[str, QTreeWidgetItem] The revised set of items in the tree.
        """
        self.tree.clear()  # clear the existing tree

        # display the revised item set
        item_set = ItemSet(self.parts_file, None, None, "assembly")
        return self.fill_tree_widget(item_set)

    def fill_tree_widget(self, item_set: ItemSet) -> dict[str, list[Item]]:
        """
        Insert the item_set into the Assembly Tree display.

        The item set is expected to be sorted in assembly order.

        Each member of the item set has the part description included,
        the parent assembly deteremined, and is inserted into the tree
        with appropriate text alignment.

        Parameters:
            item_set (ItemSet): the set of items to display in assembly
                order.
        Returns:
            dict[str, QTreeWidgetItem] The set of items in the tree.
        """
        tree_items = {}  # the set of tree widget items
        for item in item_set:
            item_properties = self.set_part_description(item.get_properties())
            item_properties = self.set_installed_entry(item_properties)
            item_values = self.set_item_values(item_properties)
            parent = self.find_parent_assy(item_properties["assembly"], tree_items)
            tree_items = self.add_item_to_tree(
                item_properties["assembly"], item_values, parent, tree_items
            )
        self.resize_columns()
        return tree_items

    def set_part_description(self, item_properties: dict[str, Any]) -> dict[str, Any]:
        """
        Add the part description to the item_properties.

        Parameters:
            item_properties: dict[str, Any]: the set of properties to
                display for the current item entry.

        Returns:
            The updated set of properties.
        """
        part = Part(self.parts_file, item_properties["part_number"], "part_number")
        item_properties["description"] = part.get_description()
        return item_properties

    def set_installed_entry(self, item_properties: dict[str, Any]) -> dict[str, Any]:
        """
        Convert 'installed' boolean value to 'Yes' if intalled else ''.

        Parameters:
            item_properties: dict[str, Any]: the set of properties to
                display for the current item entry.

        Returns:
            dict[str, Any]: The updated set of properties.
        """
        if item_properties["installed"]:
            item_properties["installed"] = "Yes"
        else:
            item_properties["installed"] = ""
        return item_properties

    def set_item_values(self, item_properties: dict[str, Any]) -> list[str]:
        """
        Convert the item_properties dict to a list of strings.

        Parameters:
            item_properties: dict[str, Any]: the set of properties to
                display for the current item entry.

        Returns:
            list[str]: The set of item properties as strings.
        """
        values = [
            item_properties["assembly"],
            str(item_properties["record_id"]),
            item_properties["part_number"],
            item_properties["description"],
            str(item_properties["quantity"]),
            item_properties["condition"],
            item_properties["installed"],
            item_properties["remarks"],
        ]
        return values

    def find_parent_assy(
        self, assembly: str, tree_items: dict[str, QTreeWidgetItem]
    ) -> str | None:
        """
        Find the parent assembly of the current assembly.

        The tree is keyed on the item assembly. The top level tree items
        normally have a single character assembly value. Second, third,
        forth, ... levels have the corresponding number of characters in
        the assembly. The parent of the current assembly is the
        corresponding next level up, so the parent of assembly AC will
        be A, for ACRGE, parent will be ACRG. If the corresponding upper
        level does not exist, move up through the levels until a
        corresponding level is found. If no parent is found, assign the
        assembly as a top level. (Generally, this means there is an
        error in the assignment of the assembly.)

        Parameters:
            assembly (str): the current assembly.
            tree_items (dict[str, QTreeWidgetItem]): the set of tree
                widget items.
        Returns:
            (str) the parent assembly of the current assembly.
        """
        if len(assembly) == 1:
            parent = None
        else:
            parent = assembly[:-1]
            finished = False
            i = 0
            while not finished:
                i += 1
                if i >= len(assembly):
                    parent = None
                    break
                if parent in tree_items.keys():
                    finished = True
                else:
                    parent = parent[:-1]
        return parent

    def add_item_to_tree(
        self,
        assembly,
        item_values: list[str],
        parent: str,
        tree_items: dict[str, QTreeWidgetItem],
    ) -> dict[str, QTreeWidgetItem]:
        """
        Add the current item to the tree.

        Parameters:
            assembly (str): the current assembly.
            item_values (list[str]): item values in column order to
                be added.
            parent (str) the parent assembly of the current assembly.
            tree_items (dict[str, QTreeWidgetItem]): the set of tree
                widget items.

        Returns:
            tree_items (dict[str, QTreeWidgetItem]): the updated set of
                tree widget items.
        """
        if parent is None:
            tree_items[assembly] = QTreeWidgetItem(self.tree, item_values)
        else:
            tree_items[assembly] = QTreeWidgetItem(tree_items[parent], item_values)

        # set center alignment for qty used, condition and installed cols
        tree_items[assembly].setTextAlignment(4, Qt.AlignmentFlag.AlignCenter)
        tree_items[assembly].setTextAlignment(5, Qt.AlignmentFlag.AlignCenter)
        tree_items[assembly].setTextAlignment(6, Qt.AlignmentFlag.AlignCenter)
        return tree_items

    def clear_tree(self):
        """Clear the assembly listing tree display."""
        self.tree.clear()

    def resize_columns(self) -> None:
        """
        Resize the columns to match the size of the entries.

        The last (remarks) column is skipped as it is set to
        automatically stretch or shrink to fill remaining space.
        """
        i = 0
        while i < len(AssemblyTreePage.COL_NAMES) - 2:
            self.tree.resizeColumnToContents(i)
            i += 1

    def set_tree_headers(self):
        """
        Set the tree headers.

        The header names are set, aligned to center of column, and
        initial column widths are set.
        """
        self.tree.setColumnCount(len(AssemblyTreePage.COL_NAMES))
        self.tree.setHeaderLabels(AssemblyTreePage.COL_NAMES)
        i = 0
        while i < len(AssemblyTreePage.COL_NAMES):
            self.tree.header().setDefaultAlignment(Qt.AlignmentFlag.AlignHCenter)
            i += 1
        self.resize_columns()

    def action_collapse(self):
        """Collapse the tree to top level entries."""
        self.tree.collapseAll()
        self.resize_columns()

    def action_expand(self):
        """Expand the tree to show all levels."""
        self.tree.expandAll()
        self.resize_columns()

    def action_item_clicked(self, tree_item: QTreeWidgetItem, column: int) -> str:
        """
        Display the Item Editing Dialog.

        Parameters:
            tree_item (QTreeWidgetItem): the Item clicked
            column (int): the column clicked

        Returns:
            (str): the type of dialog executed (primarily for testing).

        """
        item_number_column = 1

        dialog = ItemDialog(
            self.form.tab_widget,
            self.parts_file,
            tree_item.text(item_number_column),
            Dialog.EDIT_ELEMENT,
        )
        dialog.open()
        self.update_tree()
        return dialog

    def get_parts_file(self):
        """
        Return the databbase reference.

        Return (Dbal): the current database reference.
        """
        return self.parts_file
