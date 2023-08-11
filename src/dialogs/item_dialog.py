"""
Edit an Item in the database.

File:       item_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2020 - 2023 Lorn B Kerr
License:    MIT, see file License
"""

from copy import deepcopy

from lbk_library import Dbal
from lbk_library.gui import Dialog
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from elements import ConditionSet, Item, ItemSet, Part, PartSet

from .base_dialog import BaseDialog


class ItemDialog(BaseDialog):
    """
    Edit an Item in the database.

    An Item can be added, edited or deleted.
    """

    TOOLTIPS = {
        "record_id": "Required: Select the Item index",
        "assembly": "Required: Enter the Assembly, 1 to 15 Characters",
        "condition": "Required: Select the Item Condition",
        "quantity": "Required: Enter quantity, 0 to  999, 0 default",
        "installed": "Check if Item is installed",
        "box": "Optional: Enter Storage box if stored, 0 to 99",
        "remarks": "Optional: up to 255 characters",
        "part_number": "Select Part Number, Required",
        "delete": "Permanently DELETE the current item and all the lines",
        "cancel": "Close the form, optionally saving any changed information",
        "save_new": "Save the current item, then clear the form",
        "save_done": "Save the current item, then close the form",
    }
    """ Tooltips for each of the elements on the form. """

    def __init__(
        self,
        parent: QMainWindow,
        dbref: Dbal,
        record_id: int = None,
        operation: int = Dialog.EDIT_ELEMENT,
    ) -> None:
        """
        Initialize the Item editing dialog.

        Parameters:
            parent(QMainWindow): the parent window owning this dialog.
            dbref (Dbal): reference to the database for this item.
            record_id (integer): the index into the database for the
                item to be edited, default is None
            operation (integer): either the constant Dialog.ADD_ELEMENT
                if a new item is to be added or the constant
                Dialog.EDIT_ELEMENT for editing an existing item,
                defaults to Dialog.EDIT_ELEMENT
        """
        super().__init__(parent, dbref, operation)
        self.set_element(Item(dbref, record_id))
        self.form = uic.loadUi("./src/forms/item.ui", self)

        self.set_table_header(
            self.form.order_table,
            BaseDialog.PART_ORDER_COL_NAMES,
            BaseDialog.PART_ORDER_COL_WIDTHS,
            len(BaseDialog.PART_ORDER_COL_WIDTHS) - 1,
        )

        self.set_visible_add_edit_elements()
        self.fill_dialog_fields()

        # set dialog element actions
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
        self.form.record_id_combo.activated.connect(self.action_record_id_changed)
        self.form.assembly_edit.editingFinished.connect(self.action_assembly_changed)
        self.form.condition_combo.activated.connect(self.action_condition_changed)
        self.form.quantity_edit.editingFinished.connect(self.action_quantity_changed)
        self.form.installed_chkbox.stateChanged.connect(self.action_installed_changed)
        self.form.storage_box_edit.editingFinished.connect(self.action_box_changed)
        self.form.remarks_edit.editingFinished.connect(self.action_remarks_changed)
        self.form.part_number_combo.activated.connect(self.action_part_number_changed)

    def action_delete(self) -> None:
        """
        Delete Item from the database.

        The Item selected is deleted from the database, then the dialog
        is cleared for another entry. If the deletion is not successful,
        a failure message is displayed.
        Item's record_id.
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
        Save the Item to the database.

        The dialog contents are validated and, if valid, added to the
        database. If the save is successful, the dialog is closed or
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

        If any dialog element has changed, give the
        user the option of saving the changed item info or cancelling
        the item number change.
        """
        item = self.get_element()
        new_index = self.form.record_id_combo.currentText()

        # Are there unsaved edits
        if not item.have_values_changed():
            # no changes or changes already saved
            self.set_element(Item(self.get_dbref(), int(new_index)))
            self.fill_dialog_fields()
        else:  # unsaved changes
            prev_index = item.get_record_id()
            result = self.message_box_exec(self.message_question_changed("Item Number"))

            if result == QMessageBox.StandardButton.Yes:
                print("yes")
                # save item with previous item number, then change to new item number
                save_result = item.update()
                if save_result:
                    self.set_element(Item(self.get_dbref(), new_index))
                    self.fill_dialog_fields()
                else:
                    self.message_box_exec(self.message_warning_failed("Item Save"))

            elif result == QMessageBox.StandardButton.No:
                # don't save, change to new item number
                self.set_element(Item(self.get_dbref(), new_index))
                self.fill_dialog_fields()

            elif result == QMessageBox.StandardButton.Cancel:
                # cancel the record_id change, restore previous item number
                self.form.record_id_combo.setCurrentText(str(prev_index))

    def action_assembly_changed(self) -> None:
        """
        Update the change flag for the assembly entry.

        The entry is forced to upper case and validated.

        Returns:
            (dict)
                ['entry'] - (str) the updated Assembly
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
                ['is_valid_ind'] - (bool) True if the entry is valid and
                     accepted, False if not.
        """
        item = self.get_element()
        # force to upper case and validate
        self.form.assembly_edit.setText(self.form.assembly_edit.text().upper())
        result = item.set_assembly(self.form.assembly_edit.text())
        self.save_buttons_enable(item.have_values_changed() and result["valid"])
        if result["valid"]:
            self.form.assembly_edit.setToolTip(ItemDialog.TOOLTIPS["assembly"])
            result["is_valid_ind"] = self.set_valid_indicator(self.form.assembly_label)
        else:
            self.form.assembly_edit.setToolTip(
                result["msg"] + "; " + ItemDialog.TOOLTIPS["assembly"]
            )
            result["is_valid_ind"] = self.set_invalid_indicator(
                self.form.assembly_label
            )
        return result

    def action_condition_changed(self) -> None:
        """
        Update the changed flag for the Condition combo box.

        The Condition entry, selected from one of the choices, is
        required. If the current value does not match the initial value,
        the change flag is set.

        Returns:
            (dict)
                ['entry'] - (str) the updated condition
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
                ['is_valid_ind'] - (bool) True if the entry is valid and
                     accepted, False if not.
        """
        item = self.get_element()
        result = item.set_condition(self.form.condition_combo.currentText())
        self.save_buttons_enable(item.have_values_changed() and result["valid"])
        if result["valid"]:
            self.form.condition_combo.setToolTip(ItemDialog.TOOLTIPS["condition"])
            result["is_valid_ind"] = self.set_valid_indicator(self.form.condition_label)
        else:
            self.form.condition_combo.setToolTip(
                result["msg"] + "; " + ItemDialog.TOOLTIPS["condition"]
            )
            result["is_valid_ind"] = self.set_invalid_indicator(
                self.form.condition_label
            )
        return result

    def action_quantity_changed(self) -> None:
        """
        Update the changed flag for the 'Quantity' entry.

        The entry in the Quantity box is validated and the change flag
        is set if the entry is not the same as the initial entry.

        Returns:
            (dict)
                ['entry'] - (str) the updated quantity
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
                ['is_valid_ind'] - (bool) True if the entry is valid and
                     accepted, False if not.
        """
        item = self.get_element()
        if self.form.quantity_edit.text() == "":
            self.form.quantity_edit.setText("0")
        result = item.set_quantity(int(self.form.quantity_edit.text()))
        self.save_buttons_enable(item.have_values_changed() and result["valid"])
        if result["valid"]:
            self.form.quantity_edit.setToolTip(ItemDialog.TOOLTIPS["quantity"])
            result["is_valid_ind"] = self.set_valid_indicator(self.form.quantity_label)
        else:
            self.form.quantity_edit.setToolTip(
                result["msg"] + "; " + ItemDialog.TOOLTIPS["quantity"]
            )
            result["is_valid_ind"] = self.set_invalid_indicator(
                self.form.quantity_label
            )
        return result

    def action_installed_changed(self) -> None:
        """
        Update the changed flag for the 'Installed' entry.

        The entry in the Installed box is validated and the change flag
        is set if the entry is not the same as the initial entry.

        Returns:
            (dict)
                ['entry'] - (str) the updated install state
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
                ['is_valid_ind'] - (bool) True if the entry is valid and
                     accepted, False if not.
        """
        item = self.get_element()
        result = item.set_installed(self.form.installed_chkbox.isChecked())
        self.save_buttons_enable(item.have_values_changed() and result["valid"])
        return result

    def action_box_changed(self) -> None:
        """
        Update the changed flag for the 'Box' entry.

        The entry in the Box entry is validated and the change flag is
        set if the entry is not the same as the initial entry.

        Returns:
            (dict)
                ['entry'] - (str) the updated box number
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
                ['is_valid_ind'] - (bool) True if the entry is valid and
                     accepted, False if not.
        """
        item = self.get_element()
        if self.form.storage_box_edit.text() == "":
            self.form.storage_box_edit.setText("0")
        result = item.set_box(self.form.storage_box_edit.text())
        self.save_buttons_enable(item.have_values_changed() and result["valid"])
        if self.form.storage_box_edit.text() == "0":
            self.form.storage_box_edit.setText("")
        if result["valid"]:
            self.form.storage_box_edit.setToolTip(ItemDialog.TOOLTIPS["box"])
            result["is_valid_ind"] = self.set_valid_indicator(
                self.form.storage_box_label
            )
        else:
            self.form.storage_box_edit.setToolTip(
                result["msg"] + "; " + ItemDialog.TOOLTIPS["box"]
            )
            result["is_valid_ind"] = self.set_invalid_indicator(
                self.form.storage_box_label
            )
        return result

    def action_remarks_changed(self) -> None:
        """
        Update the changed flag for the 'Remarks' entry.

        The entry in the Remarks entry is validated and the change flag
        is set if the entry is not the same as the initial entry.

        Returns:
            (dict)
                ['entry'] - (str) the updated remarks
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
                ['is_valid_ind'] - (bool) True if the entry is valid and
                     accepted, False if not.
        """
        item = self.get_element()
        result = item.set_remarks(self.form.remarks_edit.text())
        self.save_buttons_enable(item.have_values_changed() and result["valid"])
        if result["valid"]:
            self.form.remarks_edit.setToolTip(ItemDialog.TOOLTIPS["remarks"])
            result["is_valid_ind"] = self.set_valid_indicator(self.form.remarks_label)
        else:
            self.form.remarks_edit.setToolTip(
                result["msg"] + "; " + ItemDialog.TOOLTIPS["remarks"]
            )
            result["is_valid_ind"] = self.set_invalid_indicator(self.form.remarks_label)
        return result

    def action_part_number_changed(self) -> None:
        """
        Update the changed flag for the 'Remarks' entry.

        The entry in the "Part Number" entry is validated and the change
        flag is set if the entry is not the same as the initial entry.

        Returns:
            (dict)
                ['entry'] - (str) the updated part number
                ['valid'] - (bool) True if the entered value is valid,
                    False otherwise
                ['msg'] - (str) Error message if not valid
                ['is_valid_ind'] - (bool) True if the entry is valid and
                     accepted, False if not.
        """
        item = self.get_element()
        result = item.set_part_number(self.form.part_number_combo.currentText())
        self.save_buttons_enable(item.have_values_changed() and result["valid"])
        self.fill_part_fields(result["entry"])
        self.fill_order_table_fields(result["entry"])
        if result["valid"]:
            self.form.part_number_combo.setToolTip(ItemDialog.TOOLTIPS["part_number"])
            result["is_valid_ind"] = self.set_valid_indicator(
                self.form.part_number_label
            )
        else:
            self.form.part_number_combo.setToolTip(
                result["msg"] + "; " + ItemDialog.TOOLTIPS["part_number"]
            )
            result["is_valid_ind"] = self.set_invalid_indicator(
                self.form.part_number_label
            )
        return result

    def fill_dialog_fields(self) -> None:
        """
        Fill the Dialog fields for the item being displayed.

        The dialog entries will be blank if no item is defined.
        """
        item = self.get_element()
        initial_conditions = deepcopy(item.get_properties())
        self.set_combo_box_selections(
            self.form.record_id_combo,
            ItemSet(self.get_dbref(), None, None, "record_id").build_option_list(
                "record_id"
            ),
            str(item.get_record_id()),
        )
        self.form.assembly_edit.setText(item.get_assembly())
        self.set_combo_box_selections(
            self.form.condition_combo,
            ConditionSet(self.get_dbref()).build_option_list("condition"),
            item.get_condition(),
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
        self.save_buttons_enable(False)

    def fill_part_fields(self, part_number: str = None) -> None:
        """
        Fill the Part fields for the part number in use.

        The dialog entries will be blank if no part number is supplied.

        Parameters:
            part_number (String) The part number for the current item,
                default is None
        """
        part = Part(self.get_dbref(), part_number, "part_number")
        self.set_combo_box_selections(
            self.form.part_number_combo,
            PartSet(self.get_dbref(), None, None, "part_number").build_option_list(
                "part_number"
            ),
            part_number,
        )
        self.form.source_text.setText(part.get_source())
        self.form.description_text.setText(part.get_description())
        self.form.remarks_text.setText(part.get_remarks())
        self.form.total_qty_text.setText(str(part.get_total_quantity()))

    def clear_dialog(self) -> None:
        """Clear the dialog entry fields."""
        self.set_element(Item(self.get_dbref()))
        self.fill_dialog_fields()

    def set_visible_add_edit_elements(self) -> None:
        """Set the visible dialog elements depending on operation flag."""
        # setup combo boxes
        self.form.record_id_combo.setStyleSheet("combobox-popup: 0;")
        self.form.record_id_combo.setMaxVisibleItems(20)
        self.form.part_number_combo.setStyleSheet("combobox-popup: 0;")
        self.form.part_number_combo.setMaxVisibleItems(20)

        # set based on 'operation'
        if self.get_operation() == Dialog.ADD_ELEMENT:
            self.form.record_id_combo.setEnabled(False)
            self.form.record_id_combo.setToolTip(
                "Item ID will be assigned when Item is saved"
            )
            self.get_element().set_value_valid_flag("record_id", True)
        else:
            self.form.record_id_combo.setEnabled(True)
            self.form.record_id_combo.setToolTip(ItemDialog.TOOLTIPS["record_id"])
