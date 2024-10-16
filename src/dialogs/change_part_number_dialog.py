"""
Change a PartNumber throughout the dtabase.

File:       change_part_number_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2022-2024 Lorn B Kerr
License:    MIT, see file License
Version     1.0.0
"""

# from typing import
from typing import ClassVar  # Any,

from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from elements import Part

from .base_dialog import BaseDialog

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class ChangePartNumberDialog(BaseDialog):
    """
    Change a Part Number in the data file.

    The Part Number is changed throughout the data file on all Items and
    OrderLines referencing this old part number.
    """

    TOOLTIPS: ClassVar[dict[str, str]] = {
        "old_part_number_edit": "Required: The part number to be changed.",
        "new_part_number_edit": "Required: The new part number.",
        "close_button": "Close the form.",
        "change_button": "Change all entries from the old part number to the new part number.",
    }

    def __init__(
        self,
        parent: QMainWindow,
        parts_file: PartsFile,
        operation: int = Dialog.EDIT_ELEMENT,
    ) -> None:
        """
        Initialize the dialog.

        Parameters:
            parent (QMainWindow:) the owning dialog
            parts_file (PartsFile) reference to the current open data file
        """
        super().__init__(None, parts_file, operation)
        self.closed = False  # used to suppport testing
        """Indicate the dialog is closed."""
        self.set_element(Part(parts_file))
        """Start with empty part, used for validating entries"""

        self.form = uic.loadUi("./src/forms/change_part_number.ui", self)
        self.set_error_frames()

        self.form.old_part_number_edit.editingFinished.connect(
            self.action_old_part_number_changed
        )

    #        self.form.new_part_number_edit.editingFinished.connect(self.action_new_part_number_changed)
    #        self.form.close_button.clicked.connect(self.action_close)
    #        self.form.change_button.clicked.connect(
    #            lambda: self.action_change(update_tree, parts_file)
    #        )
    #        self.form.change_button.clicked.connect(self.action_change)

    def action_close(self):
        """Cancel the operation and close the dialog."""
        self.closed = True
        self.close()

    def action_old_part_number_changed(self) -> None:
        """
        Force the Old Part Number value to Upper Case and validate.

        Returns:
             (dict)
                'entry' (str): the updated old part number
                'valid' (bool): True if the operation suceeded, False
                    otherwise
                'msg' (str): Error message if not valid
        """
        self.form.old_part_number_edit.setText(
            self.form.old_part_number_edit.text().upper()
        )
        return self.validate_dialog_entry(
            self.get_element().set_part_number,
            self.form.old_part_number_edit,
            self.TOOLTIPS["old_part_number_edit"],
        )

    #    ##
    #    # Force the entered New Part Number value to Upper Case and validate entry
    #    #
    #    # @return (dict)<br>&emsp;&emsp;['entry'] - the updated new part number
    #    #   <br>&emsp;&emsp;['valid'] - (bool) True if the operation suceeded,
    #    #       False otherwise
    #    #   <br>&emsp;&emsp;['msg']   - (String) Error message if not valid
    #    #
    #    def action_new_part_number_changed(self) -> None:
    #        self.form.new_part_number_edit.setText(self.form.new_part_number_edit.text().upper())
    #        result = self.get_element().set_part_number(self.form.new_part_number_edit.text())
    #        if result["valid"]:
    #            self.fields_valid["new_pn"] = True
    #            self.set_valid_format(self.form.new_pn_label)
    #        else:
    #            self.fields_valid["new_pn"] = False
    #            self.set_invalid_format(self.form.new_pn_label)
    #        return result
    #
    #    ##
    #    # Change the Part Number throughout the data file.
    #    #
    #    # The entries are verified to be  present and different. If valid,
    #    # the Database is searched for all occurrences of the old part number.
    #    # Each instance of the old part number is changed to the new part number.
    #    #
    #    def action_change(self) -> None:
    #        msg_text = ""
    #
    #        result_old_pn = self.action_old_part_number_changed()
    #        msg_text += "\nOld Part Number: " + result_old_pn["msg"] + "\n"
    #
    #        result_new_pn = self.action_new_part_number_changed()
    #        msg_text += "\nNew Part Number: " + result_new_pn["msg"] + "\n"
    #
    #        if self.fields_valid["old_pn"] and self.fields_valid["new_pn"]:
    #            if result_old_pn["entry"] == result_new_pn["entry"]:
    #                msg_text = "\nOld Part Number and New Part Number are the Same, "
    #                msg_text += "Nothing to do.\n"
    #                self.fields_valid["old_pnt"] = self.set_invalid_format(
    #                    self.form.old_pn_label
    #                )
    #                self.fields_valid["new_pn"] = self.set_invalid_format(
    #                    self.form.new_pn_label
    #                )
    #
    #        if not (self.fields_valid["old_pn"] and self.fields_valid["new_pn"]):
    #            self.message_warning_invalid(msg_text)
    #        else:
    #            self.change_part_numbers(self.form.old_part_number_edit, self.form.new_part_number_edit)
    #
    #    ##
    #    # Change the validated part number from old to new.
    #    #
    #    # Update the data file for the Part, the Items and the Orders to reflect
    #    # the new part number
    #    #
    #    # @param old_pn_edit (QLineEdit) the old part number
    #    # @param new_pn_edit (QLineEdit) the new part number to be assigned
    #    #
    #    def change_part_numbers(self, old_pn_edit: str, new_pn_edit: str) -> None:
    #        parts_file = self.get_parts_file()
    #        old_pn = old_pn_edit.text()
    #        new_pn = new_pn_edit.text()
    #        msg_text = ""
    #
    #        # Get the old part info.
    #        self.fields_valid["old_pn"] = True
    #        old_part = Part(parts_file, old_pn, "part_number")
    #        # if old part doesn't exist, issue warning
    #        if not old_part.get_entry_index():
    #            self.fields_valid["old_pn"] = False
    #            self.set_invalid_format(self.form.old_pn_label)
    #            msg_text = "\nOld part number '" + old_pn + "' is not in the data file."
    #            self.message_warning_invalid(msg_text)
    #
    #            # get the new part info
    #        self.fields_valid["new_pn"] = False
    #        if self.fields_valid["old_pn"]:
    #            new_part = Part(parts_file, new_pn, "part_number")
    #            # if new part doesn't exist, create new entry
    #            if not new_part.get_entry_index():
    #                new_part = Part(parts_file, old_part.get_properties())
    #                new_part.set_part_number(new_pn)
    #                self.fields_valid["new_pn"] = bool(new_part.add())
    #                if not self.fields_valid["new_pn"]:
    #                    msg_text += " New Part could not be accessed or created."
    #
    #        if self.fields_valid["old_pn"] and self.fields_valid["new_pn"]:
    #            # get set of all items with old part number and change part
    #            # number to new part number
    #            itemset = ItemSet(parts_file, "part_number", old_pn)
    #            for item in itemset:
    #                item.set_part_number(new_pn)
    #                item.update()
    #
    #                # get set of order lines for old part number and place new part
    #                # number in remarks section of each order line
    #            order_line_set = OrderLineSet(parts_file, "part_number", old_pn)
    #            for order_line in order_line_set:
    #                source = Order(parts_file, order_line.get_order_number()).get_source()
    #                order_line.set_remarks(
    #                    order_line.get_remarks()
    #                    + " "
    #                    + source
    #                    + " P/N "
    #                    + old_pn
    #                    + " Replaced by "
    #                    + new_pn
    #                )
    #                order_line.set_part_number(new_pn)
    #                order_line.update()
    #
    #                # delete data file entry for old part number
    #            if not old_part.delete():
    #                self.fields_valid["old_part"] = False
    #                msg_text += " Old Part could not be deleted"
    #
    #            # show final results
    #        if self.fields_valid["old_pn"] and self.fields_valid["new_pn"]:
    #            msg_text += (
    #                " Part Number "
    #                + old_pn
    #                + " has been changed to "
    #                + new_pn
    #                + "."
    #                + "\nChange another Part Number?"
    #            )
    #            action = self.message_information_close(msg_text)
    #            if action == QMessageBox.No:
    #                # No more
    #                self.close()
    #            elif action == QMessageBox.Yes:
    #                # continue, clear dialog
    #                old_pn_edit.setText("")
    #                new_pn_edit.setText("")
    #                msg_text = ""
    #        else:
    #            self.message_warning_invalid(msg_text)

    def set_error_frames(self) -> None:
        """Attach and initialize the error_frames."""
        self.form.old_part_number_edit.set_error_frame(self.form.old_part_number_frame)
        self.form.new_part_number_edit.set_error_frame(self.form.new_part_number_frame)
