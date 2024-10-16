"""
Edit a Part in the data file.

File:       part_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2020 - 2023 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.0
"""

from copy import deepcopy
from typing import ClassVar

from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

from elements import ItemSet, Part, PartSet, Source, SourceSet

from .base_dialog import BaseDialog

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class PartDialog(BaseDialog):
    """
    Edit a Part in the data file.

    A Part can be added, edited or deleted.
    """

    TOOLTIPS: ClassVar[dict[str, str]] = {
        "part_number_combo": "Select Part Number, Required",
        "part_number_edit": "Enter a Part Number, Required",
        "source_combo": "Select a Source, Required",
        "description_edit": "Description of the part, Required, up to 255 characters",
        "remarks_edit": "Remarks about this part, Optional, up to 255 characters",
        "delete_button": "Permanently Delete the part from the data file.",
        "cancel_button": "Close the form, optionally saving any changed information",
        "save_new_button": "Save the current part, then clear the form",
        "save_done_button": "Save the current part, then close the form",
    }
    """ Tooltips for each of the elements on the form. """

    ITEM_TABLE_COL_NAMES: ClassVar[list[str]] = [
        "Assembly",
        "Item",
        "Quantity",
        "Installed",
    ]
    """ Header names for the item table. """
    ITEM_TABLE_COL_WIDTHS: ClassVar[list[int]] = [100, 60, 80, 60]
    """ column widths for the item table. """

    def __init__(
        self,
        parent: QMainWindow,
        parts_file: PartsFile,
        record_id: int = None,
        operation: int = Dialog.EDIT_ELEMENT,
    ) -> None:
        """
        Initialize the Part editing dialog.

        Parameters:
            parent (QMainWindow): the parent window owning this dialog.
            parts_file (PartsFile): reference to the data file for this item.
            record_id (integer): the index into the data file for the
                item to be edited, default is None
            operation (integer): either the constant Dialog.ADD_ELEMENT
                if a new item is to be added or the constant
                Dialog.EDIT_ELEMENT for editing an existing item,
                defaults to Dialog.EDIT_ELEMENT
        """
        super().__init__(parent, parts_file, operation)
        self.set_element(Part(parts_file, record_id))
        self.form = uic.loadUi("./src/forms/part.ui", self)
        self.set_tooltips()
        self.set_error_frames()
        self.set_visible_add_edit_elements()

        self.set_table_header(
            self.form.order_table,
            BaseDialog.PART_ORDER_COL_NAMES,
            BaseDialog.PART_ORDER_COL_WIDTHS,
            len(BaseDialog.PART_ORDER_COL_WIDTHS) - 1,
        )
        self.set_table_header(
            self.form.item_table,
            self.ITEM_TABLE_COL_NAMES,
            self.ITEM_TABLE_COL_WIDTHS,
            len(self.ITEM_TABLE_COL_WIDTHS) - 1,
        )
        self.fill_dialog_fields()

        # set button actions
        self.form.cancel_button.clicked.connect(
            lambda: self.action_cancel(self.action_save, Dialog.SAVE_DONE)
        )
        self.form.delete_button.clicked.connect(self.action_delete)
        self.form.save_done_button.clicked.connect(
            lambda: self.action_save(Dialog.SAVE_DONE)
        )
        self.form.save_new_button.clicked.connect(
            lambda: self.action_save(Dialog.SAVE_NEW)
        )
        # set dialog element actions
        self.form.part_number_edit.editingFinished.connect(
            self.action_part_number_edit_changed
        )
        self.form.part_number_combo.activated.connect(
            self.action_part_number_combo_changed
        )
        self.form.source_combo.activated.connect(self.action_source_changed)
        self.form.description_edit.editingFinished.connect(self.action_description_edit)
        self.form.remarks_edit.editingFinished.connect(self.action_remarks_changed)

    def action_delete(self) -> None:
        """
        Delete Part from the data file.

        The Part selected is deleted from the data file. If the deletion
        is successful, a success message is displayed with the deleted
        Part's record_id, then the dialog is cleared for another entry.
        """
        part = self.get_element()
        if self.form.record_id_edit.text():
            part.set_record_id(self.form.record_id_edit.text())
            valid = part.delete()
            if valid:
                self.clear_dialog()
            else:
                self.message_warning_failed("Delete")
        else:
            self.message_warning_selection("Part Number", "delete")

    def action_save(self, done: int) -> None:
        """
        Save the Part to the data file.

        The dialog contents are validated and, if valid, added to the
        data file. If the save is successful, the dialog is closed or
        cleared for another entry as indicated by 'done'. If not
        successful, a failure message is displayed.

        Parameters:
            done (integer): Either the constant Dialog.SAVE_NEW
            to save the form contents, then clear form for new Part or
            Dialog.SAVE_DONE to save, then close the form.

        Returns:
            (int) result of save operation
                0 - Item successfully saved/updated
                1 - Item is invalid and needs correction
                2 - Item saved/updated, but the parameter 'done' has an
                    incorrect value.
                3 - Item save/update failed for some reason
        """
        return_value = -1
        success = False
        part = self.get_element()
        if not part.is_element_valid():
            self.message_warning_invalid()
            return_value = 1
        else:
            if self.form.record_id_edit.text() == "":
                success = part.add()
            elif int(self.form.record_id_edit.text()) > 0:
                success = part.update()

            if success:
                if done == Dialog.SAVE_DONE:
                    return_value = 0
                    self.close()
                elif done == Dialog.SAVE_NEW:
                    return_value = 0
                    self.clear_dialog()
                else:
                    return_value = 2
                    self.close()  # error, just shut down
            else:
                return_value = 3
                self.message_box_exec(self.message_warning_failed("Part Save"))
        return return_value

    def action_part_number_edit_changed(self) -> int:
        """
        Part Number entry has changed.

        Handle the entry of a new part number in the text box. update
        the changed and valid flags as needed.
        """
        partset = PartSet(self.get_parts_file(), None, None, "part_number")
        part_number_list = partset.build_option_list("part_number")
        part_number = self.form.part_number_edit.text()

        # if the part number is not in the current set, add
        if part_number not in part_number_list:
            part = self.get_element()
            result = part.set_part_number(self.form.part_number_edit.text())
            self.save_buttons_enable(part.have_values_changed() and result["valid"])
            if result["valid"]:
                self.form.part_number_edit.setToolTip(self.TOOLTIPS["part_number_edit"])
                self.form.part_number_edit.error = False
            else:
                self.form.part_number_edit.setToolTip(
                    result["msg"] + "; " + self.TOOLTIPS["part_number_edit"]
                )
                self.form.part_number_edit.error = True

        else:  # change to edit mode
            self.form.part_number_combo.setCurrentText(part_number)
            self.set_operation(Dialog.EDIT_ELEMENT)
            self.set_visible_add_edit_elements()
            self.action_part_number_combo_changed()

    def action_part_number_combo_changed(self) -> None:
        """
        Part Number selection has changed.

        Handles the change from the selection of a new part number in
        the selection box. If no changes on the dialog entries,
        repopulate the form with the new Part info. If any current
        dialog element has changed, give the user the option of saving
        the changed part info or cancelling the part number change.
        """
        part = self.get_element()
        new_part_number = self.form.part_number_combo.currentText()

        # Are there unsaved edits
        if not part.have_values_changed():
            self.set_element(
                Part(self.get_parts_file(), new_part_number, "part_number")
            )
            self.fill_dialog_fields()
        else:
            prev_part_number = part.get_part_number()
            result = self.message_box_exec(self.message_question_changed("Part Number"))
            if result == QMessageBox.StandardButton.Yes:
                # save part with previous part number, then change to new part number
                save_result = part.update()
                if save_result:
                    self.set_element(
                        Part(self.get_parts_file(), new_part_number, "part_number")
                    )
                    self.fill_dialog_fields()
                else:
                    self.message_box_exec(self.message_warning_failed("Part Save"))
            elif result == QMessageBox.StandardButton.No:
                # don't save, change to new part number
                self.set_element(
                    Part(self.get_parts_file(), new_part_number, "part_number")
                )
                self.fill_dialog_fields()
            elif result == QMessageBox.StandardButton.Cancel:
                # cancel save, restore previous part number
                self.form.part_number_combo.setCurrentText(prev_part_number)

    def action_source_changed(self) -> dict:
        """
        Update/validate the 'source' entry for the dialog.

        The Source entry. selected from one of the choices, is required.

        Returns:
            (dict)
                ['entry'] - (str) the updated source
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = {"entry": "", "valid": False, "msg": ""}
        indices = SourceSet(self.get_parts_file()).build_option_list("record_id")
        combo_index = self.form.source_combo.currentIndex()
        if combo_index >= 0 and combo_index < len(indices):
            index = int(indices[combo_index])
            result = self.get_element().set_source(index)
        else:
            result["msg"] = "A Condition must be selected. "
        if result["valid"]:
            self.form.source_combo.error = False
            self.form.source_combo.setToolTip(PartDialog.TOOLTIPS["source_combo"])
        else:
            self.form.source_combo.error = True
            self.form.source_combo.setToolTip(
                result["msg"] + PartDialog.TOOLTIPS["source_combo"]
            )
        return result

    def action_description_edit(self) -> dict:
        """
        Validate remarks entry.

        Update the error indicator flag as needed.

        Returns:
            (dict)
                ['entry'] - (str) the updated remarks
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        return self.validate_dialog_entry(
            self.get_element().set_description,
            self.form.description_edit,
            PartDialog.TOOLTIPS["description_edit"],
        )

    def action_remarks_changed(self) -> dict:
        """
        Validate remarks entry.

        Update the error indicator flag as needed.

        Returns:
            (dict)
                ['entry'] - (str) the updated remarks
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        return self.validate_dialog_entry(
            self.get_element().set_remarks,
            self.form.remarks_edit,
            PartDialog.TOOLTIPS["remarks_edit"],
        )

    def fill_dialog_fields(self) -> None:
        """
        Fill the Dialog fields for the part in use.

        The dialog entries will be blank if no part is defined
        """
        part = self.get_element()
        initial_conditions = deepcopy(part.get_properties())
        self.form.record_id_edit.setText(str(part.get_record_id()))
        if part.get_record_id() != 0:
            self.form.record_id_edit.setText(str(part.get_record_id()))
        self.form.part_number_edit.setText(part.get_part_number())
        self.set_combo_box_selections(
            self.form.part_number_combo,
            PartSet(self.get_parts_file(), None, None, "part_number").build_option_list(
                "part_number"
            ),
            part.get_part_number(),
        )
        self.set_combo_box_selections(
            self.form.source_combo,
            SourceSet(self.get_parts_file(), None, None, "source").build_option_list(
                "source"
            ),
            Source(self.get_parts_file(), part.get_source()).get_source(),
        )
        self.form.description_edit.setText(part.get_description())
        self.form.remarks_edit.setText(part.get_remarks())
        self.form.total_qty_text.setText(str(part.get_total_quantity()))

        self.fill_item_table(part.get_part_number())
        self.fill_order_table_fields(part.get_part_number())

        part.set_initial_values(initial_conditions)
        if self.get_operation() == Dialog.ADD_ELEMENT:
            part.set_value_valid_flag("record_id", True)

        self.form.delete_button.setEnabled(bool(part.get_record_id()))
        self.save_buttons_enable(False)

    def fill_item_table(self, part_number: str = None) -> None:
        """
        Build and show the table showing items using this part number.

        Parameters:
            part_number (String) the part number being displayed; if
            no part number, the table is cleared.
        """
        table = self.form.item_table
        table.clearContents()
        if part_number:
            itemset = ItemSet(
                self.get_parts_file(), "part_number", part_number, "assembly"
            )
            table.setRowCount(itemset.get_number_elements())
            if len(itemset.get_property_set()) > 0:
                row = 0
                for item in itemset:
                    table.setItem(row, 0, QTableWidgetItem(item.get_assembly()))

                    table.setItem(row, 1, QTableWidgetItem(str(item.get_record_id())))

                    entry = QTableWidgetItem(str(item.get_quantity()))
                    entry.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    table.setItem(row, 2, entry)

                    installed = item.get_installed()
                    if installed:
                        entry = QTableWidgetItem("Yes")
                    else:
                        entry = QTableWidgetItem("No")
                    table.setItem(row, 3, entry)
                    row += 1

    def clear_dialog(self) -> None:
        """Clear the dialog entry fields."""
        self.set_element(Part(self.get_parts_file()))
        self.fill_dialog_fields()

    def set_visible_add_edit_elements(self) -> None:
        """Set the visible dialog elements depending on operation flag."""
        # always hide the entry index
        self.form.record_id_edit.hide()

        if self.get_operation() == Dialog.ADD_ELEMENT:
            self.form.part_number_combo.hide()
            self.form.part_number_combo.setEnabled(False)
            self.form.part_number_edit.show()
            self.form.part_number_edit.setEnabled(True)
            self.get_element().set_value_valid_flag("record_id", True)
            self.form.setWindowTitle("Add a Part")
        else:  # editing an existing part
            self.form.part_number_combo.show()
            self.form.part_number_combo.setEnabled(True)
            self.form.part_number_edit.hide()
            self.form.part_number_edit.setEnabled(False)
            self.form.setWindowTitle("Edit a Part")

    def set_tooltips(self):
        """Set the element tooltips."""
        self.form.part_number_combo.setToolTip(self.TOOLTIPS["part_number_combo"]),
        self.form.part_number_edit.setToolTip(self.TOOLTIPS["part_number_edit"]),
        self.form.source_combo.setToolTip(self.TOOLTIPS["source_combo"]),
        self.form.description_edit.setToolTip(self.TOOLTIPS["description_edit"]),
        self.form.remarks_edit.setToolTip(self.TOOLTIPS["remarks_edit"]),
        self.form.delete_button.setToolTip(self.TOOLTIPS["delete_button"]),
        self.form.cancel_button.setToolTip(self.TOOLTIPS["cancel_button"]),
        self.form.save_new_button.setToolTip(self.TOOLTIPS["save_new_button"]),
        self.form.save_done_button.setToolTip(self.TOOLTIPS["save_done_button"]),

    def set_error_frames(self) -> None:
        """Attach and initialize the error_frames."""
        self.form.part_number_combo.set_error_frame(self.form.part_number_frame)
        self.form.part_number_edit.set_error_frame(self.form.part_number_frame)
        self.form.source_combo.set_error_frame(self.form.source_combo_frame)
        self.form.description_edit.set_error_frame(self.form.description_edit_frame)
        self.form.remarks_edit.set_error_frame(self.form.remarks_edit_frame)
