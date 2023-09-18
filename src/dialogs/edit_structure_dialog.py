"""
Change the Assembly structure.

File:       edit_structure_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

from typing import Callable

from lbk_library import Dbal
from lbk_library.gui import Dialog
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame, QMessageBox

from elements import Item


class EditStructureDialog(Dialog):
    """
    Change the Assembly structure.

    The assembly key is changed throughout the data base on all Items
    within therange of the assembly keys given.
    """

    TOOLTIPS = {
        "old_assy_edit": "Required: Enter the existing Assembly to change, 1 to 15 Characters",
        "new_assy_edit": "Required: Enter the new Assembly, 1 to 15 Characters",
        "close_button": "Close the form, any unsaved changes will be lost",
        "change_button": "Save the updated assembly changes, then clear the form",
    }
    """Tooltips for each of the elements on the form."""

    def __init__(
        self,
        dbref: Dbal,
        update_tree: callable,
        operation: int = Dialog.EDIT_ELEMENT,
    ) -> None:
        """
        Initialize the dialog.

        Parameters:
            parent (QMainWindow) the owning dialog.
            dbref (Dbal) reference to the current open database.
            update_tree (callable) reference to the AssemblyTreePage
                update_tree() method.
        """
        super().__init__(None, dbref, operation)
        
        self.closed = False  # used to suppport testing
        """Indicate the dialog is closed."""
        self.set_element(Item(dbref))
        """Start with empty item."""

        self.form = uic.loadUi("./src/forms/edit_structure.ui", self)
        self.set_error_frames()

        self.form.old_assy_edit.editingFinished.connect(self.action_old_assy_changed)
        self.form.new_assy_edit.editingFinished.connect(self.action_new_assy_changed)
        self.form.close_button.clicked.connect(self.action_close)
        self.form.change_button.clicked.connect(
            lambda: self.action_change(update_tree, dbref)
        )

    def action_close(self) -> None:
        """Cancel the operation and close the dialog."""
        self.closed = True
        self.close()

    def action_old_assy_changed(self) -> None:
        """
        Validate the assembly entry key that is to be changed.

        The entry is forced to upper case. The entry must be present
        and 1 to 15 characters long.

        Returns:
            (dict)
                ['entry'] - (str) the updated Assembly
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        self.form.old_assy_edit.setText(self.form.old_assy_edit.text().upper())
        result = self.get_element().set_assembly(self.form.old_assy_edit.text())
        if result["valid"]:
            self.form.old_assy_edit.error = False
            self.form.old_assy_edit.setToolTip(
                EditStructureDialog.TOOLTIPS["old_assy_edit"]
            )
        else:
            self.form.old_assy_edit.error = True
            self.form.old_assy_edit.setToolTip(
                result["msg"] + ";\n" + EditStructureDialog.TOOLTIPS["old_assy_edit"]
            )
        return result

    def action_new_assy_changed(self) -> None:
        """
        Validate the assembly entry key that is to be changed.

        The entry is forced to upper case. The entry must be present
        and 1 to 15 characters long.

        Returns:
            (dict)
                ['entry'] - (str) the updated Assembly
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        self.form.new_assy_edit.setText(self.form.new_assy_edit.text().upper())
        result = self.get_element().set_assembly(self.form.new_assy_edit.text())
        if result["valid"]:
            self.form.new_assy_edit.error = False
            self.form.new_assy_edit.setToolTip(
                EditStructureDialog.TOOLTIPS["new_assy_edit"]
            )
        else:
            self.form.new_assy_edit.error = True
            self.form.new_assy_edit.setToolTip(
                result["msg"] + ";\n" + EditStructureDialog.TOOLTIPS["new_assy_edit"]
            )
        return result

    def action_change(self, update_tree: Callable, dbref: Dbal) -> int:
        """
        Change the Assembly Id throughout from start prefix to end prefix.

        The entries are verified to be  present and different. If valid,
        the Database is searched for all occurrences of the old assembly.
        Each instance of the old assembly is changed to the new assembly.

        Parameters:
            update_tree (Callable): reference to the
                AssemblyTreePage.update_tree() method
            dbref (Dbal): reference to the current open database
        """
        error = False
        msg_1 = "Old Assembly ID and New Assembly ID are the Same.\nNothing to do."
        msg_2 = "Assembly ID is invalid."
        msg_text = ''

        if self.form.old_assy_edit.error:
            error = True
            msg_text = "Old " + msg_2
        elif self.form.new_assy_edit.error:
            error = True
            msg_text = "New " + msg_2
        elif self.form.old_assy_edit.text() == self.form.new_assy_edit.text():
            error = True
            msg_text = msg_1
            self.old_assy_edit.error = True
            self.new_assy_edit.error = True

        if not error:
            return self.change_assembly_ids(update_tree, dbref)
        else:
            self.message_box_exec(self.message_warning_invalid(msg_text))

    def change_assembly_ids(self, update_tree: Callable, dbref: Dbal) -> None:
        """
        Change the selected Assembly IDs in the database to new assembly.

        The Assembly tree on the main page is updated upon success. A
        warming message is shown if a failure to change or save an
        updated item occurrs. A success message box is shown if the
        operation is completed.

        Parameters:
            update_tree (callable): reference to the
                AssemblyTreePage.update_tree() method
            dbref (Dbal): reference to the current open database

        Returns:
            (int) The actual number of items updated.
        """
        # get the text to process
        old = self.form.old_assy_edit.text()
        new = self.form.new_assy_edit.text()
        # set the old assembly id range end
        old_end = old + "ZZZZ"

        # Get the item set
        itemset = self.get_itemset(old, old_end, dbref)

        valid = True
        old_len = len(old)
        number_items_updated = 0
        for item in itemset:
            assy = item.get_assembly()
            new_assy = new + assy[old_len:]
            item.set_assembly(new_assy)
            valid = item.update()
            if valid:
                number_items_updated += 1
            else:
                self.message_box_exec(
                    self.message_warning_failed(
                        "Update from " + assy + " to " + new_assy
                    )
                )
                break

        if valid:
            update_tree()
            action = self.message_box_exec(
                self.message_information_close(
                    str(len(itemset))
                    + " Items have been moved from "
                    + old
                    + " to "
                    + new
                    + ".\nDo another?"
                )
            )
            if action == QMessageBox.StandardButton.Yes:
                self.form.old_assy_edit.setText("")
                self.form.new_assy_edit.setText("")
            else:
                self.action_close()

        return number_items_updated

    def get_itemset(
        self,
        beginning_assy: str,
        ending_assy: str,
        dbref: Dbal,
    ) -> list[Item]:
        """
        Build an item list containing a subset of items selected by assembly.

        Parameters:
            beginning_assy (str): the beginning assembly value
            ending_assy (str): the end point of the selection
            dbref (Dbal): reference to the current open database

        Returns:
            (list) the item list with the selected items
        """
        itemset = []

        sql = (
            "SELECT * FROM items WHERE assembly >= '"
            + beginning_assy
            + "' and assembly <= '"
            + ending_assy
            + "'"
        )
        sql_result = dbref.sql_query(sql, [])
        resultset = dbref.sql_fetchrowset(sql_result)

        for result in resultset:
            itemset.append(Item(dbref, result))

        return itemset

    def set_error_frames(self) -> None:
        """Attach and initialize the errorframes."""
        self.form.old_assy_edit.set_frame(self.form.old_assy_frame)
        self.form.new_assy_edit.set_frame(self.form.new_assy_frame)

