"""
Provide common functions and constants for the Parts System dialogs.

File:       dialog_support.py
Author:     Lorn B Kerr
Copyright:  (c) 2020,2023, 2024 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.1.1
"""

from lbk_library import DataFile as PartsFile
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (  # QPushButton,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from elements import Order, OrderLineSet

file_version = "1.1.1"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Revised Dialog import from lbk_library to lbk_library.gui",
    "1.1.0": "Changed library 'PyQt5' to 'PySide6'",
    "1.1.1": "Refactored from a class to a set of independent functions and constants.",
}

PART_ORDER_COL_NAMES = [
    "Order",
    "Date",
    "Source",
    "Line",
    "Part Number",
    "Cost Each",
    "Quantity",
    "Remarks",
]
""" Names of the Order Table columns for the Item and Part dialogs."""

PART_ORDER_COL_WIDTHS = [60, 100, 60, 40, 120, 70, 100, 1]
""" Widths of the Order Table columns for the Item and Part dialogs."""


def set_table_header(
    table: QTableWidget,
    col_names: list[str],
    col_widths: list[int],
    stretch_column: int = None,
) -> None:
    """
    Set the header column names for a QTableWidget.

    Parameters:
        table (QTableWidget): The QTableWidget to set the headers.
        col_names (lits[str]): the names of the columns
        col_widths (list[int]): the column widths
        stretch_column (int): the column number to stretch to fill
            the remaining table width.
    """
    table.setColumnCount(len(col_names))
    table.setHorizontalHeaderLabels(col_names)
    for i in range(0, len(col_widths)):
        table.setColumnWidth(i, col_widths[i])
    if stretch_column is not None:
        table.horizontalHeader().setSectionResizeMode(
            stretch_column, QHeaderView.ResizeMode.Stretch
        )


# def buttons_enable(button_list: list[QPushButton], enable: bool) -> None:
#    """
#    Enable/Disable the set of buttons in the button list.
#
#    Parameters:
#        button_list (list[QPushButton]): the list of buttons to enable.
#        enable (Boolean) True if the buttons should be enabled,
#            False is not
#    """
#    for button in button_list:
#        button.setEnabled(enable)


def fill_order_table_fields(
    parts_file: PartsFile, part_number: str, table: QTableWidget
) -> None:
    """
    Fill the order listing with the order lines for the current part.

    Parameters:
        part_number (String) The current part part number.
    """
    order_lines = OrderLineSet(parts_file, "part_number", part_number, "order_number")

    if not part_number:
        order_lines.set_property_set([])
    table.setRowCount(order_lines.get_number_elements())
    row = 0
    for order_line in order_lines:
        order = Order(parts_file, order_line.get_order_number())
        entry = QTableWidgetItem(order_line.get_order_number())
        entry.setTextAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        table.setItem(row, 0, entry)

        entry = QTableWidgetItem(order.get_date())
        entry.setTextAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        table.setItem(row, 1, entry)

        table.setItem(row, 2, QTableWidgetItem(order.get_source()))
        entry = QTableWidgetItem(str(order_line.get_line()))
        entry.setTextAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        table.setItem(row, 3, entry)

        entry = QTableWidgetItem(order_line.get_part_number())
        table.setItem(row, 4, entry)

        entry = QTableWidgetItem(format(float(order_line.get_cost_each()), ".2f"))
        entry.setTextAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        table.setItem(row, 5, entry)
        entry = QTableWidgetItem(str(order_line.get_quantity()))
        entry.setTextAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        table.setItem(row, 6, entry)

        table.setItem(row, 7, QTableWidgetItem(order_line.get_remarks()))
        row += 1
