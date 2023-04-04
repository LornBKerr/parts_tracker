"""
Base class for the Parts System dialogs.

File:       base_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2020 - 2023 Lorn B Kerr
License:    MIT, see file License
"""


# import base64
# import csv
# import os
# from copy import deepcopy
# from pathlib import Path
# from typing import Any, Callable, ClassVar, Union
# from PyQt6.QtCore import Qt
#
# from PyQt6.QtGui import QIcon, QPixmap
# QDialog,, QFileDialog, QLabel, QMessageBox,
#                             )
#
#
# from common_table_support import RowState, TableSupport
# from forms import (ChangePartNumberForm, EditStructureForm, ItemForm,
#                   OrderForm, PartForm, SaveAssyListForm)
#
#
from lbk_library import Dbal, Dialog
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView, QMainWindow, QTableWidget, QTableWidgetItem

from elements import Order, OrderLineSet  # , PartSet, SourceSet

#
#
# (ConditionSet,, ItemSet, Order, OrderLine,
#                            OrderLineSet, OrderSet, Part, PartSet, SourceSet)
# from parts_tracker_constants import OLC
#
# from openpyxl import workbook


class BaseDialog(Dialog):
    """
    Base class for the Parts System dialogs.

    Holds common functions used by all the editing dialogs in the parts
    database program.
    """

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

    def __init__(self, parent: QMainWindow, dbref: Dbal) -> None:
        """
        Initialize the DialogBase.

        Parameters:
            parent(QMainWindow):  the parent window owning this dialog.
            dbref (Dbal): reference to the database for this item.
        """
        super().__init__(parent, dbref)

    def set_table_header(
        self,
        table: QTableWidget,
        col_names: list[str],
        col_widths: list[int],
        stretch_column: int = None,
    ) -> None:
        """
        Set the header column names for a QTable.

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

    def save_buttons_enable(self, enable: bool) -> None:
        """
        Enable/Disable the save buttons.

        Parameters:
            enable (Boolean) True if the buttons should be enabled,
                False is not
        """
        self.form.save_new_button.setEnabled(enable)
        self.form.save_done_button.setEnabled(enable)

    #    def fill_record_id_selections(
    #        self, entry_list: list[str], record_id: int | None = None
    #    ) -> None:
    #        """
    #        Fill the record id selection box with the given numbers.
    #
    #        Select the given record id if not None.
    #
    #        Paramters:
    #            entry_list (list): of valid record_id numbers.
    #            record_id (integer): (Optional) the record id to be initally
    #                selected.
    #        """
    #        self.form.record_id_combo.clear()
    #        self.form.record_id_combo.addItems(entry_list)
    #        self.form.record_id_combo.setCurrentIndex(
    #            self.form.record_id_combo.findText(str(record_id))
    #        )
    #
    #    def fill_part_number_selections(self, part_number: str = None) -> None:
    #        """
    #        Fill the part number selection box with set of part numbers.
    #
    #        The given part number, if any, will be displayed.
    #
    #        Parameters:
    #            part_number (str): the selected intial part number (Optional)
    #        """
    #        partset = PartSet(self.get_dbref(), None, None, "part_number")
    #        part_list = partset.build_option_list("part_number")
    #        self.form.part_number_combo.clear()
    #        self.form.part_number_combo.addItems(part_list)
    #        self.form.part_number_combo.setCurrentIndex(
    #            self.form.part_number_combo.findText(part_number)
    #        )
    #
    #    def fill_source_selections(self, source: str = None) -> None:
    #        """
    #        Fill the source selection box with the set of possible sources.
    #
    #        The initial source, if not None, will be displayed
    #
    #        Parameters:
    #            source (String) the selected initial condition (Optional)
    #        """
    #        sourceset = SourceSet(self.get_dbref(), None, None, "source")
    #        source_list = sourceset.build_option_list("source")
    #        self.form.source_combo.clear()
    #        self.form.source_combo.addItems(source_list)
    #        index = self.form.source_combo.findText(source)
    #        self.form.source_combo.setCurrentIndex(index)

    def fill_order_table_fields(self, part_number: str) -> None:
        """
        Fill the order listing with the order lines for the current part.

        Parameters:
            part_number (String) The current part part number.
        """
        order_lines = OrderLineSet(
            self.get_dbref(), "part_number", part_number, "order_number"
        )
        if not part_number:
            order_lines.set_property_set([])
        table = self.form.order_table
        table.setRowCount(order_lines.get_number_elements())
        row = 0
        for order_line in order_lines:
            order = Order(self.get_dbref(), order_line.get_order_number())
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
