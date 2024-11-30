"""
Edit an Item in the parts file.

File:       item_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2020 - 2023 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.0
"""

from copy import deepcopy
from typing import ClassVar

from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from elements import Condition, ConditionSet, Item, ItemSet, Part, PartSet, Source

from .base_dialog import BaseDialog

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class ItemDialog(BaseDialog):
    """
    Edit an Item in the parts file.

    An Item can be added, edited or deleted.
    """

    TOOLTIPS: ClassVar[dict[str, str]] = {
        "assembly": "Required: Enter the Assembly, 1 to 15 Characters",
        "box": "Optional: Enter Storage box if stored, 0 to 99",
        "cancel": "Close the form, optionally saving any changed information",
        "condition": "Required: Select the Item Condition",
        "delete": "Permanently DELETE the current item and all the lines",
        "installed": "Check if Item is installed",
        "part_number": "Select Part Number, Required",
        "quantity": "Required: Enter quantity, 0 to  999, 0 is default",
        "record_id": "Required: Select the Item index",
        "record_id_tbd": "Item ID will be assigned when Item is saved",
        "remarks": "Optional: up to 255 characters",
        "save_new": "Save the current item, then clear the form",
        "save_done": "Save the current item, then close the form",
    }
    """Tooltips for each of the elements on the form. """

    def __init__(
        self,
        parent: QMainWindow,
        parts_file: PartsFile,
        record_id: int = None,
        operation: int = Dialog.EDIT_ELEMENT,
    ) -> None:
        """
        Initialize the Item editing dialog.

        Parameters:
            parent(QMainWindow): the parent window owning this dialog.
            parts_file (PartsFile): reference to the parts file for this
                item.
            record_id (integer): the index into the parts file for the
                item to be edited, default is None
            operation (integer): either the constant Dialog.ADD_ELEMENT
                if a new item is to be added or the constant
                Dialog.EDIT_ELEMENT for editing an existing item,
                defaults to Dialog.EDIT_ELEMENT
        """
        super().__init__(parent, parts_file, operation)
        self.set_element(Item(parts_file, record_id))
        self.form = uic.loadUi("./src/forms/item.ui", self)

        self.set_tooltips()
        self.set_error_frames()
        self.set_visible_add_edit_elements()
        self.set_table_header(
            self.form.order_table,
            BaseDialog.PART_ORDER_COL_NAMES,
            BaseDialog.PART_ORDER_COL_WIDTHS,
            len(BaseDialog.PART_ORDER_COL_WIDTHS) - 1,
        )
        self.fill_dialog_fields()

        # Set dialog button actions
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
        self.form.assembly_edit.editingFinished.connect(self.action_assembly_edit)
        self.form.condition_combo.activated.connect(self.action_condition_combo)
        self.form.quantity_edit.editingFinished.connect(self.action_quantity_edit)
        self.form.installed_chkbox.stateChanged.connect(self.action_installed_checkbox)
        self.form.part_number_combo.activated.connect(self.action_part_number_combo)
        self.form.remarks_edit.editingFinished.connect(self.action_remarks_edit)
        self.form.storage_box_edit.editingFinished.connect(self.action_storage_box_edit)
        self.form.record_id_combo.activated.connect(self.action_record_id_changed)

    def action_delete(self) -> None:
        """
        Delete Item from the parts file.

        The Item selected is deleted from the parts file, then the
        dialog is cleared for another entry. If the deletion is not
        successful, a failure message is displayed.
        """
        item = self.get_element()
        if self.form.record_id_combo.currentText():
            item.set_record_id(self.form.record_id_combo.currentText())
            valid = item.delete()
            if valid:
                self.clear_dialog()
            else:
                self.message_box_exec(self.message_warning_failed("Delete"))
        else:
            self.message_box_exec(
                self.message_warning_selection("Item Number", "delete")
            )

    def action_save(self, done: int) -> None:
        """
         Save the Item to the parts file.

         The dialog contents are validated and, if valid, added to the
         parts file. If the save is successful, the dialog is closed or
        cleared for another entry as indicated by 'done'. If not
         successful, a failure message is displayed.

         Parameters:
             done (integer) Dialog.SAVE_DONE if finished with dialog,
                 Dialog.SAVE_NEW to do another new item
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
        item = self.get_element()
        if not item.is_element_valid():
            self.message_box_exec(self.message_warning_invalid())
            return_value = 1
        else:
            if self.form.record_id_combo.currentText() == "":
                success = item.add()
            elif int(self.form.record_id_combo.currentText()) > 0:
                success = item.update()

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
                self.message_box_exec(self.message_warning_failed("Item Save"))
        return return_value

    def action_record_id_changed(self) -> None:
        """
        Item Number selection has changed.

        If the new record_id has not changed, do nothing.

        If no changes on the dialog entries, repopulate the from with
        the new Item info.

        If any dialog element has changed, give the user the option of
        saving the changed item info or cancelling the item number
        change.
        """
        item = self.get_element()
        new_index = self.form.record_id_combo.currentText()
        if new_index == "":
            new_index = -1

        # Are there unsaved edits
        if not item.have_values_changed():
            # no changes or changes already saved
            self.set_element(Item(self.get_datafile(), int(new_index)))
            self.fill_dialog_fields()
        else:  # unsaved changes
            prev_index = item.get_record_id()
            result = self.message_box_exec(self.message_question_changed("Item Number"))

            if result == QMessageBox.StandardButton.Yes:
                # save item with previous item number, then change to new item number
                save_result = item.update()
                if save_result:
                    self.set_element(Item(self.get_parts_file(), new_index))
                    self.fill_dialog_fields()
                else:
                    self.message_box_exec(self.message_warning_failed("Item Save"))

            elif result == QMessageBox.StandardButton.No:
                # don't save, change to new item number
                self.set_element(Item(self.get_parts_file(), new_index))
                self.fill_dialog_fields()

            elif result == QMessageBox.StandardButton.Cancel:
                # cancel the record_id change, restore previous item number
                self.form.record_id_combo.setCurrentText(str(prev_index))

    def action_assembly_edit(self) -> None:
        """
        Update and validate assembly entry.

        The entry is forced to upper case and validated. Error flags are
        set if necessary.

        Returns:
            (dict)
                ['entry'] - (str) the updated Assembly
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        self.form.assembly_edit.setText(self.form.assembly_edit.text().upper())
        return self.validate_dialog_entry(
            self.get_element().set_assembly,
            self.form.assembly_edit,
            ItemDialog.TOOLTIPS["assembly"],
        )

    def action_condition_combo(self) -> None:
        """
        Update/validate the 'condition' entry for the dialog.

        The Condition entry, selected from one of the choices, is
        required. If the condition is not set, an error is flagged and
        error message included in the tooltip.

        Returns:
            (dict)
                ['entry'] - (str) the updated condition
                ['valid'] - (bool) True if the entered value is valid,
                   False otherwise
                ['msg'] - (str) Error message if not valid
        """
        result = {"entry": "", "valid": False, "msg": ""}
        indices = ConditionSet(self.get_parts_file()).build_option_list("record_id")
        combo_index = self.form.condition_combo.currentIndex()
        if combo_index >= 0 and combo_index < len(indices):
            index = int(indices[combo_index])
            result = self.get_element().set_condition(index)
        else:
            result["msg"] = "A Condition must be selected. "
        if result["valid"]:
            self.form.condition_combo.error = False
            self.form.condition_combo.setToolTip(ItemDialog.TOOLTIPS["condition"])
        else:
            self.form.condition_combo.error = True
            self.form.condition_combo.setToolTip(
                result["msg"] + ItemDialog.TOOLTIPS["condition"]
            )
        return result

    def action_installed_checkbox(self) -> None:
        """
        Update the Item's installed flag.

        Returns:
            (dict)
                ['entry'] - (str) the updated condition
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        return self.get_element().set_installed(self.form.installed_chkbox.isChecked())

    def action_part_number_combo(self) -> None:
        """
        Validate the "Part Number" entry.

        Load the order table and item tables. Must be one of the
        pre-defined part numbers.

        Returns:
            (dict)
                ['entry'] - (str) the updated part number
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        item = self.get_element()
        result = self.validate_dialog_entry(
            self.get_element().set_part_number,
            self.form.part_number_combo,
            ItemDialog.TOOLTIPS["part_number"],
        )
        self.fill_part_fields(result["entry"])
        self.fill_order_table_fields(result["entry"])
        return result

    def action_quantity_edit(self) -> None:
        """
         Validate the Quantity for this item. May be empty (0).

        Returns:
             (dict)
                 ['entry'] - (str) the updated quantity
                 ['valid'] - (bool) True if the entered value is valid,
                     False otherwise
                 ['msg'] - (str) Error message if not valid
        """
        item = self.get_element()
        if self.form.quantity_edit.text() == "":
            self.form.quantity_edit.setText("0")
        return self.validate_dialog_entry(
            self.get_element().set_quantity,
            self.form.quantity_edit,
            ItemDialog.TOOLTIPS["quantity"],
        )

    def action_storage_box_edit(self) -> None:
        """
        Validate the Box entry is validated.

        Optional; if given, must be between 1 and 99. If 0, a blank
        field is displayed.

        Returns:
            (dict)
                ['entry'] - (str) the updated box number
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
        """
        item = self.get_element()
        if self.form.storage_box_edit.text() == "":
            self.form.storage_box_edit.setText("0")
        result = self.validate_dialog_entry(
            self.get_element().set_box,
            self.form.storage_box_edit,
            ItemDialog.TOOLTIPS["box"],
        )
        if self.form.storage_box_edit.text() == "0":
            self.form.storage_box_edit.setText("")
        return result

    def action_remarks_edit(self) -> dict:
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
            ItemDialog.TOOLTIPS["remarks"],
        )

    def fill_dialog_fields(self) -> None:
        """
        Fill the Dialog fields for the item being displayed.

        The dialog entries will be blank if no item is defined.
        """
        item = self.get_element()
        initial_conditions = deepcopy(item.get_properties())
        self.set_combo_box_selections(
            self.form.record_id_combo,
            ItemSet(self.get_parts_file(), None, None, "record_id").build_option_list(
                "record_id"
            ),
            str(item.get_record_id()),
        )
        self.form.assembly_edit.setText(item.get_assembly())
        self.set_combo_box_selections(
            self.form.condition_combo,
            ConditionSet(self.get_parts_file()).build_option_list("condition"),
            Condition(self.get_parts_file(), item.get_condition()).get_condition(),
        )
        qty = item.get_quantity()
        self.form.quantity_edit.setText(str(qty))
        if qty == 0:
            self.form.quantity_edit.setText("")
        self.form.installed_chkbox.setChecked(bool(item.get_installed()))
        initial_conditions["installed"] = bool(item.get_installed())
        box = item.get_box()
        if box == 0 or box is None:
            box = ""
        self.form.storage_box_edit.setText(str(box))
        self.form.remarks_edit.setText(item.get_remarks())

        self.fill_part_fields(item.get_part_number())

        if item.get_part_number():
            self.fill_order_table_fields(item.get_part_number())

        item.set_initial_values(initial_conditions)

        if self.get_operation() == Dialog.ADD_ELEMENT:
            item.set_value_valid_flag("record_id", True)

        if not item.get_record_id():
            self.form.delete_button.setEnabled(False)

    def fill_part_fields(self, part_number: str = None) -> None:
        """
        Fill the Part fields for the part number in use.

        The dialog entries will be blank if no part number is supplied.

        Parameters:
            part_number (String) The part number for the current item,
                default is None
        """
        part = Part(self.get_parts_file(), part_number, "part_number")
        self.set_combo_box_selections(
            self.form.part_number_combo,
            PartSet(self.get_parts_file(), None, None, "part_number").build_option_list(
                "part_number"
            ),
            part_number,
        )
        source = Source(self.get_parts_file(), part.get_source()).get_source()
        self.form.source_text.setText(source)
        self.form.description_text.setText(part.get_description())
        self.form.remarks_text.setText(part.get_remarks())
        self.form.total_qty_text.setText(str(part.get_total_quantity()))

    def clear_dialog(self) -> None:
        """Clear the dialog entry fields."""
        self.set_element(Item(self.get_parts_file()))
        self.fill_dialog_fields()

    def set_visible_add_edit_elements(self) -> None:
        """Set the visible dialog elements depending on operation flag."""
        if self.get_operation() == Dialog.ADD_ELEMENT:
            self.form.record_id_combo.setEnabled(False)
            self.form.record_id_combo.setToolTip(self.TOOLTIPS["record_id_tbd"])
            self.get_element().set_value_valid_flag("record_id", True)
            self.form.setWindowTitle("Add an Item")
        else:
            self.form.record_id_combo.setEnabled(True)
            self.form.record_id_combo.setToolTip(ItemDialog.TOOLTIPS["record_id"])
            self.form.setWindowTitle("Edit an Item")

    def set_tooltips(self):
        """Set the element tooltips."""
        self.form.assembly_edit.setToolTip(self.TOOLTIPS["assembly"])
        self.form.storage_box_edit.setToolTip(self.TOOLTIPS["box"])
        self.form.cancel_button.setToolTip(self.TOOLTIPS["cancel"])
        self.form.condition_combo.setToolTip(self.TOOLTIPS["condition"])
        self.form.delete_button.setToolTip(self.TOOLTIPS["delete"])
        self.form.installed_chkbox.setToolTip(self.TOOLTIPS["installed"])
        self.form.part_number_combo.setToolTip(self.TOOLTIPS["part_number"])
        self.form.quantity_edit.setToolTip(self.TOOLTIPS["quantity"])
        self.form.record_id_combo.setToolTip(self.TOOLTIPS["record_id"])
        self.form.remarks_edit.setToolTip(self.TOOLTIPS["remarks"])
        self.form.save_new_button.setToolTip(self.TOOLTIPS["save_new"])
        self.form.save_done_button.setToolTip(self.TOOLTIPS["save_done"])

    def set_error_frames(self) -> None:
        """Attach and initialize the error_frames."""
        self.form.assembly_edit.set_error_frame(self.form.assembly_frame)
        self.form.condition_combo.set_error_frame(self.form.condition_frame)
        self.form.part_number_combo.set_error_frame(self.form.part_number_frame)
        self.form.quantity_edit.set_error_frame(self.form.quantity_frame)
        self.form.record_id_combo.set_error_frame(self.form.record_id_frame)
        self.form.storage_box_edit.set_error_frame(self.form.storage_box_frame)
        self.form.remarks_edit.set_error_frame(self.form.remarks_frame)
