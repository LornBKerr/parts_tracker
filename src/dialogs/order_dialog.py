"""
Edit an Order in the data file.

File:       order_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2020 - 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from copy import deepcopy
from typing import ClassVar

from lbk_library import DataFile as PartsFile

#  ErrorFrame, RowState, , TableButtonGroup, TableComboBox, TableLineEdit,
from lbk_library.gui import Dialog, TableModel
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QHeaderView, QMainWindow
#
from elements import (
    Order,
#    OrderLine,
    OrderLineSet,
    OrderSet,
    Part,
#    PartSet,
    Source,
    SourceSet,
)

from .base_dialog import BaseDialog

#
# from .order_line_table_model import OrderLineTableModel
#
# from PyQt6.QtGui import QFont


class OrderDialog(BaseDialog):
    """
    Edit an Order in the data file.

    An Order can be added, edited or deleted.
    """

    TOOLTIPS: ClassVar[dict[str, str]] = {
        "order_number_combo": "Required: Select Order Number",
        "order_number_edit": "Required: (dd-ddd) -> 2 digit year dash 3 digit sequence",
        "date": "Required: mm/dd/yyyy",
        "source": "Required: select from options",
        "remarks": "Optional: up to 255 characters",
        "subtotal": "Read Only: Automatically filled from sum of the order lines",
        "shipping": "Optional: dollars and cents (0.00 minimum)",
        "tax": "Optional: dollars and cents (0.00 minimum)",
        "discount": "Optional: dollars and cents (0 or a negative number)",
        "total": "Read Only: Automatically filled from sum of above charges",
        "delete": "Permanently DELETE the current order and all the lines",
        "cancel": "Close the form, optionally saving any changed information",
        "save_new": "Save the current order, then clear the form",
        "save_done": "Save the current order, then clost the form",
    }
    """The set of tooltips for the Order Dialog."""

# Order Line Table Constants
#    OLT_ENTRY_NAMES: ClassVar[list[str]] = [
#        "record_id",
#        "line",
#        "part_number",
#        "description",
#        "quantity",
#        "cost_each",
#        "remarks",
#    ]
#        "edit",
#        "del",
#    """The entry names to access the OrderLine object properties."""
#
#    # column number aliases.
#
#    # Button id's
#    OLT_EDIT: ClassVar[int] = 1
#    OLT_SAVE: ClassVar[int] = 2
#    OLT_DELETE: ClassVar[int] = 4
#    OLT_UNDELETE: ClassVar[int] = 8
    HEADER_TITLES:list[str] = [
        "Record Id",
        "Line",
        "Part Number",
        "Description",
        "Qty",
        "Cost Each",
        "Remarks",
    ]
    """The names of the order line table columns."""

    COLUMN_TOOLTIPS: list[str] = [
        "Record Id is automatically set.",
        "line number on the order",
        "Required, Select Part Number",
        "Not Editable, Description of the selected part",
        "Required, dollars and cents (0.00 minimum)",
        "Required, Number of items purchased",
        "Optional: up to 255 characters",
        "Update the order line when the order is complete",
    ]
    """The tooltips in column order for each column in the table."""

    COLUMN_ALIGNMENTS = [
        Qt.AlignLeft,       # record id
        Qt.AlignHCenter,    # line Number
        Qt.AlignLeft,       # part number
        Qt.AlignLeft,       # descriptiom
        Qt.AlignHCenter,    # quantity
        Qt.AlignRight,      # cost each
        Qt.AlignLeft,       # remarks
    ]
    """The text alignement in column order for each column in the table."""

    ORDER_LINE_NAMEs = [
        "record_id",
        "order_number",
        "line",
        "part_number",
        "quantity",
        "cost_each",
        "remarks",
    ]
    """The data names for each of the columns except 'description'."""

    COLUMN_WIDTHS: ClassVar[list[int]] = [70, 35, 95, 315, 45, 80, 20]
    """The widths of the table columns."""

#        "Save the order line when the order is complete",
#        "Delete the order line when the order is complete",

    NORMAL_BACKGROUND = QBrush(QColor("white"))
    """Default background for for the table cells."""
    ERROR_BACKGROUND = QBrush(QColor(0xF0C0C0))
    """Background for for error entry in a cell."""

    def __init__(
        self,
        parent: QMainWindow,
        parts_file: PartsFile,
        record_id: int = -1,
        operation: int = Dialog.EDIT_ELEMENT,
    ) -> None:
        """
        Initialize the Order editing dialog.

        Parameters:
            parent (QMainWindow) the parent window owning this dialog.
            parts_file (PartsFile) reference to the data file for this order.
            record_id (int) the index into the data file for the order
                to be edited
            operation (integer): either the constant Dialog.ADD_ELEMENT
                if a new order is to be added or the constant
                Dialog.EDIT_ELEMENT for editing an existing orderm,
                defaults to Dialog.EDIT_ELEMENT
        """
        super().__init__(parent, parts_file, operation)
        self.set_element(Order(parts_file, record_id))
        self.form = uic.loadUi("./src/forms/order.ui", self)

        # initialize the basics of the form
        self.set_tool_tips()
        self.set_error_frames()
        self.set_visible_add_edit_elements()
        self.order_lines: OrderLineSet = None
        self.order_line_list: List = []
        self.dataset:list[list[str]] = []
        self.table: QTableView = self.form.order_line_table
        self.model = TableModel(
            self.dataset,
            self.HEADER_TITLES,
            self.COLUMN_TOOLTIPS,
            self.COLUMN_ALIGNMENTS,
            self.NORMAL_BACKGROUND,
        )
        self.table.setModel(self.model)
        self.table.setStyleSheet(
            "QTableView {selection-background-color: white; selection-color: blue;}"
        )
        self.setup_table()

        self.fill_dialog_fields()


#
#        # set dialog button actions
#        self.form.cancel_button.clicked.connect(
#             lambda: self.action_cancel(self.action_save, Dialog.SAVE_DONE)
#        )
#        self.form.delete_button.clicked.connect(self.action_delete)
#        self.form.save_done_button.clicked.connect(
#            lambda: self.action_save(Dialog.SAVE_DONE)
#        )
#        self.form.save_new_button.clicked.connect(
#            lambda: self.action_save(Dialog.SAVE_NEW)
#        )
#
#        self.form.order_number_combo.activated.connect(self.action_order_number_combo)
#        self.form.order_number_edit.editingFinished.connect(
#            self.action_order_number_edit
#        )
#        self.form.date_edit.editingFinished.connect(self.action_date_edit)
#        self.form.source_combo.activated.connect(self.action_source_combo)
#        self.form.remarks_edit.editingFinished.connect(self.action_remarks_edit)
#        self.form.discount_edit.editingFinished.connect(self.action_discount_edit)
#        self.form.shipping_edit.editingFinished.connect(self.action_shipping_edit)
#        self.form.tax_edit.editingFinished.connect(self.action_tax_edit)
#
#        # OrderLine table cells
#
#        self.form.order_line_table.cellChanged.connect(
#            self.action_orderline_cell_changed
#        )
#
#        self.form.order_line_table.cellClicked.connect(
#            self.action_orderline_cell_clicked
#        )

    def fill_dialog_fields(self) -> None:
        """
        Fill the Dialog fields for the order being displayed.

        The dialog entries will be blank if no order is defined
        """
        order = self.get_element()
        print(order.get_properties())
        self.set_combo_box_selections(
            self.form.order_number_combo,
            OrderSet(
                self.get_parts_file(), None, None, "order_number"
            ).build_option_list("order_number"),
            order.get_order_number(),
        )

        self.set_combo_box_selections(
            self.form.source_combo,
            SourceSet(self.get_parts_file()).build_option_list("source"),
            Source(self.get_parts_file(), order.get_source()).get_source(),
        )
        self.form.record_id_edit.setText(str(order.get_record_id()))
        self.form.order_number_edit.setText(order.get_order_number())
        self.form.date_edit.setText(order.get_date())
        self.form.remarks_edit.setText(order.get_remarks())
        self.form.tax_edit.setText(format(order.get_tax(), ".2f"))
        self.form.discount_edit.setText(format(order.get_discount(), ".2f"))
        self.form.shipping_edit.setText(format(order.get_shipping(), ".2f"))
        self.form.subtotal_edit.setText("0.00")
        self.form.total_edit.setText("0.00")
        
        # get OrderLine set for the order.
        self.order_lines = OrderLineSet(
            self.get_parts_file(),
            "order_number",
            self.get_element().get_order_number(),
            "line",
        )
        self.order_line_list = self.order_lines.get_property_set()
        self.dataset = self.build_data_set()
        self.model = TableModel(
            self.dataset,
            self.HEADER_TITLES,
            self.COLUMN_TOOLTIPS,
            self.COLUMN_ALIGNMENTS,
            self.NORMAL_BACKGROUND,
        )
        self.table.setModel(self.model)
        self.append_row()
        # update subtotal and total after filling orderlines
        self.update_subtotal()
        self.update_total()

        order.set_initial_values(deepcopy(order.get_properties()))

        if self.get_operation() == Dialog.ADD_ELEMENT:
            order.set_value_valid_flag("record_id", True)

        if not order.get_record_id():
            self.form.delete_button.setEnabled(False)
        self.save_buttons_enable(False)

    def update_total(self) -> None:
        """
        Update the total cost entry.

        The total is calculated from the 'subtotal', 'shipping', 'tax',
        and 'discount' entries. This is called whenever subtotal,
        shipping, tax, or discount entries change. This is not directly
        setable from the dialog.

        Returns:
            (float) - total cost for this order.
        """
        order = self.get_element()
        total = float(order.get_subtotal()) + float(order.get_shipping())
        total += float(order.get_tax()) + float(order.get_discount())
        order.set_total(total)
        self.form.total_edit.setText(format(total, ".2f"))
        return total

    def update_subtotal(self) -> None:
        """
        Update the 'subtotal' entry for the dialog.

        The subtotal is calculated from the 'quantity' and 'cost each'
        entries in each row of the OrderLine table. The total entry is
        updated when this is updated.

        Returns:
            (float) - the sum of the order lines cost
        """
        order = self.get_element()
        subtotal = 0.0
        for order_line in self.order_lines:
            subtotal += order_line.get_line_cost()

        order.set_subtotal(subtotal)
        self.form.subtotal_edit.setText(format(subtotal, ".2f"))
        self.update_total()
        return subtotal

    def append_row(self) -> None:
        """
        Append an empty row to the data_set.

        Each column value of this empty line will have the value None.
        """
        self.model.insertRows(self.model.rowCount(), 1)
        self.model.layoutChanged.emit()

    def setup_table(self) -> None:
        """Configure the order line table."""
        self.table.verticalHeader().hide()
        for i in range(len(self.COLUMN_WIDTHS)):
            self.table.setColumnWidth(i, self.COLUMN_WIDTHS[i])
        self.table.horizontalHeader().setSectionResizeMode(
            self.HEADER_TITLES.index("Remarks"), QHeaderView.ResizeMode.Stretch
        )
        self.table.setColumnHidden(self.ORDER_LINE_NAMEs.index("record_id"), True)

    def build_data_set(self) -> list[list[str]]:
        """
        Convert the properties of the order_line_list to a list of lists.

        Returns:
            (list[list[str]]) The set of condition properties as an
                list of lists of strings in table column order.
        """
        data_set = []
        for i in range(len(self.order_line_list)):
            an_order_line = []
            order_line_properties = self.order_line_list[i].get_properties()
            record_id_value = order_line_properties["record_id"]

            for name in self.ORDER_LINE_NAMEs:
                if not record_id_value:
                    order_line_properties[name] = ""
                if not name == "order_number" and not name == "cost_each":
                    an_order_line.append(order_line_properties[name])
                if name == "part_number":
                    an_order_line.append(
                        Part(
                            self.get_parts_file(),
                            order_line_properties["part_number"],
                            "part_number",
                        ).get_description()
                    )
                    
                if name == "cost_each":
                    an_order_line.append(format(order_line_properties[name], ".2f"))
            data_set.append(an_order_line)

        return data_set

    def set_tool_tips(self) -> None:
        """Set the rooltips for each of the form elements."""
        self.form.order_number_combo.setToolTip(self.TOOLTIPS["order_number_combo"])
        self.form.order_number_edit.setToolTip(self.TOOLTIPS["order_number_edit"])
        self.form.date_edit.setToolTip(self.TOOLTIPS["date"])
        self.form.source_combo.setToolTip(self.TOOLTIPS["source"])
        self.form.remarks_edit.setToolTip(self.TOOLTIPS["remarks"])
        self.form.subtotal_edit.setToolTip(self.TOOLTIPS["subtotal"])
        self.form.shipping_edit.setToolTip(self.TOOLTIPS["shipping"])
        self.form.tax_edit.setToolTip(self.TOOLTIPS["tax"])
        self.form.discount_edit.setToolTip(self.TOOLTIPS["discount"])
        self.form.total_edit.setToolTip(self.TOOLTIPS["total"])
        self.form.delete_button.setToolTip(self.TOOLTIPS["delete"])
        self.form.cancel_button.setToolTip(self.TOOLTIPS["cancel"])
        self.form.save_new_button.setToolTip(self.TOOLTIPS["save_new"])
        self.form.save_done_button.setToolTip(self.TOOLTIPS["save_done"])

    def set_error_frames(self) -> None:
        """Attach and initialize the error_frames."""
        self.form.order_number_combo.set_error_frame(self.form.order_number_frame)
        self.form.order_number_edit.set_error_frame(self.form.order_number_frame)
        self.form.date_edit.set_error_frame(self.form.date_edit_frame)
        self.form.source_combo.set_error_frame(self.form.source_combo_frame)
        self.form.remarks_edit.set_error_frame(self.form.remarks_edit_frame)
        self.form.shipping_edit.set_error_frame(self.form.shipping_frame)
        self.form.tax_edit.set_error_frame(self.form.tax_frame)
        self.form.discount_edit.set_error_frame(self.form.discount_frame)

    def set_visible_add_edit_elements(self) -> None:
        """
        Show or hide the Order number selection fields.

        If adding a new Order, show the line edit box to enter the Order
        Number. Otherwise, for an existing Order, show the Order Number
        selections ComboBox
        """
        # always hide entry index fields
        #        self.form.record_id_edit.hide()
        # if adding a new Order
        if self.get_operation() == Dialog.ADD_ELEMENT:
            self.form.order_number_combo.hide()
            self.form.order_number_combo.setEnabled(False)
            self.form.order_number_edit.show()
            self.form.order_number_edit.setEnabled(True)
            self.get_element().set_value_valid_flag("record_id", True)
        else:  # editing an existing part
            self.form.order_number_combo.show()
            self.form.order_number_combo.setEnabled(True)
            self.form.order_number_edit.hide()
            self.form.order_number_edit.setEnabled(False)
#
#
#    def action_date_edit(self) -> None:
#        """
#        Update/validate the 'date' entry for the dialog.
#
#        The date fromats accepted are mm/dd/yyyy such as '02/23/2015'
#        or yyyy-mm-dd such as '2015-23-03'.
#
#        Returns:
#            (dict)
#                ['entry'] - (str) the updated remark
#                ['valid'] - (bool) True if the entered value is valid,
#                    False otherwise
#                ['msg'] - (str) Error message if not valid
#        """
#        result = self.validate_dialog_entry(
#            self.get_element().set_date,
#            self.form.date_edit,
#            self.TOOLTIPS["date"],
#        )
#        return result
#
#    def action_source_combo(self) -> None:
#        """
#        Update/validate the 'source' entry for the dialog.
#
#        The Source entry. selected from one of the choices, is required.
#
#        Returns:
#            (dict)
#                ['entry'] - (str) the updated source
#                ['valid'] - (bool) True if the entered value is valid,
#                    False otherwise
#                ['msg'] - (str) Error message if not valid
#        """
#        result = {"entry": "", "valid": False, "msg": ""}
#        indices = SourceSet(self.get_parts_file()).build_option_list("record_id")
#        combo_index = self.form.source_combo.currentIndex()
#        if combo_index >= 0 and combo_index < len(indices):
#            index = int(indices[combo_index])
#            result = self.get_element().set_source(index)
#        else:
#            result["msg"] = "A Condition must be selected. "
#        if result["valid"]:
#            self.form.source_combo.error = False
#            self.form.source_combo.setToolTip(self.TOOLTIPS["source"])
#        else:
#            self.form.source_combo.error = True
#            self.form.source_combo.setToolTip(result["msg"] + self.TOOLTIPS["source"])
#        return result
#
#    def action_remarks_edit(self) -> None:
#        """
#        Validate remarks entry.
#
#        Update the error indicator flag as needed.
#
#        Returns:
#            (dict)
#                ['entry'] - (str) the updated remarks
#                ['valid'] - (bool) True if the entered value is valid,
#                    False otherwise
#                ['msg'] - (str) Error message if not valid
#        """
#        result = self.validate_dialog_entry(
#            self.get_element().set_remarks,
#            self.form.remarks_edit,
#            self.TOOLTIPS["remarks"],
#        )
#        return result
#
#    def action_discount_edit(self):
#        """
#        Validate the 'discount' entry for the dialog.
#
#        The discount, if present, is a negative number.
#
#        Returns:
#            (dict)
#                ['entry'] - (str) the updated remark
#                ['valid'] - (bool) True if the entered value is valid,
#                    False otherwise
#                ['msg'] - (str) Error message if not valid
#        """
#        result = self.validate_dialog_entry(
#            self.get_element().set_discount,
#            self.form.discount_edit,
#            self.TOOLTIPS["discount"],
#        )
#        if result["entry"] == 0:
#            self.form.discount_edit.setText("")
#        else:
#            self.form.discount_edit.setText(format(result["entry"], ".2f"))
#
#        if result["valid"]:
#            self.update_total()
#        return result
#
#    def action_shipping_edit(self):
#        """
#        Update/validate the 'shipping' entry for the dialog.
#
#        Returns:
#            (dict)
#                ['entry'] - (str) the updated remark
#                ['valid'] - (bool) True if the entered value is valid,
#                    False otherwise
#                ['msg'] - (str) Error message if not valid
#        """
#        result = self.validate_dialog_entry(
#            self.get_element().set_shipping,
#            self.form.shipping_edit,
#            self.TOOLTIPS["shipping"],
#        )
#        if result["entry"] == 0:
#            self.form.shipping_edit.setText("")
#        else:
#            self.form.shipping_edit.setText(format(result["entry"], ".2f"))
#        if result["valid"]:
#            self.update_total()
#        return result
#
#    def action_tax_edit(self):
#        """
#        Update/validate the 'tax' entry for the dialog.
#
#        Returns:
#            (dict)
#                ['entry'] - (str) the updated remark
#                ['valid'] - (bool) True if the entered value is valid,
#                    False otherwise
#                ['msg'] - (str) Error message if not valid
#        """
#        result = self.validate_dialog_entry(
#            self.get_element().set_tax,
#            self.form.tax_edit,
#            self.TOOLTIPS["tax"],
#        )
#        if result["entry"] == 0:
#            self.form.tax_edit.setText("")
#        else:
#            self.form.tax_edit.setText(format(result["entry"], ".2f"))
#
#        if result["valid"]:
#            self.update_total()
#        return result
#
#
#    def setup_table(self) -> None:
#        """Configure the order line table."""
#        self.table.verticalHeader().hide()
#        for i in range(len(self.COLUMN_WIDTHS)):
#            self.table.setColumnWidth(i, self.COLUMN_WIDTHS[i])
#        self.table.horizontalHeader().setSectionResizeMode(
#            self.HEADER_TITLES.index("Remarks"), QHeaderView.ResizeMode.Stretch
#        )
#        self.table.setColumnHidden(self.ORDER_LINE_NAMEs.index("record_id"), True)


#    def have_entries_changed(self) -> bool:
#        """
#        Check if changes in the Order or the associated order lines.
#
#        Returns:
#            (bool) True if any changes have been made, False if not
#        """
#        changes = self.get_element().have_values_changed()
#        for row in range(len(self.order_line_row_state)):
#            changes = changes  # or self.order_lines.get(row).have_values_changed()
#        return changes
#
#    def action_delete(self) -> None:
#        """
#        Delete Order from the data file.
#
#        The Order selected along with the attached OrderLines is deleted
#        from the data file. If the deletion is successful, the dialog is
#        cleared for another entry. Messages are shown for any failures.
#        """
#        order = self.get_element()
#        if self.form.record_id_edit.currentText():
#            order.set_record_id(self.form.record_id_edit.currentText())
#            valid = order.delete()
#            if valid:
#                for order_line in self.order_lines:
#                    order_line.delete()
#                self.clear_dialog()
#            else:
#                self.message_warning_failed("Delete")
#        else:
#            self.message_warning_selection("Order Number", "delete")
#
#    def action_save(self, done: int) -> None:
#        """
#        Save the Order to the data file.
#
#        The dialog contents are validated and, if valid, added to the
#        data file. If the save is successful, the dialog is closed or
#        cleared for another entry as indicated by 'done'. If not
#        successful, a failure message is displayed.
#
#        Parameters:
#            done (int) one of the constants SAVE_DONE or SAVE_NEW
#        """
#        order = self.get_element()
#        # check order validity
#        order_valid = True
#        if not order.is_element_valid():
#            order_valid = False
#        for i in range(self.order_lines.get_number_elements()):
#            if (
#                self.order_line_row_state[i] == RowState.Update
#                or self.order_line_row_state[i] == RowState.Save
#            ):
#                if not self.order_lines.get(i).is_element_valid():
#                    order_valid = False
#        if not order_valid:
#            self.message_warning_invalid()
#            return
#
#        # Save order and order lines
#        if self.form.record_id_edit.text() == "":
#            success = order.add()
#        elif int(self.form.record_id_edit.text()) > 0:
#            success = order.update()
#        else:
#            success = False
#
#        if success:
#            for row in range(len(self.order_line_row_state)):
#                if self.order_line_row_state[row] == RowState.Update:
#                    success = self.order_lines.get(row).update()
#                elif self.order_line_row_state[row] == RowState.Save:
#                    success = self.order_lines.get(row).add()
#                elif self.order_line_row_state[row] == RowState.Delete:
#                    success = self.order_lines.get(row).delete()
#
#        if success:
#            if done == Dialog.SAVE_DONE:
#                self.close()
#            elif done == Dialog.SAVE_NEW:
#                self.clear_dialog()
#        else:
#            self.message_warning_failed("Order Save")
#
#    def action_order_number_edit(self) -> None:
#        """
#        Handle the changed Order Number selection.
#
#        This handles the entry of a new order number in the order number
#        edit box. If the  order number is not in the data file, validate
#        the entry. If it is in the data file, change to editing mode and
#        fill the dialog.
#        """
#        orderset = OrderSet(self.get_parts_file(), None, None, "order_number")
#        order_number_list = orderset.build_option_list("order_number")
#        order_number = self.form.order_number_edit.text()
#
#        # if the order number is not in the current set, add
#        if order_number not in order_number_list:
#            order = self.get_element()
#            result = order.set_order_number(order_number)
#            self.save_buttons_enable(self.have_entries_changed() and result["valid"])
#            if result["valid"]:
#                self.form.order_number_edit.setToolTip(self.tooltips["order_number"])
#            #                self.set_valid_format(self.form.order_number_label)
#            else:
#                self.form.order_number_edit.setToolTip(
#                    result["msg"] + "; " + self.tooltips["order_number_edit"]
#                )
#                self.set_invalid_format(self.form.order_number_label)
#
#        else:  # change to edit mode
#            self.form.order_number_combo.setCurrentText(order_number)
#            self.set_operation(Dialog.EDIT_ELEMENT)
#            self.set_visible_add_edit_elements()
#            self.action_order_number_combo()
#
#    def action_order_number_combo(self) -> None:
#        """
#        Handle the changed Order Number selection.
#
#        This handles the change from the selection of a new order number
#        in the selection box.  If no changes on the dialog entries,
#        repopulate the withthe new Order info. If any dialog element
#        has changed, give the user the option of saving the changed
#        order info or cancelling the order number change.
#        """
#        order = self.get_element()
#        new_order_number = self.form.order_number_combo.currentText()
#        # Are there unsaved edits
#        if self.have_entries_changed():
#            prev_order_number = order.get_order_number()
#            result = self.message_question_changed("Order Number")
#            if result == QMessageBox.Yes:
#                # save order with previous order number, then change to new order number
#                save_result = self.get_element().update()
#                if save_result:
#                    self.set_element(
#                        Order(self.get_parts_file(), new_order_number, "order_number")
#                    )
#                    self.order_lines = self.get_element().get_order_lines()
#                    self.order_line_row_state = []
#                    self.fill_dialog_fields()
#                else:
#                    self.message_warning_failed("Order Save")
#            elif result == QMessageBox.No:
#                # don't save, change to new order number
#                self.set_element(
#                    Order(self.get_parts_file(), new_order_number, "order_number")
#                )
#                self.order_lines = self.get_element().get_order_lines()
#                self.order_line_row_state = []
#                self.fill_dialog_fields()
#            else:
#                # cancel save, restore previous order number
#                self.form.order_number_combo.setCurrentText(prev_order_number)
#        else:
#            self.set_element(Order(self.get_parts_file(), new_order_number, "order_number"))
#            self.order_lines = self.get_element().get_order_lines()
#            self.order_line_row_state = []
#            self.fill_dialog_fields()
#
#    def action_orderline_cell_changed(self, row: int, column: int) -> None:
#        """
#        Handle the order_line_table 'cellChanged' signal.
#
#        The LineEdit and ComboBox elements on a table row capture their
#        'activated' or 'editingFinished' signals and emit a
#        'cellChanged' signal. This connects the signal to the proper
#        handler based on the column number.
#
#        Parameters:
#            row (int): the row of the cell
#            column (int): the column of the cell
#        """
#        if column == self.OLT_LINE:
#            self.action_orderline_line_edit(row)
#        elif column == self.OLT_PART_NUMBER:
#            self.action_orderline_part_number_combo(row)
#
#        elif column == self.OLT_PART_NUMBER:
#            self.action_orderline_part_number_combo(row)
#        elif column == self.OLT_QTY:
#            self.action_orderline_quantity_edit(row)
#        elif column == self.OLT_COST_EA:
#            self.action_orderline_cost_each_edit(row)
#        elif column == self.OLT_REMARKS:
#            self.action_orderline_remarks_edit(row)
#
#    def action_orderline_cell_clicked(self, row: int, button_id: int) -> None:
#        """
#        Handle the order_line_table 'cellClicked' signal.
#
#        The PushButton elements on a table row capture their 'clicked'
#        signals and emit a 'cellClicked' signal. This connects the
#        signal to the proper handler based on the column number.
#
#        Parameters:
#            row (int)" the row of the cell
#            button_id (int): the column of the cell
#        """
#        order_line_row = self.order_lines.get(row)
#
#        edit_save_button = self.form.order_line_table.cellWidget(
#            row, self.OLT_ACTIONS
#        ).get_button(self.OLT_EDIT_SAVE)
#        delete_button = self.form.order_line_table.cellWidget(
#            row, self.OLT_ACTIONS
#        ).get_button(self.OLT_DELETE)
#        if button_id == self.OLT_EDIT_SAVE:
#            if order_line_row.have_values_changed():
#                self.validate_order_line_row(row)
#                if edit_save_button.text() == "Edit":
#                    self.order_line_row_state[row] = RowState.Update
#                elif edit_save_button.text() == "Save":
#                    order_line_row.set_value_valid_flag("record_id", True)
#                    self.order_line_row_state[row] = RowState.Save
#                    if row + 1 == len(self.order_line_row_state):
#                        self.orderline_table_append_line(
#                            self.get_element().get_order_number()
#                        )
#            else:
#                self.order_line_row_state[row] = RowState.NoState
#            if order_line_row.get_value_changed_flag(
#                "quantity"
#            ) or order_line_row.get_value_changed_flag("cost_each"):
#                self.update_subtotal()
#        elif button_id == self.OLT_DELETE:
#            delete_button = self.form.order_line_table.cellWidget(
#                row, self.OLT_ACTIONS
#            ).get_button(button_id)
#            if delete_button.text() == "Del":
#                self.set_orderline_enabled(False, row)
#                self.order_line_row_state[row] = RowState.Delete
#                delete_button.setText("UnDel")
#            elif delete_button.text() == "UnDel":
#                self.set_orderline_enabled(True, row)
#                delete_button.setText("Del")
#                if not order_line_row.have_values_changed():
#                    self.order_line_row_state[row] = RowState.NoState
#                elif order_line_row.get_record_id() > 0:
#                    self.order_line_row_state[row] = RowState.Update
#                else:
#                    self.order_line_row_state[row] = RowState.Save
#                edit_save_button.setEnabled(
#                    order_line_row.have_values_changed()
#                    and order_line_row.is_element_valid()
#                )
#        self.save_buttons_enable(self.have_entries_changed())
#
#    def action_tax_edit(self):
#        """
#        Update/validate the 'tax' entry for the dialog.
#
#        Returns:
#            (dict)
#                ['entry'] - (str) the updated remark
#                ['valid'] - (bool) True if the entered value is valid,
#                    False otherwise
#                ['msg'] - (str) Error message if not valid
#        """
#        result = self.validate_dialog_entry(
#            self.get_element().set_tax,
#            self.form.tax_edit,
#            OrderDialog.tooltips["tax"],
#        )
#        if result["entry"] == 0:
#            self.form.tax_edit.setText("")
#        else:
#            self.form.tax_edit.setText(format(result["entry"], ".2f"))
#
#        if result["valid"]:
#            self.update_total()
#        return result
#
#    def action_orderline_line_edit(self, row: int) -> None:
#        """
#        Update the OrderLine.line number entry.
#
#        This handles the entry of a new line number in the text box.
#
#        Parameters:
#            row (int) the current row of the table
#        """
#        cell_widget = self.form.order_line_table.cellWidget(row, self.OLT_LINE)
#        order_line = self.order_lines.get(row)
#        result = self.validate_dialog_entry(
#            order_line.set_line,
#            cell_widget,
#            OrderDialog.OLT_TOOLTIPS["line"],
#        )
#        return result
#
#    def action_orderline_part_number_combo(self, row: int) -> None:
#        """
#        Validate the OrderLine.part_number entry.
#
#        This handles the entry of a new part number in the combo box.
#        The description cell is also updated to match the new
#        part number.
#
#        Parameters:
#            row (int) the current row of the table
#        """
#        table = self.form.order_line_table
#        part_number_cell = table.cellWidget(row, self.OLT_PART_NUMBER)
#        description_cell = table.cellWidget(row, self.OLT_DESC)
#        order_line = self.order_lines.get(row)
#        part_number = part_number_cell.currentText()
#        result = self.validate_dialog_entry(
#            order_line.set_part_number,
#            part_number_cell,
#            OrderDialog.OLT_TOOLTIPS["part_number"],
#        )
#        if result["valid"]:
#            description_cell.setText(
#                Part(self.get_parts_file(), part_number, "part_number").get_description()
#            )
#        else:
#            description_cell.setText("")
#        return result
#
#        desc = Part(self.get_parts_file(), part_number, "part_number").get_description()
#        table.cellWidget(row, self.OLT_DESC).setText(desc)
#        result = order_line.set_part_number(part_number)
#        edit_save_button = table.cellWidget(row, self.OLT_ACTIONS).get_button(
#            self.OLT_EDIT_SAVE
#        )
#        edit_save_button.setEnabled(
#            order_line.have_values_changed() and result["valid"]
#        )
#        if result["valid"]:
#            cell_widget.setToolTip(self.OLT_TOOLTIPS["part_number"])
#            self.set_valid_format(cell_widget)
#            self.set_valid_format(table.cellWidget(row, self.OLT_DESC))
#        else:
#            cell_widget.setToolTip(
#                result["msg"] + "; " + self.OLT_TOOLTIPS["part_number"]
#            )
#            self.set_invalid_format(cell_widget)
#            self.set_invalid_format(table.cellWidget(row, self.OLT_DESC))
#        cell_widget.setMaxVisibleItems(20)
#        cell_widget.setStyleSheet("combobox-popup: 0;")
#
#    def action_orderline_quantity_edit(self, row: int) -> None:
#        """
#        Update?validate the OrderLine.Quantity entry.
#
#        This handles the entry of a new quantity in the text box. Update.
#
#        Parameters:
#            row (int): the current row of the table
#        """
#        cell_widget = self.form.order_line_table.cellWidget(row, self.OLT_QTY)
#        order_line = self.order_lines.get(row)
#        quantity = cell_widget.text()
#        result = order_line.set_quantity(quantity)
#        edit_save_button = self.form.order_line_table.cellWidget(
#            row, self.OLT_ACTIONS
#        ).get_button(self.OLT_EDIT_SAVE)
#        edit_save_button.setEnabled(
#            order_line.have_values_changed() and result["valid"]
#        )
#        if result["valid"]:
#            cell_widget.setToolTip(self.OLT_TOOLTIPS["quantity"])
#        #            self.set_valid_format(cell_widget)
#        else:
#            cell_widget.setToolTip(result["msg"] + "; " + self.OLT_TOOLTIPS["quantity"])
#            self.set_invalid_format(cell_widget)
#
#    def action_orderline_cost_each_edit(self, row: int) -> None:
#        """
#        Update/validate the 'cost_each' entry for order_line selected.
#
#        This handles the entry of a new 'cost each' value in the text box.
#
#        Parameters:
#            row (int): the current row of the table
#
#        Returns:
#            (dict)
#                ['entry'] - (str) the updated source
#                ['valid'] - (bool) True if the entered value is valid,
#                    False otherwise
#                ['msg'] - (str) Error message if not valid
#        """
#        cell_widget = self.form.order_line_table.cellWidget(row, self.OLT_COST_EA)
#        order_line = self.order_lines.get(row)
#        cost_each = cell_widget.text()
#        result = order_line.set_cost_each(cost_each)
#        edit_save_button = self.form.order_line_table.cellWidget(
#            row, self.OLT_ACTIONS
#        ).get_button(self.OLT_EDIT_SAVE)
#        edit_save_button.setEnabled(
#            order_line.have_values_changed() and result["valid"]
#        )
#        if result["valid"]:
#            cell_widget.setToolTip(self.OLT_TOOLTIPS["cost_each"])
#            cell_widget.setText(format(result["entry"], ".2f"))
#        #            self.set_valid_format(cell_widget)
#        else:
#            cell_widget.setToolTip(
#                result["msg"] + "; " + self.OLT_TOOLTIPS["cost_each"]
#            )
#            self.set_invalid_format(cell_widget)
#        return result
#
#    def action_orderline_remarks_edit(self, row: int) -> None:
#        """
#        Update/validate he OrderLine.Remarks entry.
#
#        This handles the entry of a new remarks in the text box.
#
#        Parameters:
#            row (int) the current row of the table
#        """
#        cell_widget = self.form.order_line_table.cellWidget(row, self.OLT_REMARKS)
#        order_line = self.order_lines.get(row)
#        remarks = cell_widget.text()
#        result = order_line.set_remarks(remarks)
#        edit_save_button = self.form.order_line_table.cellWidget(
#            row, self.OLT_ACTIONS
#        ).get_button(self.OLT_EDIT_SAVE)
#        edit_save_button.setEnabled(
#            order_line.have_values_changed() and result["valid"]
#        )
#        if result["valid"]:
#            cell_widget.setToolTip(self.OLT_TOOLTIPS["remarks"])
#        #            self.set_valid_format(cell_widget)
#        else:
#            cell_widget.setToolTip(result["msg"] + "; " + self.OLT_TOOLTIPS["remarks"])
#            self.set_invalid_format(cell_widget)
#
#    def set_orderline_enabled(self, enabled: bool, row: int) -> None:
#        """
#        Indicate that the OrderLine is enabled or not.
#
#        When the OrderLine is marked for deletion, the widgets should be
#        disabled, otherwise they are enabled.
#
#        If the line is to be set for deletion, the set of LineEdits and
#        Combo Boxes are disabled and the font is set to StrikeOut. The
#        Edit/Save button is disabled and the font is set to StrikeOut.
#
#        If not, the everything is set to white background, the font is
#        set to normal, and the edit button is enabled.
#
#        Parameters:
#            enabled (bool): False if the row is to be marked for
#                deletion, True if not.
#            row (int): the row to be marked.
#        """
#        for col in range(self.OLT_ACTIONS):
#            cell_widget = self.form.order_line_table.cellWidget(row, col)
#            font = cell_widget.font()
#            if isinstance(cell_widget, QLabel):
#                if enabled:
#                    cell_widget.setStyleSheet("QLabel { background: white; }")
#                    font.setWeight(QFont.Normal)
#                else:
#                    cell_widget.setStyleSheet(
#                        "QLabel { background: rgb(240, 240, 240 ); }"
#                    )
#                    font.setWeight(QFont.ExtraLight)
#            else:
#                cell_widget.setEnabled(enabled)
#            font.setStrikeOut(not enabled)
#            cell_widget.setFont(font)
#
#        edit_save_button = self.form.order_line_table.cellWidget(
#            row, self.OLT_ACTIONS
#        ).get_button(self.OLT_EDIT_SAVE)
#        edit_save_button.setEnabled(enabled)
#        font = edit_save_button.font()
#        font.setStrikeOut(not enabled)
#        edit_save_button.setFont(font)
#
#    def validate_order_line_row(self, row: int) -> None:
#        """
#        Validate the entries in an order line row.
#
#        This just steps through each of the actions for the row in question
#
#        Parameters:
#            row (int) the row to be validated
#        """
#        self.action_orderline_line_edit(row)
#        self.action_orderline_part_number_combo(row)
#        self.action_orderline_quantity_edit(row)
#        self.action_orderline_cost_each_edit(row)
#        self.action_orderline_remarks_edit(row)
#
#    def clear_dialog(self) -> None:
#        """Clear the dialog entry fields."""
#        self.set_element(Order(self.get_parts_file()))
#        self.order_lines = self.get_element().get_order_lines()
#        self.order_line_row_state = []
#        self.form.order_line_table.clearContents()
#        table.setRowCount(0)
#        self.fill_dialog_fields()
#
#    def fill_orderline_table(self) -> None:
#        """
#        Fill the Order Line table for the given order number.
#
#        The order lines that exist will have data will be filled in. The
#        last or only line will be an empty line set for adding an order
#        line.
#        """
#        order = self.get_element()
#        self.order_lines = OrderLineSet(
#            self.get_parts_file(), "order_number", order.get_order_number(), "line"
#        )
#
#        self.form.order_line_table.clearContents()
#        self.form.order_line_table.setRowCount(0)
#
#        new_orderline = OrderLine(self.get_parts_file())
#        new_orderline.set_order_number(order.get_order_number())
#        self.order_lines.append(new_orderline)
#
#        # initialize the row state
#        for order_line in self.order_lines:
#            self.order_line_row_state.append(RowState.NoState)
#
#        self.set_orderline_table_widgets(self.order_lines.get_number_elements())
#        self.set_orderline_table_data()
#
#    def orderline_table_append_line(self, order_number: str) -> None:
#        """
#        Append a new empty OrderLine to the Order Line table.
#
#        Parameters:
#            order_number (str) The order number of the order
#        """
#        # Add new OrderLine to the order line set
#        new_orderline = OrderLine(self.get_parts_file())
#        new_orderline.set_value_valid_flag("record_id", True)
#        new_orderline.set_order_number(order_number)
#        self.order_lines.append(new_orderline)
#        self.order_line_row_state.append(RowState.NoState)
#
#        # fill the new row in the table
#        part_list = PartSet(
#            self.get_parts_file(), None, None, "part_number"
#        ).build_option_list("part_number")
#        table = self.form.order_line_table
#        rows = table.rowCount()
#        table.insertRow(rows)
#        self.set_orderline_table_row_widgets(table, rows, part_list)
#        self.fill_orderline_table_row(
#            rows, self.order_lines.get(-1)
#        )  # get last element
#
#    def set_orderline_table_widgets(self, number_rows: int) -> None:
#        """
#        Set up the table widgets.
#
#        This will set up each row with the correct widgets to handle the
#        data. Each row will have the structure:
#            Line -> TableLineEdit, center aligned
#            Part Number -> TableComboBox
#            Description -> QLabel
#            Quantity -> TableLineEdit, right aligned
#            Cost Each -> TableLineEdit, right aligned
#            Remarks -> TableLineEdit, left aligned
#            Action -> Button Group with 2 PushButtons
#                (Edit/Save and Delete/UnDelete)
#        """
#        table = self.form.order_line_table
#        table.setRowCount(number_rows)
#        part_list = PartSet(
#            self.get_parts_file(), None, None, "part_number"
#        ).build_option_list("part_number")
#
#        for row in range(number_rows):
#            self.set_orderline_table_row_widgets(table, row, part_list)
#
#    def set_orderline_table_row_widgets(
#        self, table: QTableWidget, row: int, part_list: list[str]
#    ) -> None:
#        """
#        Set a single row of widgets for the order line table.
#
#        Parameters:
#            table (QTableWidget): the table being filled
#            row (int): the row number to fill.
#            part_list (List[str]) the part list for the combo box selections
#        """
#        widget_line = TableLineEdit(
#            table, row, self.OLT_LINE, Qt.AlignmentFlag.AlignCenter
#        )
#        widget_line.setToolTip(self.OLT_TOOLTIPS["line"])
#        table.setCellWidget(row, self.OLT_LINE, widget_line)
#
#        widget_pn = TableComboBox(table, row, self.OLT_PART_NUMBER, part_list)
#        widget_pn.setToolTip(self.OLT_TOOLTIPS["part_number"])
#        table.setCellWidget(row, self.OLT_PART_NUMBER, widget_pn)
#
#        widget_desc = TableLineEdit(
#            table, row, self.OLT_DESC, Qt.AlignRight | Qt.AlignVCenter
#        )
#        widget_desc.setReadOnly(True)
#        widget_desc.setToolTip(self.OLT_TOOLTIPS["description"])
#        table.setCellWidget(row, self.OLT_DESC, widget_desc)
#
#        widget_qty = TableLineEdit(
#            table, row, self.OLT_QTY, Qt.AlignRight | Qt.AlignVCenter
#        )
#        widget_qty.setToolTip(self.OLT_TOOLTIPS["quantity"])
#        table.setCellWidget(row, self.OLT_QTY, widget_qty)
#
#        widget_cost_ea = TableLineEdit(
#            table, row, self.OLT_COST_EA, Qt.AlignRight | Qt.AlignVCenter
#        )
#        widget_cost_ea.setToolTip(self.OLT_TOOLTIPS["cost_each"])
#        table.setCellWidget(row, self.OLT_COST_EA, widget_cost_ea)
#
#        widget_remarks = TableLineEdit(
#            table, row, self.OLT_REMARKS, Qt.AlignRight | Qt.AlignVCenter
#        )
#        widget_remarks.setToolTip(self.OLT_TOOLTIPS["remarks"])
#        table.setCellWidget(row, self.OLT_REMARKS, widget_remarks)
#
#        table.setCellWidget(
#            row, self.OLT_ACTIONS, TableButtonGroup(table, row, self.OLT_ACTIONS)
#        )
#
#    def set_orderline_table_data(self) -> None:
#        """
#        Add the order line set data to the dialog.
#
#        Each row is filled with the data from the order lines and the
#        Edit/Save and Delete buttons are initialized.
#        """
#        row = 0
#        for order_line in self.order_lines:
#            self.fill_orderline_table_row(row, order_line)
#            row += 1
#
#    def fill_orderline_table_row(self, row: int, order_line: OrderLine) -> None:
#        """
#        Fill a single line of the OrderLine table with data.
#
#        Parameters:
#            row (int) the row to be filled.
#            order_line (OrderLine) the OrderLine for this row
#        """
#        table = self.form.order_line_table
#        line_number = order_line.get_line()
#        if line_number == 0:
#            line_number = ""
#        table.cellWidget(row, self.OLT_LINE).setText(str(line_number))
#
#        part_number = order_line.get_part_number()
#        table.cellWidget(row, self.OLT_PART_NUMBER).setCurrentText(part_number)
#
#        desc = Part(self.get_parts_file(), part_number, "part_number").get_description()
#        table.cellWidget(row, self.OLT_DESC).setText(desc)
#
#        quantity = order_line.get_quantity()
#        if quantity == 0:
#            quantity = ""
#        table.cellWidget(row, self.OLT_QTY).setText(str(quantity))
#
#        cost_each = order_line.get_cost_each()
#        if cost_each == 0:
#            cost_each = ""
#            table.cellWidget(row, self.OLT_COST_EA).setText(cost_each)
#        else:
#            table.cellWidget(row, self.OLT_COST_EA).setText(format(cost_each, ".2f"))
#        table.cellWidget(row, self.OLT_REMARKS).setText(order_line.get_remarks())
#
#        button_group = table.cellWidget(row, self.OLT_ACTIONS)
#
#        if order_line.get_record_id() > 0:
#            edit_save_button = button_group.add_button("Edit", self.OLT_EDIT)
#            edit_save_button.setToolTip(self.OLT_TOOLTIPS["edit"])
#        else:
#            edit_save_button = button_group.add_button("Save", self.OLT_SAVE)
#            edit_save_button.setToolTip(self.OLT_TOOLTIPS["save"])
#
#        delete_button = button_group.add_button("Del", self.OLT_DELETE)
#        delete_button.setToolTip(self.OLT_TOOLTIPS["delete"])
#
#    def setup_order_line_table(self) -> None:
#        """
#        Initialize the basic orderline table.
#
#        This includes the header names, the column widths and the
#        stretch column.
#        """
#        self.form.order_line_table.setVisible(True)
#
#        header = self.form.order_line_table.horizontalHeader()
#        header_model = header.selectionModel()
#
#        header_model.setHorizontalHeaderLabels(self.OLT_COLUMN_NAMES)
#        header.setHeaderData(1, self.COLUMN_WIDTHS[i])
#        header.stretchLastSection(True)


